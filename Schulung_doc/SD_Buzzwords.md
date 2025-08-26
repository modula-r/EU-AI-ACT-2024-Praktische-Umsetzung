# 🧠 Generative Bild-KI – Glossar & Buzzwords (Fokus: ComfyUI)  
**Version: V.01-SD-SU-modula-r.com**

> Dieses Glossar bietet eine prägnante und fundierte Übersicht zentraler Begriffe und Technologien im Bereich der generativen Bild-KI – mit besonderem Fokus auf [ComfyUI](https://github.com/comfyanonymous/ComfyUI).  
> Zielgruppe: Entwickler:innen, Artists, Prompt Engineers und technische Mitwirkende. Ebenso EntscheiderInnen und allgemein Interessierte.

---

## 🗂️ Inhaltsverzeichnis

- [Allgemeine Begriffe](#-allgemeine-begriffe)
- [Modelle & Checkpoints](#-modelle--checkpoints)
- [Prompting & Conditioning](#-prompting--conditioning)
- [ComfyUI-spezifische Begriffe](#-comfyui-spezifische-begriffe)
- [Bildbearbeitung & Nodes](#-bildbearbeitung--nodes)
- [Dateiformate & Pipelines](#-dateiformate--pipelines)
- [Technische Grundlagen](#️-technische-grundlagen)
- [Hinweis](#-hinweis)
- [Lizenz](#-lizenz)

---

## 🧩 Allgemeine Begriffe

| Begriff             | Beschreibung |
|---------------------|--------------|
| **KI-generierte Bilder** | Bilder, die mithilfe neuronaler Netze aus Text- oder Bild-Inputs erzeugt werden. |
| **Diffusion Models** | Generative Modelle, die Rauschen schrittweise in realistische Bilder umwandeln. |
| **Latenter Raum (Latent Space)** | Abstrakte Repräsentation von Bilddaten in komprimierter Form. |
| **VAE (Variational Autoencoder)** | Codiert Bilder in den latenten Raum und rekonstruiert sie wieder. |
| **CLIP** | Modell von OpenAI zur Zuordnung von Text und Bild in einen gemeinsamen Repräsentationsraum. |

---

## 🧠 Modelle & Checkpoints

| Begriff | Beschreibung |
|--------|--------------|
| **Stable Diffusion (SD)** | Offenes, latentes Diffusionsmodell zur Bildgenerierung. |
| **Checkpoint (.ckpt / .safetensors)** | Modellzustand mit Gewichtungen und Architektur. |
| **LoRA (Low-Rank Adaptation)** | Leichtgewichtige Methode zur Modellanpassung. |
| **VAE File** | Separate Datei zur Decodierung/Encodierung im latenten Raum. |
| **Textual Inversion** | Methode zur Erweiterung eines Modells mit neuen Konzepten via Embeddings. |

---

## 💬 Prompting & Conditioning

| Begriff | Beschreibung |
|--------|--------------|
| **Prompt** | Texteingabe zur Steuerung des generierten Bildes. |
| **Negative Prompt** | Beschreibung dessen, was vermieden werden soll. |
| **Prompt Weighting** | Gewichtung von Begriffen zur Feinsteuerung, z. B. `(high detail:1.2)`. |
| **Conditioning** | Einflussnahme auf das Modell durch Text, Bilder, Masken etc. |

---

## 🧱 ComfyUI-spezifische Begriffe

| Begriff | Beschreibung |
|--------|--------------|
| **Node** | Einzelelement in ComfyUI zur Ausführung einer Funktion (z. B. „Text to Latent“). |
| **Workflow** | Gesamter graphischer Aufbau und Ablauf der Nodes. |
| **Custom Nodes** | Benutzerdefinierte, erweiterbare Nodes mit Spezialfunktionen. |
| **Preview Node** | Zeigt Zwischenergebnisse zur Kontrolle an. |
| **Execution Queue** | Reihenfolge und Ablauf der Node-Verarbeitung. |

---

## 🎨 Bildbearbeitung & Nodes

| Begriff | Beschreibung |
|--------|--------------|
| **Inpainting / Outpainting** | KI-basierte Rekonstruktion oder Erweiterung von Bildbereichen. |
| **ControlNet** | Externes Steuerungsmodell für Kompositionen (z. B. Pose, Kanten, Tiefen). |
| **Masking Node** | Node zur gezielten Ausmaskierung von Bildbereichen. |
| **Upscale Node** | Vergrößerung von Bildern via ESRGAN, RealESRGAN etc. |

---

## 📁 Dateiformate & Pipelines

| Begriff | Beschreibung |
|--------|--------------|
| **`.json` (Workflow File)** | Exportierter Node-Graph zur vollständigen Beschreibung einer Pipeline. |
| **`.png` / `.webp` (mit Metadata)** | Bildformate mit eingebetteten Workflow-Metadaten. |
| **`.safetensors`** | Sicheres Binärformat für Modellgewichte, Alternative zu `.ckpt`. |

---

## ⚙️ Technische Grundlagen

| Begriff | Beschreibung |
|--------|--------------|
| **CUDA / GPU Acceleration** | GPU-basierte KI-Beschleunigung via NVIDIA CUDA. |
| **Batch Size** | Anzahl gleichzeitiger Bildgenerierungen. |
| **Seed** | Startwert zur Steuerung von Zufälligkeit & Reproduzierbarkeit. |
| **Scheduler** | Algorithmus zur Steuerung der Rauschreduktion bei der Diffusion. |

---

## 📌 Hinweis

Diese Liste ist **nicht vollständig** und wird laufend erweitert.  
💡 *Vorschläge, Ergänzungen und Pull Requests sind ausdrücklich willkommen!*

---

## ✅ Lizenz

Dieses Glossar steht unter der **[MIT-Lizenz](LICENSE)** – frei zur Nutzung, Modifikation und Weitergabe.

---

## 🧷 Optional: Badges (für Repositories)

```markdown
![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
![Status: Work in Progress](https://img.shields.io/badge/status-in_progress-yellow)
