import subprocess
from datetime import datetime

from app.services.process_service import ProcessService


class ServerService:
    @staticmethod
    def status():
        process = ProcessService.find_cod_process()

        if process is None:
            return {
                "online": False,
                "pid": None,
                "name": None,
                "memory_mb": 0,
                "cpu_percent": 0,
                "status": "offline",
                "uptime": "Offline",
            }

        memory = round(process.memory_info().rss / 1024 / 1024, 1)

        cpu = process.cpu_percent(interval=0.1)

        started = datetime.fromtimestamp(process.create_time())

        uptime = datetime.now() - started

        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        seconds = uptime.seconds % 60

        if days:
            uptime_string = f"{days}d {hours}h {minutes}m"
        elif hours:
            uptime_string = f"{hours}h {minutes}m"
        elif minutes:
            uptime_string = f"{minutes}m {seconds}s"
        else:
            uptime_string = f"{seconds}s"

        return {
            "online": True,
            "pid": process.pid,
            "name": process.name(),
            "memory_mb": memory,
            "cpu_percent": cpu,
            "status": process.status(),
            "uptime": uptime_string,
        }

    @staticmethod
    def start():

        subprocess.run(
            ["systemctl", "start", "cod1"],
            check=False,
        )

        return ServerService.status()

    @staticmethod
    def stop():

        subprocess.run(
            ["systemctl", "stop", "cod1"],
            check=False,
        )

        return ServerService.status()

    @staticmethod
    def restart():

        subprocess.run(
            ["systemctl", "restart", "cod1"],
            check=False,
        )

        return ServerService.status()