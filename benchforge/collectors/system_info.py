import platform
import psutil


def collect_system_info():
    cpu_freq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "max_freq_mhz": getattr(cpu_freq, "max", None),
        },
        "memory": {"total_gb": round(mem.total / (1024**3), 2)},
        "storage": {"total_gb": round(disk.total / (1024**3), 2)},
    }
