#!/usr/bin/env python3
"""Read-only snapshot of a MAIANA transponder over its serial console.

Sends only query commands (sys?, station?, tx?, otp?, xotrim?), never a
command that writes configuration, transmits or reboots. Logs everything
the board says, plus a short capture of its normal NMEA output, to a
timestamped file.

Usage: readout.py /dev/ttyUSB0 [--listen SECONDS] [--out DIR]
"""
import argparse
import datetime
import os
import sys
import time

import serial

BAUD = 38400
# Queries only. Do not add anything here that changes the board.
QUERIES = ["sys?", "station?", "tx?", "otp?", "xotrim?"]


def read_for(port, seconds):
    end = time.monotonic() + seconds
    chunks = []
    while time.monotonic() < end:
        data = port.read(port.in_waiting or 1)
        if data:
            chunks.append(data)
    return b"".join(chunks).decode("ascii", errors="replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("device")
    ap.add_argument("--listen", type=float, default=15.0,
                    help="seconds of normal NMEA output to capture (default 15)")
    ap.add_argument("--out", default=".", help="directory for the log file")
    args = ap.parse_args()

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(args.out, f"maiana-readout-{stamp}.log")

    with serial.Serial(args.device, BAUD, timeout=0.2) as port, \
            open(path, "w") as log:
        def emit(text):
            sys.stdout.write(text)
            log.write(text)
            log.flush()

        emit(f"# MAIANA readout {stamp} on {args.device} at {BAUD} 8N1\n")
        emit("# --- idle output ---\n")
        emit(read_for(port, args.listen))

        for q in QUERIES:
            emit(f"\n# --- {q} ---\n")
            port.reset_input_buffer()
            port.write((q + "\r\n").encode("ascii"))
            port.flush()
            emit(read_for(port, 2.0))

        emit(f"\n# done; saved to {path}\n")


if __name__ == "__main__":
    main()
