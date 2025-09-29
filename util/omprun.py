"""Automated testing for OpenMP programs
"""
import argparse
import csv
import datetime
import os
import re
import subprocess
import sys
import typing


DEFAULT_THREADS = (1, 8)
DEFAULT_REPS = 7
DEFAULT_REGEX = r'\b\d+\.\d+|\b\d+|\B\.\d+'
DEFAULT_OUT = 'results'


def get_thread_range(arg: typing.Sequence[int], default_base: int = 1) -> typing.Tuple[int, int]:
    arg = list(arg)
    assert len(arg) in [1, 2], "Expected [start:]stop"
    stop = arg.pop()
    start = arg.pop() if arg else default_base
    return start, stop


def get_default_mask(threads: int) -> int:
    if threads <= 8:
        return 0x00005555
    if threads <= 16:
        return 0x0000FFFF
    return 0xFFFFFFFF


def main() -> int:
    cfg = parse_args()
    os.makedirs(cfg.out, exist_ok=True)
    with open(f"{cfg.out}/omprun_{datetime.datetime.now().strftime('%m%d%Y_%H%M%S')}.csv", "w") as f:
        # Write Header
        f.write(f"# Command: `{cfg.TEST}`\n")
        if cfg.info is not None:
            f.write(f"# Brief: {cfg.info}\n")
        writer = csv.writer(f)
        writer.writerow(["Threads", "Time"])

        start, stop = cfg.threads
        for thread in range(start, stop + 1):
            times = []
            for rep in range(cfg.reps):
                # Run the test
                print(f"Threads {thread}, Rep {rep}")
                mask = get_default_mask(thread) if cfg.mask is None else cfg.mask
                cmd = f"OMP_NUM_THREADS={thread} taskset {hex(mask)} " + cfg.TEST
                test = subprocess.run(cmd, shell=True, capture_output=True)
                if test.returncode != 0:
                    raise ValueError(f"`{cmd}` exited with {test.returncode}")
                result = test.stdout.decode()
                print(result.strip())
                # Pull the result from stdout
                match = re.search(cfg.regex, result)
                if match is None:
                    raise ValueError(f"Unable to extract time from result `{result}` with regex {cfg.regex}")
                times.append(float(match.group()))
            mean_time = sum(times)/len(times)
            writer.writerow([thread, mean_time])
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("TEST", type=str,
                        help="Test command to run. Example `\"./hello_world\"`")
    parser.add_argument("--threads", type=lambda x: map(int, x.split(':')), default=DEFAULT_THREADS,
                        help="Number of threads to test, [start:]stop (i.e. `5` runs 1-5 threads, `2:3` runs 2-3 threads)")
    parser.add_argument("--reps", type=int, default=DEFAULT_REPS,
                        help="Number of reps to run per test")
    parser.add_argument("--mask", type=lambda x: int(x, 0), default=None,
                        help="Taskset Mask. Uses the ideal mask if not specified (i.e. 0x5555 for 8 threads, 0xFFFF for 16 threads, etc...)")
    parser.add_argument("--regex", type=str, default=DEFAULT_REGEX,
                        help="Regular expression to parse stdout of the TEST.")
    parser.add_argument("--out", "-o", type=str, default=DEFAULT_OUT,
                        help="Output directory for results.")
    parser.add_argument("--info", "-i", type=str, default=None,
                        help="Optional note to include in output file.")
    cfg = parser.parse_args()
    cfg.threads = get_thread_range(cfg.threads)
    return cfg


if __name__ == "__main__":
    sys.exit(main())
