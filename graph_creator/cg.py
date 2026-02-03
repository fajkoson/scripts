import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def parse_duration_to_seconds(s: str) -> float:
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
      - dataset filename: 'dataset01.csv'  -> resolves to <script_dir>/datasets/dataset01.csv
      - relative/absolute path: 'datasets/dataset01.csv' or 'C:\\...\\dataset01.csv'
    """
    p = Path(arg)

    # If absolute path, just use it.
    if p.is_absolute():
        return p

    script_dir = Path(__file__).resolve().parent

    # If user already included 'datasets/...' keep it relative to script dir.
    candidate = (script_dir / p).resolve()
    if candidate.exists():
        return candidate

    # Otherwise assume filename should be in script_dir/datasets/
    candidate = (script_dir / "datasets" / p).resolve()
    return candidate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_file", help="Dataset filename (e.g. dataset01.csv) or a path")
    args = ap.parse_args()

    csv_path = resolve_dataset_path(args.csv_file)

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    rows = load_dataset(csv_path)

    threads = [r[0] for r in rows]
    times_s = [r[2] for r in rows]

    t1 = times_s[0]
    speedup = [t1 / t for t in times_s]
    efficiency_percent = [(s / n) * 100.0 for s, n in zip(speedup, threads)]

    print("threads,duration,seconds,speedup,perf_percent,efficiency_percent")
    for (t, d, sec), sp, ef in zip(rows, speedup, efficiency_percent):
        print(f"{t},{d},{sec:.2f},{sp:.4f},{sp*100.0:.1f},{ef:.1f}")

    title_base = csv_path.stem

    plt.figure()
    plt.plot(threads, times_s, marker="o")
    plt.xlabel("Threads")
    plt.ylabel("Build time (seconds)")
    plt.title(f"Build time vs Threads")
    plt.grid(True, linewidth=0.5)

    plt.figure()
    plt.plot(threads, speedup, marker="o", label="Measured speedup")
    plt.plot(threads, threads, linestyle="--", label="Ideal speedup (linear)")
    plt.xlabel("Threads")
    plt.ylabel("Speedup (T1 / Tn)")
    plt.title(f"Speedup vs Threads")
    plt.grid(True, linewidth=0.5)
    plt.legend()

    plt.figure()
    plt.plot(threads, efficiency_percent, marker="o")
    plt.xlabel("Threads")
    plt.ylabel("Efficiency (%)")
    plt.title(f"Parallel efficiency vs Threads")
    plt.grid(True, linewidth=0.5)

    plt.show()


if __name__ == "__main__":
    main()
