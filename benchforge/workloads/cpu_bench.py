import time


def _work(n: int) -> int:
    x = 0
    for i in range(n):
        x = (x * 1664525 + 1013904223) & 0xFFFFFFFF
    return x


def run_cpu_bench(profile: str = "standard"):
    loops = 30_000_000 if profile == "standard" else 10_000_000
    start = time.perf_counter()
    _ = _work(loops)
    elapsed = time.perf_counter() - start
    score = round(loops / max(elapsed, 1e-9), 2)

    return {
        "loops": loops,
        "elapsed_sec": round(elapsed, 3),
        "approx_ops_per_sec": score
    }
