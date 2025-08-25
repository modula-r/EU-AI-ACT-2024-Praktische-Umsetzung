## 🛡 Funktionsdatenblatt

Komponente: MetaWatermarkNode

Version: 1.0

Entwickler: modula-r (interne Eigenentwicklung)

Lizenz: proprietär (projektgebunden)

Kategorie: Audit Tools

Einsatzbereich: DSGVO-/AI-ACT-konforme Bildkennzeichnung

Status: Stable

Letzte Änderung: 2025-07-16


## 🛡1. Funktionsübersicht

Die MetaWatermarkNode ist eine spezielle ComfyUI-Node zur Einbettung von maschinenlesbaren Metadaten in generierte Bilder. Sie ermöglicht eine nachweisbare, nicht-visuelle Kennzeichnung von AI-generierten Medieninhalten gemäß Artikel 52, 53 und 54 des AI Act 2024 sowie § 9 DSGVO.

Ziel ist die eindeutige Kennzeichnung, Herkunftsnachverfolgbarkeit und Auditierung von Bildausgaben in AI-basierten Generierungssystemen.


## 🛡2. Eingabestruktur

INPUT_TYPES = {

  "required": {
  
    "image": ("IMAGE",),  # Tensor-Format: [1,3,H,W]
	
    "model_name": ("STRING", default="qwen-image"),
	
    "tool_or_provider": ("STRING", default="ComfyUI Revision..."),
	
    "purpose_description": ("STRING", default="KI-Bildgenerierung"),
	
    "user_identifier": ("STRING", default="Customer-project"),
	
    "audit_hash": ("STRING", default="auto"),
	
    "format": (["PNG", "JPEG"],),
	
  }
  
}
## 🛡3. Ausgabe

RETURN_TYPES = ("IMAGE",)

Gibt ein Bild im identischen Tensorformat zurück, das nun dauerhaft die eingebetteten AI-ACT-Metadaten enthält.

Rückgabeformat: [1, 3, H, W]

## 4. Funktionalität im Detail

🔁 Konvertierung

Eingabe-Bild: torch.Tensor → PIL.Image

Nach Metadaten-Embedding: PIL.Image → torch.Tensor


🧩 Metadatenstruktur (JSON)


{

  "ai_generated": "true",
  
  "model_name": "qwen-image.safetensors",
  
  "tool_or_provider": "ComfyUI Revision: ...",
  
  "generation_timestamp": "UTC-Timestamp (ISO 8601)",
  
  "purpose_description": "KI-Bildgenerierung",
  
  "user_identifier": "Customer-project",
  
  "audit_hash": "SHA256 o.ä.",
  
  "compliance_level": "AI-Act-2024-Conform"
  
}


📦 Einbettungsmethoden

Format	Methode	Ort der Einbettung

PNG	PngInfo()	Text-Chunks (Key: AI_ACT_METADATA)

JPEG	piexif	Exif > UserComment (UTF-8 codiert)


## 🛡5. Relevanz zur AI-ACT-Compliance

Vorschrift	Umsetzung durch Node

Art. 52 Abs. 1 AI Act – Hinweis auf KI-generiert	ai_generated: true

Art. 53 Abs. 1 – Transparenz bzgl. Modell und Zweck	Felder model_name, purpose_description, tool_or_provider

Art. 54 – Dokumentationspflicht für Anbieter	Felder audit_hash, user_identifier, generation_timestamp

DSGVO – Zweckbindung & Verarbeitungsklarheit	Durch explizite Textbeschreibung im JSON



## 🛡6. Sicherheits- & Prüfmerkmale

Formatneutral: PNG + JPEG vollständig unterstützt

Maschinenlesbar: Strukturierte JSON-Einbettung

Nichtvisuell: Keine sichtbaren Artefakte im Bild

Unverfälschbarkeit: Kombinierbar mit Hashkette / AES-Verschlüsselung downstream

Prüfbar: Jederzeit auslesbar mit Standardtools (z. B. ExifTool, Pillow, CustomNode)


## 🛡7. Integrationshinweise

Kompatibel mit allen Standard-ComfyUI Bildausgaben

Empfohlen: In Kombination mit PromptModelLoggerNode, LoRAContextCaptureNode und PromptComplianceCheckerNode zur vollständigen AI-ACT-Kette

Wird effektiv am Ende der Pipeline ausgeführt – direkt vor Speicherung oder Anzeige


## 🛡8. Prüf-Signatur (Ausgabebeispiel)

INPUT_TYPES = {

  "required": {


  "ai_generated": "true",
  
  "model_name": "Fluxdev_SDv1",
  
  "tool_or_provider": "ComfyUI Revision: 3332 [a14c2fc3]",
  
  "generation_timestamp": "2025-07-16T12:45:32Z",
  
  "purpose_description": "Sachbild-Generierung im Behördenprojekt",
  
  "user_identifier": "Projekt X-07-LRA",
  
  "audit_hash": "23c8f89d8b2e13...",
  
  "compliance_level": "AI-Act-2024-Conform"
  
  }

}

## 🛡9. Bekannte Einschränkungen

Einschränkung	Beschreibung

Dateigröße	Leichte Vergrößerung durch Metadaten (~1–5 KB)

JPEG-Limitierung	Exif-Kommentare können von einigen Programmen ignoriert werden

Kein Schutz vor absichtlicher Entfernung der Metadaten – nur kombinierbar mit kryptografischem Nachweis	


## 🛡10. Weiterentwicklung geplant

AES-Verschlüsselung optional für sensiblere Kennzeichnung

Signaturhash zur Integritätsprüfung via öffentlichem Schlüssel

Versionierung der Node selbst (zur Nachvollziehbarkeit der Metadatenstruktur)
