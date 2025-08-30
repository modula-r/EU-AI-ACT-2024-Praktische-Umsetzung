# Stock Image Audit Storage
---

## Stockbilder aus dem Generator

Für professionelle Anwendungen innerhalb einer produktiven Umgebung kann es sehr nutzvoll sein, immer wieder verwendete Stockelemente griffbereit zu haben.
Diese Funktion ermöglicht es innerhelb eines ComfyUI Workflow, über eine gepflegte Bibliothek, benötigte Inhalte immer auf Abfrage gezielt zu generieren, statt
sie mühsam selektieren und zusammenstellen zu müssen.

Ein weiterer Vorteil besteht darin, das sämtliche Prompts schon geprüft und audifiziert im Storagefile gelagert sind.

Workflow laden - Stock wählen - ausführen. So einfach!

---

## Möglichkeiten der Grundfunktion

Die Prompt_Storage_Node bietet dabei folgende Funktionen.

1. Aus einem Kontextmenu einfach die bereits geprüften und verifizierten Generationsanweisungen für qwen-image auswählen.
2. Falls neue Anweisungen nötig sind muss nicht extra der Workflow gewechselt werden. Stattdessen im Kontextmenu einfach die Vorauswahl auf "None" stellen und via Texteingabe die manuelle Generation ausführen.

---

## Die Struktur der Bibliothek bildet sich wiefolgt ab:

```json
{
  "library": [
    {
      "name": "Prompt 1",
      "positive": "positive prompt text",
      "negative": "negative prompt text"
    },
    {
      "name": "Prompt 2",
      "positive": "positive prompt text",
      "negative": "negative prompt text"
    }
  ]
}
```

---

## Produktionstypischer modula-r Workflow mit Prompt_Storage_Stock Funktion

<img width="2577" height="1549" alt="Stock_storage_Workflow" src="https://github.com/user-attachments/assets/b2878f87-1ef1-4d42-aa54-5c9c84982c82" />

---

Nachfolgend einige Outputs aus der aktuell verfügbaren Bibliothek.
Diese Generationen unterliegen der Apache2.0 Lizenz und innerhalb dieser Lizenz frei nutzbar.

---

## Stock-Produkte Qwen-Image-fb8


![Stock_Gen1](Images/stock_gen1.png)

![Stock_Gen2](Images/stock_gen2.png)

![Stock_Gen3](Images/stock_gen3.png)

![Stock_Gen4](Images/stock_gen4.png)

![Stock_Gen5](Images/stock_gen5.png)

![Stock_Gen6](Images/stock_gen6.png)

![Stock_Gen7](Images/stock_gen7.png)

---

### Weiterentwicklung Funktionen

Diese Funktion wird fortlaufend weiterentwickelt und gepflegt. Ein Upgrade der Node wird in Kürze verfügbar sein.

Hier geht es zum Respority: [ComfyUI-QwenImage-PromptStorage-Node](https://github.com/modula-r/ComfyUI-QwenImage-PromptStorage-Node)
