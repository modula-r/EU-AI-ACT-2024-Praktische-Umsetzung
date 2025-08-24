#!/usr/bin/env python3
"""
Audit Validator (EU AI Act support) – v1.0.0

- Verifiziert verschlüsselte, verkettete Audit-Logs (AES-256-GCM, pro Zeile ein Datensatz)
- Prüft Hash-Kette (prev_hash) und Eintrag-Hashes (audit_hash)
- Optional: Bild-Metadaten (PNG/JPEG) auslesen und mit Log abgleichen
- Gibt CLI-Ausgabe und optional einen JSON-Report
- Exit-Codes: 0=OK, 1=Warnungen, 2=Fehler
"""
import argparse
import base64
import json
import sys
import os
import hashlib
from typing import List, Dict, Any, Tuple, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image, PngImagePlugin, ExifTags

# ---------- Helpers ----------

def _canonical_json(obj: Dict[str, Any]) -> bytes:
    """Return canonical JSON bytes (stable keys, no spaces)."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')

def _strip_audit_fields(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy without 'audit_hash' field for hashing."""
    e = dict(entry)
    e.pop('audit_hash', None)
    return e

def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_key(key_arg: str) -> bytes:
    """Load AES key: hex string or path to file containing raw 32 bytes or hex/base64 string."""
    # Try as hex directly
    ka = key_arg.strip()
    try:
        if all(c in '0123456789abcdefABCDEF' for c in ka) and len(ka) in (64, 32):
            # 64 hex chars = 32 bytes; 32 hex chars = 16 bytes (but we need 32 bytes)
            key = bytes.fromhex(ka)
            if len(key) not in (16, 24, 32):
                raise ValueError("Unsupported AES key length")
            return key
    except Exception:
        pass
    # Try as path
    if os.path.isfile(key_arg):
        with open(key_arg, 'rb') as f:
            raw = f.read().strip()
        # Try raw 32 bytes
        if len(raw) in (16, 24, 32):
            return raw
        # Try hex
        try:
            key = bytes.fromhex(raw.decode('ascii'))
            if len(key) in (16, 24, 32):
                return key
        except Exception:
            pass
        # Try base64
        try:
            key = base64.b64decode(raw, validate=True)
            if len(key) in (16, 24, 32):
                return key
        except Exception:
            pass
        raise ValueError("Could not parse key file (expected 16/24/32 raw bytes or hex/base64)")
    raise ValueError("Key must be 32-byte AES key provided as hex or path to key file.")

def decrypt_line_b64(line_b64: str, key: bytes) -> Dict[str, Any]:
    """Decrypt a single base64 line: [nonce(12) | ciphertext | tag(16)] -> JSON dict"""
    blob = base64.b64decode(line_b64.strip())
    if len(blob) < 12 + 16:
        raise ValueError("Encrypted line too short")
    nonce = blob[:12]
    ct_tag = blob[12:]
    aes = AESGCM(key)
    data = aes.decrypt(nonce, ct_tag, None)  # ct_tag = ciphertext+tag
    return json.loads(data.decode('utf-8'))

def read_log_entries_b64(path: str, key: bytes) -> List[Dict[str, Any]]:
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                entries.append(decrypt_line_b64(s, key))
            except Exception as e:
                raise RuntimeError(f"Failed to decrypt line {i}: {e}")
    return entries

def verify_chain(entries: List[Dict[str, Any]]) -> Tuple[bool, List[str], Optional[str]]:
    """
    Verify prev_hash chain and per-entry audit_hash (SHA-256 over entry without audit_hash).
    Returns: (ok, warnings, last_hash)
    """
    warnings = []
    last_hash = None
    ok = True
    for idx, e in enumerate(entries):
        # Verify entry hash
        calc_hash = _sha256_hex(_canonical_json(_strip_audit_fields(e)))
        if 'audit_hash' not in e:
            ok = False
            warnings.append(f"Entry {idx}: missing 'audit_hash'.")
        elif e['audit_hash'] != calc_hash:
            ok = False
            warnings.append(f"Entry {idx}: audit_hash mismatch (expected {calc_hash}, got {e['audit_hash']}).")
        # Verify chain
        expected_prev = last_hash
        got_prev = e.get('prev_hash')
        if idx == 0:
            if got_prev not in (None, "", "null"):
                warnings.append(f"Entry 0: prev_hash should be null/empty; got {got_prev!r}.")
        else:
            if got_prev != expected_prev:
                ok = False
                warnings.append(f"Entry {idx}: prev_hash mismatch (expected {expected_prev}, got {got_prev}).")
        last_hash = calc_hash
    return ok, warnings, last_hash

def read_image_metadata(path: str) -> Dict[str, Any]:
    """Extract minimal metadata from PNG or JPEG for audit fields."""
    img = Image.open(path)
    meta = {}
    # PNG key/value
    if isinstance(img.info, dict):
        for k, v in img.info.items():
            # Only include string-like values for report cleanliness
            if isinstance(v, (str, int, float)):
                meta[str(k)] = v if isinstance(v, str) else str(v)
    # JPEG EXIF
    try:
        exif = img.getexif()
        if exif:
            rev = {ExifTags.TAGS.get(k, str(k)): exif.get(k) for k in exif.keys()}
            # Common fields to surface
            for key in ('UserComment', 'ImageDescription', 'XPComment'):
                if key in rev:
                    val = rev[key]
                    if isinstance(val, bytes):
                        try:
                            val = val.decode('utf-8', errors='ignore')
                        except Exception:
                            val = str(val)
                    meta[key] = val
    except Exception:
        pass
    return meta

