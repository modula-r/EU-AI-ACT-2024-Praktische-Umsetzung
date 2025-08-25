## 🧾 Node-Datenblatt: 

🛡 PromptComplianceCheckerNode (Encrypted)


## 📌 1. Node-ID & Klassendefinition

Klassename: PromptComplianceCheckerNode

Modul: ComfyUI CustomNode

ComfyUI-Version: v 0.3.51

Version: 1.0

Entwickler: modula-r.com

Lizenz: proprietär (projektgebunden)


Node-Typ: Audit / Compliance

Displayname: 🛡 Prompt Compliance Checker (Encrypted)


## 🧠 2. Zweck der Node (Funktion & rechtlicher Rahmen)

✔️ Hauptfunktion:

Diese Node prüft generative Textprompts (positive/negative) auf definierte Verstöße gegen:

DSGVO (Erwägungsgründe 60, 71)

AI ACT (Art. 5, Art. 53, Art. 54, Art. 60)

🧾 Relevante Normen:

DSGVO Art. 32: Verarbeitungssicherheit

DSGVO TOM – Abschnitt C, D, E

AI ACT Art. 53, 54, 55, 60

KI-generierte Inhalte (Art. 60 AI-ACT): Prüfung der Inhalte auf rechtswidrige Generierung

Prompt-Transparenz (Art. 54 AI ACT): verpflichtende Prüfung auf nicht erlaubte Inhalte



## 🔄 3. Inputs & Outputs

Name	Typ	Beschreibung

positive_prompt	STRING	Prompt-Text, der visuell umgesetzt werden soll

negative_prompt	STRING	Prompt-Text, der ausgeschlossen werden soll

Rückgabe (Output):

status (STRING): "✅ OK" oder Exception mit match-Detail


## 🔐 4. Sicherheits- & Protokollierungsfunktionen

Mechanismus	Beschreibung

Blacklists	Zwei Kategorielisten: nsfw, ai_act_blocked

System-injected Negatives	Optional: automatische Promptergänzungen, von der Prüfung ausgenommen

AES-Verschlüsselung	Logeinträge werden AES-256 CBC verschlüsselt

PBKDF2 Key-Derivation	Schlüssel wird aus statischer Phrase + Salt generiert, gespeichert in .key

Hashchain-Logging	Jeder Eintrag enthält prev_hash + neuen hash (SHA512), fälschungssicher

Auditlog-Verzeichnis	./auditlogs/.../compliance_chain_log.log



## 🔬 5. Wirksamkeit & Blockierlogik

Jeder Prompt wird gegen zwei sensible Begriffskategorien geprüft (vollständig definierbar).

Treffer erzeugen eine Blockierung durch Exception (raise Exception).

Der Auditlog bleibt auch bei Blockierung vollständig nachvollziehbar.

System ist deterministisch – gleiche Eingabe erzeugt gleiche Ausgabe.

Kein Prompt kann außerhalb dieser Prüfung verwendet werden (Node als Gatekeeper eingebunden).


## 📚 6. Codeintegrität & Sicherheit

Alle Audit-Einträge sind unveränderbar, da:

jeder Eintrag seinen Vor-Hash kennt (prev_hash)

alle Inhalte verschlüsselt gespeichert sind (AES)

Logs chronologisch gesichert werden (kein Rewrite)

Backup durch manuell trennbare Partition möglich (Abschnitt H TOM)

Keine Nutzung externer APIs, Bibliotheken vollständig lokal


## 🧩 7. AI ACT-Kategorisierung

Artikel	Inhalt	Erfüllt durch

Art. 5	Verbotene Anwendungen	Über Begriffsprüfung (Blacklist ai_act_blocked)

Art. 53	Open-Source-Ausnahme	Eigenentwicklung + Auditfunktion

Art. 54	Transparenz	Inhalte & Begriffe dokumentiert, maschinenlesbar

Art. 55	Technische Dokumentation	Dieses Datenblatt + Auditlog

Art. 60	Kennzeichnung & Nachvollziehbarkeit	Vollständiger Auditlog, maschinenlesbar


## 🔏 8. Technische Integritätssignatur

{

  "node_class": "PromptComplianceCheckerNode",
  
  "hash": "6ee1df1e9b7e4c1fa7e57d2d4f2fa6f3d843d58ef45d754c6b2c2fc1dd7f64cd",
  
  "version": "1.0.0-ACT",
  
  "verified": true
  
}

## 🧾 9. Letzte Überprüfung

Datum: 2025-07-16

Prüfer: modula-r / AI-ACT Check.- V1.0

Status: ✅ Konform, keine sicherheitskritischen Schwächen erkannt
