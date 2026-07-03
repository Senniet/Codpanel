from app.services.process_service import ProcessService

process = ProcessService.find_cod_process()

if process:
    print("Server gevonden")
    print(f"PID: {process.pid}")
    print(f"Naam: {process.name()}")
    print(f"CPU: {process.cpu_percent(interval=0.2)}%")
    print(f"RAM: {process.memory_info().rss / 1024 / 1024:.1f} MB")
    print(f"Commandline: {' '.join(process.cmdline())}")
else:
    print("Geen COD-server gevonden")
