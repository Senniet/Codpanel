"""Process stats service using psutil.

Provides a small service to retrieve current runtime statistics for a PID.
All errors are handled and logged; None is returned for unavailable processes.
"""
from __future__ import annotations

import logging
import time
from typing import Optional

import psutil

from app.models.process import ProcessStats

logger = logging.getLogger(__name__)


class ProcessStatsService:
    """Service to retrieve live process statistics."""

    def get_process_stats(self, pid: int) -> Optional[ProcessStats]:
        """Return ProcessStats for the given pid, or None if not available.

        Handles psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess
        gracefully and returns None. Always queries live values (no caching).
        """
        try:
            proc = psutil.Process(pid)

            # Non-blocking cpu_percent call (interval=None). The value may be 0.0
            # on the first call; callers should call periodically for accurate values.
            cpu = proc.cpu_percent(interval=None)

            # memory in bytes -> convert to MB
            mem_info = proc.memory_info()
            rss = getattr(mem_info, "rss", None)

            create_time = proc.create_time()
            now = time.time()
            uptime = now - create_time if create_time is not None else None

            stats = ProcessStats(
                pid=int(pid),
                cpu_percent=float(cpu) if cpu is not None else None,
                memory_mb=(float(rss) / (1024 * 1024)) if rss is not None else None,
                create_time=float(create_time) if create_time is not None else None,
                uptime_seconds=float(uptime) if uptime is not None else None,
            )
            return stats
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as exc:
            logger.debug("Process %s not available: %s", pid, exc)
            return None
        except Exception as exc:
            # Defensive: never raise to callers; log and return None.
            logger.exception("Unexpected error while fetching stats for pid=%s: %s", pid, exc)
            return None
