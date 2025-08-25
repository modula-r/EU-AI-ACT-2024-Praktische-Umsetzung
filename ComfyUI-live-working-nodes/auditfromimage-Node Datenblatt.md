## 📄 Node-Datenblatt: audit_from_image_Node

Kategorie: 🛡 Audit

Zweck: AI-ACT-/DSGVO-konforme Logging-Instanz zur Nachvollziehbarkeit von Prompts & Modellnutzung

Version: 1.0

Entwickler: modula-r.com

Lizenz: proprietär (projektgebunden)


## ✅ Zweck der Node

Diese Node dient der gesetzeskonformen Erfassung und Protokollierung der Interaktion von Nutzern mit KI-Modellen im ComfyUI-System.

Sie erfüllt im Speziellen die Anforderungen aus:

AI-ACT Artikel 53 Abs. 1 lit. b, c, d

DSGVO Artikel 5 Abs. 2 (Accountability)

DSGVO Artikel 13 & 14 (Informationspflichten)


## 🔐 Sicherheit & Integrität

# Merkmal	Beschreibung

Verschlüsselung	AES-256 CBC mit zufälligem IV pro Eintrag

Key-Handling	Speicherung im lokalen AES-Schlüssel unter superkey.key

Hash-Kette	SHA-512 Hash-Kette mit prev_hash-Verkettung

Fallback	Letzter Eintrag wird bei Fehlern als CORRUPTED gekennzeichnet


## 📥 Eingaben (INPUT_TYPES)

Parameter	Typ	Beschreibung

positive_prompt	STRING (multiline)	Nutzer-Input zur Modellerzeugung

negative_prompt	STRING (multiline)	Einschränkungen, z. B. verbotene Inhalte

model_name	STRING	Der verwendete Modellname oder Pfad (z. B. qwen-image-edit.safetensors)

## 📤 Ausgaben (RETURN_TYPES)

Name	Typ	Beschreibung

positive_out	STRING	Ursprünglicher positive_prompt

negative_out	STRING	Negativer Prompt inklusive Injektionssicherheitsliste

## 🧠 Hauptfunktionen (log())

Lade letzte Logzeile → extrahiere prev_hash für Chain

Lese systemweite Injektions-Prompts (injected_negatives.json)

Ergänze negative_prompt automatisch mit Sicherheitseinträgen

Erstelle strukturierten JSON-Eintrag mit Audit-Metadaten

Verschlüssele den Logeintrag mit AES

Schreibe den verschlüsselten Eintrag in prompt_model_log.log


## 📊 Struktur des gespeicherten Eintrags (vereinfachtes Beispiel)

{

  "timestamp": "2025-07-16T17:00:00",
  
  "positive_prompt": "A beautiful waterfall",
  
  "negative_prompt": "blood, violence",
  
  "model_filename": "qwen-image.safetensors",
  
  "training_data_rights": "Unklare Rechtebasis...",
  
  "transparency_notice": "Nutzung unter Vorbehalt...",
  
  "audit_compliance": "Erfüllt Transparenzpflicht...",
  
  "injected_negatives": ["nude", "gun"],
  
  "final_negative_prompt": "blood, violence, nude, gun",
  
  "prev_hash": "xyz",
  
  "hash": "abc123"
  
}


## 📌 Compliance & Transparenzhinweise

training_data_rights: Offen und ehrlich über das Modell – erfüllt Transparenzanforderungen des AI Act.

transparency_notice: Nutzer wird über Unsicherheiten der Trainingsdatenlage informiert.

audit_compliance: Festes Statement zur Konformität (in der Logik hartcodiert) – prüfbar im Log.

## 🏛️ Relevanz für den AI-ACT (2024)

Artikel	Relevanz	Beschreibung

Art. 53 (1b)	✔️	Dokumentation von Prompts & Nutzung

Art. 53 (1c)	✔️	Technische Nachvollziehbarkeit der Funktionsweise

Art. 53 (1d)	✔️	Nachvollziehbare Erklärung durch gespeichertes Logging

DSGVO Art. 5	✔️	Rechenschaftspflicht durch vollständige Nachvollziehbarkeit

DSGVO Art. 13/14	✔️	Informationspflicht erfüllt durch Transparenzhinweise


## ⚠️ Besondere Eigenschaften

Eingebautes "Fail-Safe"-Verhalten bei fehlerhafter Decryption (CORRUPTED)

Kein Zugriff auf Drittanbieter-APIs, rein lokal

Prompt-Erweiterung sichert gegen kritische Inhaltexpansion im Negativfeld

Keine externe Speicherung oder Analyse – rein dokumentarisch
