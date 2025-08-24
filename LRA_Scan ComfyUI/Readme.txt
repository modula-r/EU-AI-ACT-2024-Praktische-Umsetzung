ComfyUI version: 0.3.51
ComfyUI frontend version: 1.25.9

****

🛠️ Diese Readme ist für die praktische Anwendung zur Erstellung eines LRA-Shild, welches die eingefügten LoRA-Modelle/Workflows
erfasst und dokumentiert. So kann sichergestellt werden, das keine anderen als die vorgesehenen Low Rank Modelle/Workflows in die produktive Umgebung einfließen können.

🔎 Werden fremdgeladene Modelle/Workflows erkannt, verhindert ComfyUI den Startbefehl, die Servererstellung wird abgebrochen.

✍️ Praktische Umsetzung

Die __init__.py aus dem Verzeichnis LRA_ShieldSet in die __init__der Custom_node [Pfad] aus Audit_Registry kopieren. (Original redundant sichern)

Re_Read_LRA.py in das Verzeichnis Audit_Registry kopieren. (Original redundant sichern)

Comfy ausführen - Konsole debugged erfolgreiches aktualisieren und silent Start.

Original- __init__ wieder herstellen und Re_Read_LRA.py aus Verzeichnis entfernen.

Relaunch ComfyUI - die Initialisierung muss dann erfolgreich sein und ComfyUI startet typisch.

****

Den Ordner LRA_Shieldtest in das Verzeichnis /custom_nodes/ einfügen. Vor dem ersten Start die Erfassungsroutine mit den oben gezeigten Verfahren durchführen. 

- Logfile(include.json)prüfen.
- __init__ und Re_Read_LRA.py austauschen. 
- ComfyUI starten.

Bei Missmatch Vorgang wiederholen. Sicherstellen, das die richtigen Dateien zur Anmeldung eingefügt wurden.

Lizenz: GNU General Public License v3.0 / Version 3, 29 June 2007

Opensource ✅: Technischer Support eingeschränkt.