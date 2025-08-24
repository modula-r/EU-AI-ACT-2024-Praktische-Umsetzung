# Sicherheitshinweise

Dieses Repository enthält Audit-Komponenten für KI-Workflows, die vertrauliche Daten enthalten können.

## Kryptographische Standards
- AES-256-GCM zur Verschlüsselung
- SHA-256 für Hash-Bildung der Audit-Kette
- IV-Handling: pro Logeintrag einzigartig
- Key-Rotation über `tools/key_rotate.py`

## Offenlegung von Sicherheitslücken
Sicherheitslücken bitte ausschließlich über private Kanäle melden.  
E-Mail: security@modula-r.com  
PGP-Key: [optional einfügen wenn bekannt]

## Haftungsausschluss
Die Software dient als technische Unterstützung.  
Für rechtskonforme Gesamtprozesse ist eine ergänzende organisatorische und juristische Prüfung erforderlich.
