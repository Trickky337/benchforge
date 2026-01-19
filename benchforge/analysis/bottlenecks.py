def analyze_bottlenecks(report: dict):
    cpu_ops = report["benchmarks"]["cpu"]["approx_ops_per_sec"]
    disk_r = report["benchmarks"]["disk"]["read_mbps"]
    disk_w = report["benchmarks"]["disk"]["write_mbps"]

    notes = []

    # Simple MVP heuristics (we'll improve later)
    if disk_r < 300 or disk_w < 300:
        notes.append("Storage looks relatively slow; may impact load times and large-file workflows.")
    if cpu_ops < 8_000_000:
        notes.append("CPU score is modest; CPU-bound workloads may bottleneck (compiling, heavy multitasking).")

    if not notes:
        notes.append("No obvious bottleneck detected from basic CPU/Disk checks (expand tests for GPU/thermals).")

    return {"notes": notes}
