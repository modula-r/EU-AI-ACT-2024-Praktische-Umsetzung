# Compliance-Matrix (EU AI Act 2024/1689)

| Vorgabe                               | Artikel       | Umsetzung im Repository |
|---------------------------------------|--------------:|-------------------------|
| Kennzeichnung KI-generierter Inhalte  | Art. 50       | `MetaWatermarkNode` schreibt `ai_generated: true` + Tool-Version, Hash, Zeitstempel in PNG/JPEG-Metadaten |
| Nachvollziehbare Log-Aufzeichnung     | Art. 50 / 53  | Verkettete JSON-Logs (`logs/audit.jsonl.enc`) mit AES-256-GCM Verschlüsselung, Hash-Kette (prev_hash) |
| Technische Dokumentation (GPAI)       | Art. 53       | README, Compliance-Matrix, Validierungs-Tool, Node-Dokumentation |
| Übergangsfristen beachten             | Art. 113      | Timeline im README mit 2025-2026-Stufenplan |
| Manipulationsschutz                   | –             | Hash-Chain-Verifizierung + AES-GCM (Key-Rotation) |
