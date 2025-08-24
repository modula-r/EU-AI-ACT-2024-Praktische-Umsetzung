import argparse
import json
import hashlib
from PIL import Image, PngImagePlugin
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def read_metadata(image_path):
    img = Image.open(image_path)
    meta = img.info
    return meta

def verify_hash_chain(log_path, key):
    aesgcm = AESGCM(key)
    with open(log_path, "rb") as f:
        lines = f.read().splitlines()
    prev_hash = None
    for line in lines:
        nonce, ciphertext, tag = line[:12], line[12:-16], line[-16:]
        data = aesgcm.decrypt(nonce, ciphertext + tag, None)
        entry = json.loads(data)
        entry_hash = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        if prev_hash and entry["prev_hash"] != prev_hash:
            raise RuntimeError(f"Hash chain broken at {entry['timestamp']}")
        prev_hash = entry_hash
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Validator")
    parser.add_argument("--image", help="Pfad zu PNG/JPEG", required=True)
    parser.add_argument("--log", help="Pfad zu verschlüsseltem Log", required=True)
    parser.add_argument("--key", help="AES-GCM Key (hex)", required=True)
    args = parser.parse_args()

    print("[*] Prüfe Bild-Metadaten …")
    meta = read_metadata(args.image)
    print(json.dumps(meta, indent=2))

    print("[*] Prüfe Hash-Kette im Log …")
    if verify_hash_chain(args.log, bytes.fromhex(args.key)):
        print("[OK] Hash-Kette vollständig und konsistent.")
