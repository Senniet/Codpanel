import time
from unittest.mock import Mock, patch

import psutil
from app.services.process_stats import ProcessStatsService
from app.models.process import ProcessStats


class DummyMem:
    def __init__(self, rss):
        self.rss = rss


def make_proc(cpu=1.5, rss=50 * 1024 * 1024, create_time=1000.0):
    proc = Mock()
    proc.cpu_percent.return_value = cpu
    proc.memory_info.return_value = DummyMem(rss)
    proc.create_time.return_value = create_time
    return proc


def test_normal_process():
    pid = 1234
    proc = make_proc(cpu=2.5, rss=100 * 1024 * 1024, create_time=1000.0)
    with patch("psutil.Process", return_value=proc):
        with patch("time.time", return_value=2000.0):
            svc = ProcessStatsService()
            stats = svc.get_process_stats(pid)

    assert isinstance(stats, ProcessStats)
    assert stats.pid == pid
    assert abs(stats.cpu_percent - 2.5) < 1e-6
    assert abs(stats.memory_mb - 100.0) < 1e-3
    assert abs(stats.create_time - 1000.0) < 1e-6
    assert abs(stats.uptime_seconds - 1000.0) < 1e-6


def test_missing_process_returns_none():
    with patch("psutil.Process", side_effect=psutil.NoSuchProcess(pid=9999)):
        svc = ProcessStatsService()
        assert svc.get_process_stats(9999) is None


def test_access_denied_returns_none():
    with patch("psutil.Process", side_effect=psutil.AccessDenied(pid=1)):
        svc = ProcessStatsService()
        assert svc.get_process_stats(1) is None


def test_zombie_returns_none():
    with patch("psutil.Process", side_effect=psutil.ZombieProcess(pid=2)):
        svc = ProcessStatsService()
        assert svc.get_process_stats(2) is None


def test_invalid_pid_returns_none():
    # psutil may raise ValueError for invalid PIDs; simulate that
    with patch("psutil.Process", side_effect=ValueError("invalid pid")):
        svc = ProcessStatsService()
        assert svc.get_process_stats(-1) is None


def test_cpu_and_memory_conversion():
    pid = 5678
    proc = make_proc(cpu=0.0, rss=12345678, create_time=1500.0)
    with patch("psutil.Process", return_value=proc):
        with patch("time.time", return_value=1600.0):
            svc = ProcessStatsService()
            stats = svc.get_process_stats(pid)

    assert stats is not None
    assert abs(stats.memory_mb - (12345678 / (1024 * 1024))) < 1e-6
    assert stats.cpu_percent == 0.0
    assert abs(stats.uptime_seconds - 100.0) < 1e-6