def compare_metadata_with_log(meta: Dict[str, Any], last_hash: Optional[str]) -> Tuple[bool, List[str]]:
    """
    Compare ai_generated flag and audit_hash in image with the last log hash.
    Accepts keys: 'ai_generated', 'audit_hash' (PNG text chunks) or EXIF UserComment containing JSON.
    """
    ok = True
    notes = []
    ai_flag = None
    img_hash = None

    # Direct keys from PNG text chunks
    if 'ai_generated' in meta:
        ai_flag = str(meta['ai_generated']).strip().lower()
    if 'audit_hash' in meta:
        img_hash = str(meta['audit_hash']).strip()

    # Try parse EXIF UserComment JSON if present
    uc = meta.get('UserComment')
    if uc and (not ai_flag or not img_hash):
        try:
            obj = json.loads(str(uc))
            ai_flag = ai_flag or str(obj.get('ai_generated', '')).lower()
            img_hash = img_hash or obj.get('audit_hash')
        except Exception:
            # ignore parse failure
            pass

    if ai_flag not in ('true', '1', 'yes'):
        ok = False
        notes.append("Image metadata 'ai_generated' not set to true.")
    if last_hash and img_hash and img_hash != last_hash:
        ok = False
        notes.append(f"Image audit_hash mismatch (expected {last_hash}, got {img_hash}).")
    elif last_hash and not img_hash:
        notes.append("Image missing 'audit_hash' metadata (informational).")
        # don't mark as fatal; some pipelines add it only to logs
    return ok, notes

# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="Audit Validator (EU AI Act support)")
    ap.add_argument("--log", help="Pfad zu verschlüsseltem JSONL-Log (base64 pro Zeile)")
    ap.add_argument("--key", help="AES Key (hex) oder Pfad zur Key-Datei")
    ap.add_argument("--image", help="Pfad zu PNG/JPEG mit Audit-Metadaten", default=None)
    ap.add_argument("--json", help="Schreibe JSON-Report in Datei", default=None)
    ap.add_argument("--strict", action="store_true", help="Strenger Modus: Metadaten-Mismatches als Fehler behandeln")
    ap.add_argument("--testvector", help="Pfad zu Testvektor-JSON (unverschlüsselt, Liste von Einträgen)")
    args = ap.parse_args()

    report: Dict[str, Any] = {
        "version": "1.0.0",
        "ok": True,
        "warnings": [],
        "errors": [],
        "summary": {},
    }
    exit_code = 0

    entries: List[Dict[str, Any]] = []
    last_hash: Optional[str] = None

    try:
        if args.testvector:
            # Test mode: load plain JSON list
            with open(args.testvector, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                # also allow single entry or object with "entries"
                data = data.get("entries") or [data]
            if not isinstance(data, list):
                raise ValueError("Testvector must be a JSON list of entries or an object with 'entries' list.")
            entries = data
        else:
            if not args.log or not args.key:
                raise ValueError("For encrypted logs, both --log and --key are required.")
            key = load_key(args.key)
            entries = read_log_entries_b64(args.log, key)

        ok_chain, chain_notes, last_hash = verify_chain(entries)
        if not ok_chain:
            report["ok"] = False
            report["errors"].extend(chain_notes)
            exit_code = 2
        else:
            report["warnings"].extend(chain_notes)

        report["summary"]["entries"] = len(entries)
        report["summary"]["last_hash"] = last_hash

        # Image checks
        if args.image:
            try:
                meta = read_image_metadata(args.image)
                report["summary"]["image_metadata"] = {k: meta[k] for k in sorted(meta.keys()) if k in ("ai_generated","audit_hash","UserComment","ImageDescription","XPComment")}
                img_ok, img_notes = compare_metadata_with_log(meta, last_hash)
                if not img_ok and args.strict:
                    report["ok"] = False
                    report["errors"].extend(img_notes)
                    exit_code = max(exit_code, 2)
                else:
                    # treat as warnings if not strict
                    if not img_ok:
                        report["warnings"].extend(img_notes)
                        exit_code = max(exit_code, 1)
            except Exception as e:
                report["warnings"].append(f"Image metadata read failed: {e}")
                exit_code = max(exit_code, 1)

    except Exception as e:
        report["ok"] = False
        report["errors"].append(str(e))
        exit_code = 2

    # Human output
    status = "OK" if report["ok"] else "FAILED"
    print(f"[{status}] Entries: {report['summary'].get('entries', 0)}")
    if "last_hash" in report["summary"]:
        print(f"Last hash: {report['summary']['last_hash']}")
    if report["warnings"]:
        print("\nWarnings:")
        for w in report["warnings"]:
            print(f" - {w}")
    if report["errors"]:
        print("\nErrors:")
        for e in report["errors"]:
            print(f" - {e}")

    # JSON report
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n[+] JSON-Report geschrieben: {args.json}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
