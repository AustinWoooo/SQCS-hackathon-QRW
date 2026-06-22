"""Command-line interface for reproducible 1D walk comparisons."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .core import classical_distribution, quantum_distribution


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--start", type=int)
    parser.add_argument("--output", type=Path, default=Path("results/qrw_1d.csv"))
    parser.add_argument("--plot", type=Path)
    args = parser.parse_args()

    quantum = quantum_distribution(size=args.size, steps=args.steps, start=args.start)
    classical = classical_distribution(size=args.size, steps=args.steps, start=args.start)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["position", "quantum_probability", "classical_probability"])
        writer.writerows((index, quantum[index], classical[index]) for index in range(args.size))

    if args.plot:
        import matplotlib.pyplot as plt

        args.plot.parent.mkdir(parents=True, exist_ok=True)
        x = list(range(args.size))
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.bar(x, classical, color="#9aa0a6", alpha=0.55, label="classical")
        ax.plot(x, quantum, "o-", color="#0057b8", linewidth=1.7, label="quantum")
        ax.set(xlabel="position", ylabel="probability", title=f"1D walk after {args.steps} steps")
        ax.grid(axis="y", alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(args.plot, dpi=180)

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

