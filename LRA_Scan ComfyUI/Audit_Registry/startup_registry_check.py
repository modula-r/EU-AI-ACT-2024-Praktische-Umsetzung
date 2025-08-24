import os
import sys
import json

WORKFLOW_ROOT = os.path.join(os.path.dirname(__file__), "../../user/default/workflows")
INCLUDE_FILE = os.path.join(os.path.dirname(__file__), "include.json")

def collect_workflow_paths(base_dir):
    wf_list = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                wf_list.append(rel_path.replace("\\", "/"))  # Normalize for Windows
    return sorted(wf_list)

def check_registry():
    if not os.path.exists(INCLUDE_FILE):
        print("[AuditRegistry] FEHLER: include.json nicht gefunden.")
        sys.exit("[AuditRegistry] Initialisierung fehlgeschlagen.")

    with open(INCLUDE_FILE, "r", encoding="utf-8") as f:
        try:
            allowed_list = sorted(json.load(f))
        except json.JSONDecodeError:
            sys.exit("[AuditRegistry] Fehlerhafte JSON-Struktur in include.json.")

    current_list = collect_workflow_paths(WORKFLOW_ROOT)

    if allowed_list != current_list:
        print("[AuditRegistry] Nicht autorisierte Workflow-Dateien erkannt:")
        print("→ Erwartet:", allowed_list)
        print("→ Gefunden :", current_list)
        sys.exit("Ihre Registrierung ist abgelaufen. Bitte wenden Sie sich an den technischen Support von modula-r.com.")

    print("[AuditRegistry]✅ Workflow-Integration validiert. System bereit.")

# Wird automatisch beim Laden des Pakets ausgeführt
check_registry()



