# DSGVO und AI-ACT relevante Prüfmechanismen - Integration V0.1
---

## Vorwort

modula-r.com (als Akteur diesen Angebotes bei Github/EU-AI-ACT-2024-Praktische-Umsetzung) kann keine juristisch verifizierte Handlungsanleitung oder
Handlungsempfehlung aussprechen oder versprechen. Die Verantwortung im Umgang mit Daten/Exponaten/Outputs/Generierungen allgemein, welche für den
Release oder das Teilen in öffentlich zugänglichen Medien bestimmt sind, unterliegen immer der Person welche sie in Umlauf bringt.

modula-r.com möchte aber technische Möglichkeiten aufzeigen, insbesondere der technischen Umsetzung, welche Prüfroutinen und Dokumentation, nach den
Dokumentationspfilchten des EU AI-Act 2024 Art. 53 KI-VO (Pflichten für Anbieter von KI Modellen mit allgemeinen Verwendungszweck), sicherstellen und
umsetzen.

---

## Generative Systeme (Stable Diffusion) und die Einhaltung der Urheberrechte und DSGVO

Das verwendete System (KI-Engine), mit welchem wir in diesem Artikel arbeiten verwendet ein sog. Open Source Model. 

Bezeichnung: qwen-image[...].safetensors

Quelle: https://huggingface.co/Qwen/Qwen-Image

Release: 04.08.2025

Hersteller: Alibaba

Lizenz: Apache2.0


Eigenschaft: .safetensors Dateiformat und somit maschinenlesbar, Gewichte können ermittelt und dokumentiert werden.

Klone: Ableitungen des Grundmodelles wie: qwen-image-edit.safetensors.../


Versionierung für AuditIntegration mit MetaHeader: qwen_image_fp8_e4m3fn_Audit_v1_signed.safetensors

(Maschinenlesbar und Log-Funktion.)


Lizenz vererbt: Apache2.0

## KI-Engine:

Bezeichnung: ComfyUI

Quelle: https://www.comfy.org/about

Version: 0.3.51

Lizenz:  GNU GENERAL PUBLIC LICENSE  Version 3, 29 June 2007

(Version ändert sich systematisch durch Updatefunktion.)

---

## Prüfroutinen und Detektion

Grundmodelle in Stable Diffusion werden mit einem sehr großen Datensatz aus Trainingsdaten erstellt. Damit ein Model umso flexibler und dynamischer generieren kann,
müssen Bilder und Captions (Bildbeschreibung in Textform) alle möglichen Inhalte aufzeigen, welche es ermöglichen semantische Zusammenhänge zu erlernen. Bei qwen-image
waren das mehrere millionen Bildpaare.


Aufgrund der Trainingsdaten (Bildpaare) kann eine künstliche Intelligenz in der Umsetzung einer Generationsanweisung (Prompt) natürlich in Bereiche kommen, welche Ähnlichkeiten oder
urheberechtlich kritische Übereinstimmungen aufzeigen. Das liegt in der Natur des Prozesses und dem menschlichen Wiedererkennungsvermögens auf Bildinhalte. Nicht zwingend muss dies die Grundlage
der verwendeten Trainingsdaten sein. Ein KI-gestützer Generationsprozess ist immer das "zuschwimmen" auf die nächstmögliche "Wahrscheinlichkeit". Eine generative KI arbeitet niemals "definitiv".

Dennoch gilt es die Rechte Dritter zu wahren und zu schützen. Und zugleich die rechtlichen Rahmenbedingungen einzuhalten.


Um diesen Umstand gerecht zu werden und die Arbeit mit diesem großartigen Werkzeug weiterhin möglich zu machen, gibt es technische Mechanismen welche die Transparenz, Dokumentation und Prüfung von
Generationen anwenderfreundlich gestalten.


## In der Praxis

In folgendem Screenshot eines produktionstypischen Workflow von modula-r.com werden folgende Prüfroutinen umgesetzt:

- Prompteingabeprüfung
- Promptlogging (HashChain-Prinzip)
- Stichwortvergleich kritisch/unkritisch
- Prüfung Ai-Act relevante Kontaminationen
- Prüfung DSGVO relevante Kontaminationen
- Abbruchszenario der Generation bei Detektion mit eindeutigem Logeintrag.


## Screenshot valide Eingabe mit Bestätigung und Output  

<img width="2834" height="1040" alt="dsgvo_check_ok" src="https://github.com/user-attachments/assets/13b97a41-22a8-4244-bdda-ff2a75e2cbae" />


