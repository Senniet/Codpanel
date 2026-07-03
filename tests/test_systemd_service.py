import subprocess
from unittest.mock import patch

import app.services.systemd_service as ss


class DummyProc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_unit_exists_true():
    with patch("shutil.which", return_value="/bin/systemctl"):
        mock_proc = DummyProc(returncode=0, stdout="Loaded: loaded\n")
        with patch("subprocess.run", return_value=mock_proc):
            assert ss.unit_exists("cod1.service") is True


def test_unit_exists_false_not_found():
    with patch("shutil.which", return_value="/bin/systemctl"):
        # simulate systemctl reporting "not found" on stderr
        mock_proc = DummyProc(returncode=1, stdout="", stderr="Unit could not be found\n")
        with patch("subprocess.run", return_value=mock_proc):
            assert ss.unit_exists("cod1.service") is False


def test_unit_exists_false_no_systemctl():
    with patch("shutil.which", return_value=None):
        assert ss.unit_exists("cod1.service") is False


def test_get_active_state_active():
    with patch("shutil.which", return_value="/bin/systemctl"):
        mock_proc = DummyProc(returncode=0, stdout="active\n")
        with patch("subprocess.run", return_value=mock_proc):
            assert ss.get_active_state("cod1.service") == "active"


def test_get_active_state_unknown_on_error():
    with patch("shutil.which", return_value="/bin/systemctl"):
        with patch("subprocess.run", side_effect=RuntimeError("boom")):
            assert ss.get_active_state("cod1.service") == "unknown"


def test_get_main_pid_valid_and_zero_and_malformed():
    with patch("shutil.which", return_value="/bin/systemctl"):
        # valid pid
        mock_proc = DummyProc(returncode=0, stdout="1234\n")
        with patch("subprocess.run", return_value=mock_proc):
            assert ss.get_main_pid("cod1.service") == 1234

        # zero pid -> None
        mock_proc_zero = DummyProc(returncode=0, stdout="0\n")
        with patch("subprocess.run", return_value=mock_proc_zero):
            assert ss.get_main_pid("cod1.service") is None

        # malformed output
        mock_proc_bad = DummyProc(returncode=0, stdout="not-a-number\n")
        with patch("subprocess.run", return_value=mock_proc_bad):
            assert ss.get_main_pid("cod1.service") is None


def test_get_exec_start_timestamp():
    with patch("shutil.which", return_value="/bin/systemctl"):
        ts = "Mon 2026-07-03 12:34:56 CEST"
        mock_proc = DummyProc(returncode=0, stdout=ts + "\n")
        with patch("subprocess.run", return_value=mock_proc):
            assert ss.get_exec_start_timestamp("cod1.service") == ts


def test_timeout_handling():
    with patch("shutil.which", return_value="/bin/systemctl"):
        def raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs.get("timeout", None))

        with patch("subprocess.run", side_effect=raise_timeout):
            assert ss.unit_exists("cod1") is False
            assert ss.get_active_state("cod1") == "unknown"
            assert ss.get_main_pid("cod1") is None
            assert ss.get_exec_start_timestamp("cod1") is None


def test_subprocess_filenotfound_handled():
    # systemctl reported present by which, but running it raises FileNotFoundError
    with patch("shutil.which", return_value="/bin/systemctl"):
        with patch("subprocess.run", side_effect=FileNotFoundError("no such file")):
            assert ss.unit_exists("cod1") is False
            assert ss.get_active_state("cod1") == "unknown"
            assert ss.get_main_pid("cod1") is None
            assert ss.get_exec_start_timestamp("cod1") is None


def test_subprocess_runtime_error_handled():
    with patch("shutil.which", return_value="/bin/systemctl"):
        with patch("subprocess.run", side_effect=RuntimeError("boom")):
            assert ss.unit_exists("cod1") is False
            assert ss.get_active_state("cod1") == "unknown"
            assert ss.get_main_pid("cod1") is None
            assert ss.get_exec_start_timestamp("cod1") is None
