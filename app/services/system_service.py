import psutil
import platform
import socket
import time


class SystemService:

    @staticmethod
    def get_system_info():

        uptime = time.time() - psutil.boot_time()

        return {

            "hostname": socket.gethostname(),

            "platform": platform.system(),

            "platform_version": platform.release(),

            "cpu_percent": psutil.cpu_percent(interval=0.2),

            "cpu_cores": psutil.cpu_count(),

            "memory_total": round(
                psutil.virtual_memory().total / 1024 / 1024
            ),

            "memory_used": round(
                psutil.virtual_memory().used / 1024 / 1024
            ),

            "memory_percent": psutil.virtual_memory().percent,

            "uptime": round(uptime),

        }
