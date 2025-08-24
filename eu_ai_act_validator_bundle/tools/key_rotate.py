#!/usr/bin/env python3
"""
Key Rotation Helper – v1.0.0
- Generiert AES-Keys (16/24/32 Bytes)
- Optional: schreibt Key in Datei (RAW bytes oder hex)
"""
import argparse, os, base64, secrets, sys

def main():
    ap = argparse.ArgumentParser(description="AES Key Generator / Rotation Helper")
    ap.add_argument("--size", type=int, default=32, choices=(16,24,32), help="Key size in bytes (default 32)")
    ap.add_argument("--hex", action="store_true", help="Print as hex instead of raw")
    ap.add_argument("--outfile", help="Write key to file")
    args = ap.parse_args()

    key = secrets.token_bytes(args.size)
    out = key.hex() if args.hex else key

    if args.outfile:
        mode = 'w' if args.hex else 'wb'
        with open(args.outfile, mode) as f:
            f.write(out)
        print(f"[+] Wrote key ({args.size} bytes) to {args.outfile}")
    else:
        if args.hex:
            print(out)
        else:
            sys.stdout.buffer.write(out)

if __name__ == "__main__":
    main()
