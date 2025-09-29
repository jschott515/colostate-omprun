"""Speedup Plotting Tool
"""
import argparse
import csv
import matplotlib.pyplot
import os
import pathlib
import sys
import typing


DEFAULT_OUT = "figures"


def load_csv(file: str) -> typing.Sequence[float]:
    threads = []
    times = []

    with open(file, 'r') as f:
        reader = csv.DictReader(line for line in f if not line.strip().startswith('#'))
        for row in reader:
            threads.append(int(row['Threads']))
            times.append(float(row['Time']))
    expected_threads = list(range(1, len(times) + 1))
    if threads != expected_threads:
        raise ValueError("Unexpected data format!")
    return times


def splot(file_name: str, data: typing.Sequence[float], sequential_time: float | None = None) -> None:
    # Plot ideal speedup
    threads = len(data) + 1
    x = list(range(1, threads))
    matplotlib.pyplot.plot(x, x, linestyle='--', color='r', label='Ideal')

    # Calculate speedup, use single thread time if sequential time is not available
    if sequential_time is None:
        sequential_time = data[0]
    speedup = [sequential_time / value for value in data]

    matplotlib.pyplot.plot(x, speedup, color='b', label='Actual')

    matplotlib.pyplot.xlabel('Threads')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig(file_name)
    matplotlib.pyplot.clf()


def main() -> int:
    cfg = parse_args()
    output = typing.cast(pathlib.Path, cfg.out)
    os.makedirs(output, exist_ok=True)

    csv_path = typing.cast(pathlib.Path, cfg.CSV)
    if cfg.recursive:
        if cfg.sequential:
            print("WARNING - Specifiying a sequential execution time is not recommended in 'recursive' mode!")
        if csv_path.is_file():
            raise ValueError("Expected a directory when using 'recursive' mode!")
        sources = csv_path.glob('*.csv')
    else:
        if not csv_path.is_file():
            raise ValueError("Expected a file!")
        sources = [csv_path]

    for source in sources:
        data = load_csv(source.as_posix())
        file_name = output / f"{source.stem}.png"
        if file_name.exists() and not cfg.force:
            raise FileExistsError(f"{file_name.as_posix()} exists and 'force' is not set!")

        splot(file_name.as_posix(), data, cfg.sequential)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("CSV", type=pathlib.Path,
                        help="Results .csv or directory containing .csv files to load.")
    parser.add_argument("--sequential", "-s", type=float, default=None,
                        help="Sequential execution time of the program. Uses the single thread time if None.")
    parser.add_argument("--out", "-o", type=pathlib.Path, default=DEFAULT_OUT,
                        help="Output directory for plot.")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Experimental 'recursive' feature.")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Force overwrite figure if it exists.")
    cfg = parser.parse_args()
    return cfg


if __name__ == "__main__":
    sys.exit(main())
