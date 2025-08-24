import os
import json
from datetime import datetime

def scan_lora_folder(lora_dir):
    files_info = []
    total_size = 0
    file_count = 0

    for root, _, files in os.walk(lora_dir):
        for file in sorted(files):
            if file.endswith(".safetensors"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, lora_dir)
                size = os.path.getsize(full_path)

                files_info.append({
                    "filename": file,
                    "relative_path": rel_path.replace("\\", "/"),  # UNIX-kompatibel
                    "size": size
                })
                total_size += size
                file_count += 1

    return file_count, total_size, files_info

def write_new_registry_entry(log_file_path, file_count, total_size, files_info):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "file_count": file_count,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "files": files_info
    }

    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, indent=2))

    print(f"[Re_Read_LRA] Neue Registry gespeichert mit {file_count} Dateien, {entry['total_size_mb']} MB")

def main():
    base_path = r".\ComfyUI_windows_portable\ComfyUI" #Pfad anpassen!
    lora_dir = os.path.join(base_path, "models", "loras")
    log_file = os.path.join(base_path, "auditlogs", "LRA_Shield", "Registry_.log")

    if not os.path.exists(lora_dir):
        print("[Re_Read_LRA] Fehler: LoRA-Verzeichnis nicht gefunden.")
        return

    file_count, total_size, files_info = scan_lora_folder(lora_dir)
    write_new_registry_entry(log_file, file_count, total_size, files_info)

if __name__ == "__main__":
    main()
