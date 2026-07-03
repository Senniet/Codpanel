"""Systemd service abstraction for CodPanel.

Provides read-only helpers to query systemd about units. All methods are
non-raising and return safe defaults on failure. This module only supports
Linux with systemctl available; if not present the methods return safe values.

Do NOT perform any lifecycle actions (start/stop/restart) here; only queries.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


def _has_systemctl() -> bool:
    """Return True if systemctl is available on this host.

    Do not cache the result at module import time so unit tests can patch
    shutil.which() and simulate environments with or without systemctl.
    Calling shutil.which() is inexpensive and keeps detection correct.
    """
    return shutil.which("systemctl") is not None


def unit_exists(unit: str, timeout: float = 2.0) -> bool:
    """Return True if the given systemd unit exists on the system.

    Uses `systemctl status <unit>` and interprets the output. This is a best
    effort check and will return False if systemctl is not available or the
    command indicates the unit could not be found.
    """
    if not _has_systemctl():
        logger.debug("systemctl not available, unit_exists(%s) -> False", unit)
        return False

    try:
        proc = subprocess.run(
            ["systemctl", "status", unit],
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:  # defensive: don't leak exceptions
        logger.exception("unit_exists: subprocess failed for unit=%s: %s", unit, exc)
        return False

    stderr = (proc.stderr or "").lower()
    stdout = proc.stdout or ""

    if "could not be found" in stderr or "not found" in stderr:
        logger.debug("unit_exists: unit %s not found (stderr=%s)", unit, stderr.strip())
        return False

    # If status returned anything, assume unit exists (even if inactive/failed)
    if proc.returncode == 0 or stdout or stderr:
        logger.debug("unit_exists: unit %s appears present (returncode=%s)", unit, proc.returncode)
        return True

    logger.debug("unit_exists: unit %s not present (empty output)", unit)
    return False


def get_active_state(unit: str, timeout: float = 2.0) -> str:
    """Return the active state of the unit (e.g., 'active', 'inactive', 'failed').

    Returns 'unknown' if systemctl is unavailable or the state cannot be
    determined.
    """
    if not _has_systemctl():
        logger.debug("systemctl not available, get_active_state(%s) -> 'unknown'", unit)
        return "unknown"

    try:
        proc = subprocess.run(
            ["systemctl", "is-active", unit],
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        logger.exception("get_active_state: subprocess failed for unit=%s: %s", unit, exc)
        return "unknown"

    state = (proc.stdout or proc.stderr or "").strip()
    if not state:
        logger.debug("get_active_state: empty state for unit=%s (returncode=%s)", unit, proc.returncode)
        return "unknown"

    logger.debug("get_active_state: unit=%s state=%s", unit, state)
    return state


def get_main_pid(unit: str, timeout: float = 2.0) -> Optional[int]:
    """Return the MainPID of the unit, or None if not available.

    Uses `systemctl show -p MainPID --value` which prints a numeric PID or 0.
    """
    if not _has_systemctl():
        logger.debug("systemctl not available, get_main_pid(%s) -> None", unit)
        return None

    try:
        proc = subprocess.run(
            ["systemctl", "show", unit, "-p", "MainPID", "--value"],
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        logger.exception("get_main_pid: subprocess failed for unit=%s: %s", unit, exc)
        return None

    out = (proc.stdout or "").strip()
    if not out:
        logger.debug("get_main_pid: empty output for unit=%s", unit)
        return None

    try:
        pid = int(out)
        if pid <= 0:
            return None
        return pid
    except ValueError:
        logger.debug("get_main_pid: unexpected pid value for unit=%s: %r", unit, out)
        return None


def get_exec_start_timestamp(unit: str, timeout: float = 2.0) -> Optional[str]:
    """Return the ExecMainStartTimestamp value for the unit as a string.

    This returns the raw timestamp string reported by systemd or None if it
    cannot be determined. Parsing to datetime is left to callers if needed.
    """
    if not _has_systemctl():
        logger.debug("systemctl not available, get_exec_start_timestamp(%s) -> None", unit)
        return None

    try:
        proc = subprocess.run(
            ["systemctl", "show", unit, "-p", "ExecMainStartTimestamp", "--value"],
            timeout=timeout,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        logger.exception("get_exec_start_timestamp: subprocess failed for unit=%s: %s", unit, exc)
        return None

    out = (proc.stdout or "").strip()
    if not out:
        logger.debug("get_exec_start_timestamp: empty output for unit=%s", unit)
        return None

    # Return the raw string; parsing can be performed by the caller.
    logger.debug("get_exec_start_timestamp: unit=%s exec_start=%s", unit, out)
    return out
