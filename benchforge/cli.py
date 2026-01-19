import argparse
import json
from datetime import datetime

from benchforge.collectors.system_info import collect_system_info
from benchforge.workloads.cpu_bench import run_cpu_bench
from benchforge.workloads.disk_bench import run_disk_bench
from benchforge.analysis.bottlenecks import analyze_bottlenecks


def main():
    parser = argparse.ArgumentParser(prog="benchforge", description="Benchmark & Bottleneck Analyzer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="Run benchmarks and generate report")
    runp.add_argument("--out", default="report.json", help="Output JSON report path")
    runp.add_argument("--profile", default="standard", choices=["light", "standard"], help="Benchmark profile")

    args = parser.parse_args()

    if args.cmd == "run":
        report = {
            "tool": "benchforge",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "profile": args.profile,
            "system": collect_system_info(),
            "benchmarks": {},
            "analysis": {}
        }

        report["benchmarks"]["cpu"] = run_cpu_bench(profile=args.profile)
        report["benchmarks"]["disk"] = run_disk_bench(profile=args.profile)
        report["analysis"] = analyze_bottlenecks(report)

        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"Saved report -> {args.out}")


if __name__ == "__main__":
    main()
