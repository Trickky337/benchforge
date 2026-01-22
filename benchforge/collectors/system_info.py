import platform
import psutil

import subprocess


def collect_gpu_info():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True
        )
        name, mem = result.stdout.strip().split(", ")
        return {"vendor": "NVIDIA", "name": name, "memory_total": mem}
    except Exception:
        return {"vendor": "unknown"}



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
        "gpu": collect_gpu_info(),
        "memory": {"total_gb": round(mem.total / (1024**3), 2)},
        "storage": {"total_gb": round(disk.total / (1024**3), 2)},
    }
