import os
import time
import tempfile


def run_disk_bench(profile: str = "standard"):
    size_mb = 512 if profile == "standard" else 128
    chunk = b"\0" * (1024 * 1024)  # 1MB

    fd, path = tempfile.mkstemp(prefix="benchforge_", suffix=".bin")
    os.close(fd)

    # WRITE test
    start = time.perf_counter()
    with open(path, "wb") as f:
        for _ in range(size_mb):
            f.write(chunk)
        f.flush()
        os.fsync(f.fileno())
    write_elapsed = time.perf_counter() - start

    # READ test
    start = time.perf_counter()
    with open(path, "rb") as f:
        while f.read(len(chunk)):
            pass
    read_elapsed = time.perf_counter() - start

    os.remove(path)

    return {
        "size_mb": size_mb,
        "write_sec": round(write_elapsed, 3),
        "read_sec": round(read_elapsed, 3),
        "write_mbps": round(size_mb / max(write_elapsed, 1e-9), 2),
        "read_mbps": round(size_mb / max(read_elapsed, 1e-9), 2),
    }
