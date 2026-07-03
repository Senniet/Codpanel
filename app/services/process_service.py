import psutil


class ProcessService:

    @staticmethod
    def find_cod_process():

        for process in psutil.process_iter(
            ["pid", "name", "cmdline", "memory_info", "cpu_percent"]
        ):

            try:

                cmdline = " ".join(process.info["cmdline"] or [])

                if "cod_lnxded" in cmdline:

                    return process

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):
                pass

        return None
