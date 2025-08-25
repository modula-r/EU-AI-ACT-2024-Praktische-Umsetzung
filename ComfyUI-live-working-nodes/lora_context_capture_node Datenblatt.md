## 📄 Funktionsdatenblatt


## 🔧 Node: LoRAContextCaptureNode

Version: 1.0

Entwickler: modula-r.com

Lizenz: proprietär (projektgebunden)

Kategorie: 🛡 Audit Tools

Zweck: Erfassung, Verschlüsselung und Auditierung der zur Inferenz verwendeten LoRA-Dateien in ComfyUI-Pipelines gemäß AI Act Art. 53–55 und DSGVO (TOM-konform).

## 1. 🔍 Zweck der Node

Die LoRAContextCaptureNode erfasst zur Laufzeit alle bei der Inferenz verwendeten LoRA-Dateien (.safetensors) sowie das Hauptmodell, verschlüsselt diese Informationen manipulationssicher und speichert sie als chronologisch gehashte Logeinträge. Diese Einträge dienen der Rückverfolgbarkeit, Integritätsprüfung und Auditierung generativer KI-Ausgaben gemäß den Anforderungen des AI Acts.

## 2. 📥 Eingaben
Parameter  Typ	Beschreibung

model	ModelPatcher	Das für die Inferenz geladene Modell (z. B. SDXL). Wird zur Durchschleifung genutzt, bleibt unverändert.

model_filename	str	Dateiname des verwendeten Modells zur protokollarischen Erfassung.

lora_filename	str	Kommagetrennte Liste aller verwendeten LoRA-Dateien, z. B. "lora1.safetensors,lora2.safetensors".


## 3. 🛠️ Verarbeitungsschritte
Initialisierung:

Prüft Existenz des Verzeichnisses auditlogs/SDXL/.

Prüft oder erzeugt die Datei lora_context_log.log.

Schlüsselbereitstellung:

AES-256 Schlüssel wird aus lokal festgelegtem Passwort + Salt generiert (PBKDF2HMAC).

Dieser Schlüssel dient der Verschlüsselung der Logeinträge.

Loghistorie (optional):

Letzter verschlüsselter Logeintrag wird ausgelesen, entschlüsselt und gehasht.

Falls unlesbar oder fehlerhaft: setzt prev_hash auf "CORRUPTED".

Datensatz-Erstellung:

Erzeugt ein neues Logobjekt:

{

  "timestamp": "...",
  
  "model": "...",
  
  "lora_used": [...],
  
  "prev_hash": "..."
  
}


Jedes lora_used-Element enthält file (Name) und weight (unknown oder "none").

Hashkette:

Vor dem finalen Hash wird ein pre_hash des Datenobjekts erzeugt (SHA512).

Der finale hash beinhaltet auch den pre_hash zur Konsistenzprüfung.

Verschlüsselung:

Kompletter JSON-Datensatz wird AES-CBC verschlüsselt und Base64-codiert.

Protokollierung:

Die verschlüsselte Base64-Zeile wird an die Logdatei angehängt.

## 4. 🔐 Sicherheitsmerkmale

Feature	Status	Beschreibung

AES-256 CBC Verschlüsselung	✅	Sichere symmetrische Verschlüsselung, IV generiert pro Eintrag.

PBKDF2HMAC Key Derivation	✅	Starkes Passwort-Derivation-Verfahren mit festem Salt.

Base64-Kodierung	✅	Ermöglicht Speicherung als reine Textzeile im Audit-Log.

Hashkette mit prev_hash	✅	Lückenlose Chronologie und Manipulationssicherung.

Fehlerresistenz bei Loglesefehlern	✅	Defekte Logzeilen werden mit "CORRUPTED" markiert, System bleibt stabil.


## 5. 📤 Ausgabe
Parameter	Typ	Beschreibung

model	ModelPatcher	Unverändert zurückgegeben, zur Weiterverwendung im Workflow.

status	str	Rückmeldung der Node, z. B. "✅ LoRA usage logged successfully." oder Fehlerhinweis.


## 6. 📁 Beispiel-Logeintrag (nach Entschlüsselung)


{

  "timestamp": "2025-07-16 12:34:56",
  
  "model": "sdxl_custom_053.safetensors",
  
  "lora_used": [
  
    {"file": "portrait_sharp.safetensors", "weight": "unknown"},
	
    {"file": "none", "weight": "0.0"}
	
  ],
  
  "prev_hash": "af3c2d....",
  
  "pre_hash": "e4b9c8....",
  
  "hash": "a73e49...."
  
}


## 7. 📜 Audit-Fähigkeit

Die Node erfüllt folgende rechtliche Vorgaben:

Rechtsnorm	Erfüllung	Beschreibung

AI Act Art. 53 (Transparenzpflicht)	✅	Alle LoRA-Komponenten werden eindeutig dokumentiert.

AI Act Art. 54 (Logpflicht für Basis-/LoRA-Modelle)	✅	Modell- und LoRA-Verwendung wird chronologisch geloggt.

DSGVO Art. 32 (Integrität/Vertraulichkeit)	✅	Manipulationssichere Logs mit AES-Verschlüsselung und Hashchain.

TOM-konform nach ISO/IEC 27001	✅	Lokal verschlüsselte Speicherung, keine externen Abhängigkeiten.


## 8. 🧩 Erweiterungspotenzial (optional)

Idee	Nutzen

SHA256-Hash jeder LoRA-Datei erfassen	Für tiefergehende Forensik & Modellprüfung

LoRA-Metadaten aus safetensors extrahieren	Validierung z. B. auf NSFW- oder Lizenzmarker

Logrotation oder Archivierung	Langfristige Audithaltung ohne Logwachstum


## ✅ Zusammenfassung

Die LoRAContextCaptureNode bietet ein robustes, manipulationssicheres Framework zur Auditierung von LoRA-Einsätzen in ComfyUI. Sie erfüllt alle aktuellen Vorgaben des AI Act 2024 und dokumentiert Modellverwendung transparent, nachvollziehbar und technisch zuverlässig.
