from unittest.mock import Mock, patch
from datetime import datetime

import app.services.server_manager as sm
from app.models.server import ServerConfig, ServerStatus
from app.models.process import ProcessStats


def make_config(id_: str, unit: str):
    return ServerConfig(id=id_, name=f"Server {id_}", systemd_unit=unit)


def test_get_servers_all_running():
    cfg1 = make_config("s1", "s1.service")
    cfg2 = make_config("s2", "s2.service")

    config_loader = Mock()
    config_loader.get_all.return_value = [cfg1, cfg2]
    config_loader.get.side_effect = lambda sid: cfg1 if sid == "s1" else cfg2 if sid == "s2" else None

    systemd = Mock()
    systemd.unit_exists.return_value = True
    systemd.get_active_state.side_effect = lambda unit: "active" if unit == "s1.service" else "inactive"
    systemd.get_main_pid.side_effect = lambda unit: 111 if unit == "s1.service" else 0

    proc_stats = Mock()
    proc_stats.get_process_stats.side_effect = lambda pid: ProcessStats(pid=111, cpu_percent=1.2, memory_mb=50.0, create_time=1600.0, uptime_seconds=100.0) if pid == 111 else None

    mgr = sm.ServerManager(config_loader, systemd, proc_stats)
    servers = mgr.get_servers()

    assert len(servers) == 2
    s1 = next(s for s in servers if s.id == "s1")
    assert s1.status == "running"
    assert s1.active_state == "active"
    assert s1.pid == 111
    assert s1.cpu_percent == 1.2


def test_get_server_unit_missing_and_error_isolated():
    cfg1 = make_config("s1", "s1.service")
    cfg2 = make_config("s2", "s2.service")

    config_loader = Mock()
    config_loader.get_all.return_value = [cfg1, cfg2]
    config_loader.get.return_value = cfg1

    systemd = Mock()

    # s1: unit missing
    def unit_exists_side(unit):
        if unit == "s1.service":
            return False
        if unit == "s2.service":
            return True
        return False

    systemd.unit_exists.side_effect = unit_exists_side

    # s2: get_active_state raises
    def get_active_state_side(unit):
        if unit == "s2.service":
            raise RuntimeError("boom")
        return "inactive"

    systemd.get_active_state.side_effect = get_active_state_side
    systemd.get_main_pid.return_value = None

    proc_stats = Mock()

    mgr = sm.ServerManager(config_loader, systemd, proc_stats)
    servers = mgr.get_servers()

    # s1 should be reported as unit_missing
    s1 = next(s for s in servers if s.id == "s1")
    assert s1.status == "unit_missing"

    # s2 should still be present despite systemd.get_active_state raising
    s2 = next(s for s in servers if s.id == "s2")
    assert s2 is not None


def test_get_server_single_lookup():
    cfg = make_config("s1", "s1.service")
    config_loader = Mock()
    config_loader.get.return_value = cfg

    systemd = Mock()
    systemd.unit_exists.return_value = True
    systemd.get_active_state.return_value = "active"
    systemd.get_main_pid.return_value = 222

    proc_stats = Mock()
    proc_stats.get_process_stats.return_value = ProcessStats(pid=222, cpu_percent=0.5, memory_mb=10.0, create_time=1000.0, uptime_seconds=500.0)

    mgr = sm.ServerManager(config_loader, systemd, proc_stats)
    s = mgr.get_server("s1")

    assert isinstance(s, ServerStatus)
    assert s.id == "s1"
    assert s.pid == 222
    assert s.cpu_percent == 0.5
