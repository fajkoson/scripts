import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def parse_duration_to_seconds(s: str) -> float:
    """
    Parses 'HH:MM:SS.xx' into seconds (float).
    Example: '00:16:33.24'
    """
    s = s.strip()
    parts = s.split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid duration '{s}'. Expected HH:MM:SS.xx")

    hh = int(parts[0])
    mm = int(parts[1])

    sec_part = parts[2]
    if "." in sec_part:
        ss_str, frac_str = sec_part.split(".", 1)
        ss = int(ss_str)
        frac = float("0." + frac_str)
    else:
        ss = int(sec_part)
        frac = 0.0

    return hh * 3600.0 + mm * 60.0 + ss + frac


def load_dataset(csv_path: Path):
    rows = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")

        expected = {"threads", "duration"}
        missing = expected - set(reader.fieldnames)
        if missing:
            raise ValueError(f"CSV missing columns: {sorted(missing)}. Expected: {sorted(expected)}")

        for line in reader:
            t = int(line["threads"])
            d = line["duration"]
            sec = parse_duration_to_seconds(d)
            rows.append((t, d, sec))

    rows.sort(key=lambda x: x[0])
    if not rows or rows[0][0] != 1:
        raise ValueError("Dataset must include baseline row with threads=1.")

    return rows


def resolve_dataset_path(arg: str) -> Path:
    """
    Accepts either:
      - dataset filename: 'dataset01.csv' -> resolves to <script_dir>/datasets/dataset01.csv
      - relative/absolute path: 'datasets/dataset01.csv' or 'C:\\...\\dataset01.csv'
    """
    p = Path(arg)

    # Absolute path: use as-is.
    if p.is_absolute():
        return p

    script_dir = Path(__file__).resolve().parent

    # If user already passed a relative path that exists relative to script dir, use it.
    candidate = (script_dir / p).resolve()
    if candidate.exists():
        return candidate

    # Otherwise assume filename lives in script_dir/datasets/
    return (script_dir / "datasets" / p).resolve()


def prepare_output_dir(csv_path: Path) -> Path:
    """
    Creates (if needed) and returns:
      <script_dir>/out/results/<dataset_name>/
    Mandatory checks:
      - create attempt
      - ensure path exists
      - ensure it's a directory
    """
    script_dir = Path(__file__).resolve().parent
    dataset_name = csv_path.stem
    out_dir = script_dir / "out" / "results" / dataset_name

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create output directory: {out_dir}") from e

    # Mandatory checks before writing results
    if not out_dir.exists():
        raise RuntimeError(f"Output directory does not exist after creation attempt: {out_dir}")
    if not out_dir.is_dir():
        raise RuntimeError(f"Output path exists but is NOT a directory: {out_dir}")

    return out_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_file", help="Dataset filename (e.g. dataset01.csv) or a path")
    ap.add_argument("--show", action="store_true", help="Show plots interactively (also saves PNGs)")
    args = ap.parse_args()

    csv_path = resolve_dataset_path(args.csv_file)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    rows = load_dataset(csv_path)

    threads = [r[0] for r in rows]
    times_s = [r[2] for r in rows]

    t1 = times_s[0]
    speedup = [t1 / t for t in times_s]  # T1/Tn
    efficiency_percent = [(s / n) * 100.0 for s, n in zip(speedup, threads)]

    # Prepare output directory (mandatory checks happen inside)
    out_dir = prepare_output_dir(csv_path)

    # Console summary
    print("threads,duration,seconds,speedup,perf_percent,efficiency_percent")
    for (t, d, sec), sp, ef in zip(rows, speedup, efficiency_percent):
        print(f"{t},{d},{sec:.2f},{sp:.4f},{sp*100.0:.1f},{ef:.1f}")

    # ---- Plot 1: Time vs Threads ----
    plt.figure()
    plt.plot(threads, times_s, marker="o")
    plt.xlabel("Threads")
    plt.ylabel("Build time (seconds)")
    plt.title("Build time vs Threads")
    plt.grid(True, linewidth=0.5)
    plt.savefig(out_dir / "build_time_vs_threads.png", dpi=150, bbox_inches="tight")

    # ---- Plot 2: Speedup vs Threads (with ideal) ----
    plt.figure()
    plt.plot(threads, speedup, marker="o", label="Measured speedup")
    plt.plot(threads, threads, linestyle="--", label="Ideal speedup (linear)")
    plt.xlabel("Threads")
    plt.ylabel("Speedup (T1 / Tn)")
    plt.title("Speedup vs Threads")
    plt.grid(True, linewidth=0.5)
    plt.legend()
    plt.savefig(out_dir / "speedup_vs_threads.png", dpi=150, bbox_inches="tight")

    # ---- Plot 3: Efficiency vs Threads ----
    plt.figure()
    plt.plot(threads, efficiency_percent, marker="o")
    plt.xlabel("Threads")
    plt.ylabel("Efficiency (%)")
    plt.title("Parallel efficiency vs Threads")
    plt.grid(True, linewidth=0.5)
    plt.savefig(out_dir / "efficiency_vs_threads.png", dpi=150, bbox_inches="tight")

    # Close figures unless user explicitly wants GUI windows
    if args.show:
        plt.show()
    else:
        plt.close("all")

    print(f"Results written to: {out_dir}")


if __name__ == "__main__":
    main()