Wir sehen die Eingabefelder mit den geschriebenen Prompts. Eine Prüfbestätigung wurde an den Nutzer ausgeben. 

Das eingetragene Log verweist auf die Regelkonforme Generation innerhalb der Prüfkriterien:

```json
{"gen_id": "226a2741-7272-4f3c-bd37-a61415e13a50", "timestamp": "2025-08-31T04:34:13.529451",
 "status": "✅OK - Keine Auffälligkeiten. Output bitte dennoch vor Export auf Urheberrechtslage der Inhalte prüfen!",
 "matches_found": 0,
 "sha_chain_prev": "ad5edca2736452195097d49bdff83d1a62c61d1c78a6467b2b67483827cff915",
 "sha_chain": "ce415d5e133731caa2a4030922e13c08271799232eb82888b15a6f22c7a391e4"}
```

---

## Screenshot invalide Eingabe mit Detektionswarnung

<img width="2830" height="1040" alt="dsgvo_check_dedect" src="https://github.com/user-attachments/assets/4fa42c88-4053-4566-abc7-1fb250bf0473" />


Hier hat uns das System eine eindeutige Warnmeldung aufgrund der in der Generationsanweisung gefundenen kritischen Begriffe, welche eine Rechtsverletzung potentiell
darstellen können, ausgegeben.

Im Log wurde es eindeutig hinterlegt:

```json
{"gen_id": "5dc63145-3ba3-4bce-a688-8c3b758fd992",
 "timestamp": "2025-08-31T04:36:52.461253",
 "status": "️⚠️Warnung: 2 kritische Begriffe erkannt. Output bitte prüfen auf mögliche Urheberrechtskonflikte.",
 "matches_found": 2,
 "sha_chain_prev": "dddd277d63615fea9fd9e68b14bdc1ca1670a6d9ec68b914868f2b5964a071c9",
 "sha_chain": "77e1e46b79f88943acd5819675192a2d9f346c26e1f852b6d189dc30ffa58114"}
```

---


## Screenshot "Raise Exception" Abgleich kritische Blacklist

<img width="2831" height="1060" alt="dsgvo_ai-act_raise" src="https://github.com/user-attachments/assets/950a6bf2-520d-4e13-8d3c-2a5aeb5151d2" />


Hier wurde ein Begriff innerhalb des Prompts ausgewertet, welcher über die AI-Act relevante Blacklist ermittelt wurde.

Diese Blacklist hat die Aufgabe, das Generieren von zb. Deepfakes, besonders kritsche Inhalte, sensible Inhalte, gewaltverherrlichende Inhalte etc. auszuschließen.

Ehe es zu einer Generation kommt und mögliche entsprechende Daten erzeugt werden könnten, geht hier die Prüfroutine auf den Exceptionzustand und bricht den Run (die Generation)
innerhalb der Pipeline ab. So haben Anwendente die Möglichkeit den Prompt umzugestalten oder erneut zu prüfen. Der gefundene Begriff wird mitgeteilt.

Der Logeintrag ist dann produktionstypisch, entsprechend verfasst:


```json
{
"⚠️ Verstoß 2025-08-31T06:35:52.350363"
"→ Positiv-Prompt": "Ultra-high-resolution stock photo, 8k, photorealistic, we have the year 1985. a navy warship with big guns, highly detailed, grey color tones, colorful flags on handrails, seems it is a happy event before navy vessel is leaving port. sun, sunlight, blue sky, slightly clouds, subtle reflections on surfaces, cool daylight tones, high dynamic range, blurred background with shipyard equipment, no human presence."
"→ Negativ-Prompt": "people, faces, hands, poor textures, logos, text, distortion, cartoonish look."
"→ Rechte Trainingsdaten":" [...]"
"→ Transparenz-Hinweis":" [...]"
"→ Compliance":" [...]"
"→ Hash":" 91ebc853c6a94c8212d7ce8d317bdf2854da3eac3fab7b174f4aac5cb2662588b3c68daeebed388a55276cc9d38e76b462b7a7ecba697e659eccb5256d979830"
"→ Prev Hash":" 863c731262286fd3a76aad0ddad9cc3e66faa3200ae693601690614af402ae23ca0a7f42e6c163dd671cd2f5dbd21d528fd0a0f9f11db967e16c2d94fc37adbd"
}
```

---

## Schlußwort

Diese Abhandlung unterliegt einer kontinuierlichen Wartung und Pflege. Neue Funktionen, Updates oder Änderungen werden hier festgehalten und im Hauptverzeichnis diesen Repository, via CHANGELOG.md festgehalten.

31.08.2025 modula-r.com







