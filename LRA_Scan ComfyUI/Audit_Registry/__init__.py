from .startup_registry_check import check_registry

from .LRA_Shield import validate_lora_integrity
import sys

try:
    validate_lora_integrity()  # keine Argumente hier!
except Exception as e:
    print(f"[LRA Shield] Fehler bei Prüfung: {e}")
    print("ComfyUI wird beendet.")
    sys.exit(1)