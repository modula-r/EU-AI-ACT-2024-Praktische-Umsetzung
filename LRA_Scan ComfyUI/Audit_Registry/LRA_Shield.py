import os
import json
import hashlib
import sys
import uuid
from datetime import datetime

def read_last_registry_entry(log_file_path):
    if not os.path.isfile(log_file_path):
        raise RuntimeError(f"LRA Shield Logdatei nicht gefunden: {log_file_path}")

    with open(log_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise RuntimeError("Registry Logdatei ist leer oder fehlerhaft.")

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Fehler beim Parsen der Registry_.log: {e}")

def check_lora_folder(lora_dir):
    if not os.path.isdir(lora_dir):
        raise RuntimeError(f"LoRA Verzeichnis nicht gefunden: {lora_dir}")

    file_count = 0
    total_size = 0
    files = []

    for root, _, filenames in os.walk(lora_dir):
        for file in sorted(filenames):
            if file.endswith(".safetensors"):
                path = os.path.join(root, file)
                file_count += 1
                total_size += os.path.getsize(path)
                files.append(f"{file}:{os.path.getsize(path)}")

    return file_count, total_size, files

def compute_hash(files: list, prev_hash: str) -> str:
    content = json.dumps({"files": files, "prev_hash": prev_hash}, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_last_check_hash(logfile_path):
    if not os.path.exists(logfile_path):
        return None
    with open(logfile_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
        if lines:
            try:
                return json.loads(lines[-1]).get("current_hash")
            except Exception:
                return None
    return None

def write_audit_log(logfile_path, entry: dict):
    with open(logfile_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def validate_lora_integrity():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    lora_dir = os.path.join(base_dir, "models", "loras")
    registry_log = os.path.join(base_dir, "auditlogs", "LRA_Shield", "Registry_.log")
    check_log = os.path.join(base_dir, "auditlogs", "LRA_Shield", "LRA_Check.log")

    last_registry = read_last_registry_entry(registry_log)
    reg_file_count = last_registry.get("file_count")
    reg_total_size = last_registry.get("total_size_bytes")

    cur_file_count, cur_total_size, filelist = check_lora_folder(lora_dir)

    # Vorheriger Hash laden
    prev_hash = get_last_check_hash(check_log) or "0" * 64
    current_hash = compute_hash(filelist, prev_hash)

    audit_entry = {
        "audit_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "file_count": cur_file_count,
        "total_size_bytes": cur_total_size,
        "current_hash": current_hash,
        "prev_hash": prev_hash,
    }

    if reg_file_count != cur_file_count or reg_total_size != cur_total_size:
        audit_entry["result"] = "error"
        audit_entry["message"] = "Mismatch with registry – possible tampering detected."
        write_audit_log(check_log, audit_entry)
        print("[LRA Shield] ❌ ERROR: LoRA-Verzeichnis stimmt NICHT mit Registry überein!")
        sys.exit(1)
    else:
        audit_entry["result"] = "success"
        audit_entry["message"] = "LoRA-Verzeichnis validiert – keine Manipulation."
        write_audit_log(check_log, audit_entry)
        print("[LRA Shield] ✅ LRA Integration geprüft. ComfyUI startet leise.")

if __name__ == "__main__":
    validate_lora_integrity()
