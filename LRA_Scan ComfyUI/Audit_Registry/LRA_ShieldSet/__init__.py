import os
import sys
import subprocess
from .startup_registry_check import check_registry
from .LRA_Shield import validate_lora_integrity

# Manuell auslösbare Re_Read_LRA-Funktion (nur wenn vorhanden)
re_read_script = os.path.join(os.path.dirname(__file__), "Re_Read_LRA.py")
if os.path.isfile(re_read_script):
    print("[LRA Shield] Re_Read_LRA.py gefunden. Aktualisiere Registry_.log...")
    result = subprocess.run([sys.executable, re_read_script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("[LRA Shield] Fehler beim Ausführen von Re_Read_LRA.py.")
        print(result.stderr)
        sys.exit(1)

# Danach reguläre Validierung
try:
    validate_lora_integrity()
except Exception as e:
    print(f"[LRA Shield] Fehler bei Prüfung: {e}")
    print("ComfyUI wird beendet.")
    sys.exit(1)
