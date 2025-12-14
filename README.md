# Smart Concierge - NLU Dataset 🗂️

![Language](https://img.shields.io/badge/Language-English-green)
![Format](https://img.shields.io/badge/Format-JSONL-blue)
![Task](https://img.shields.io/badge/Task-Intent_Recognition_%26_NER-orange)
![License](https://img.shields.io/badge/License-MIT-grey)

This repository contains the dataset used to fine-tune the **Smart Concierge NLU Model**. 

It consists of pairs of **natural language inputs** (simulating transcriptions of voice commands given to a concierge) and their corresponding **structured JSON outputs** (intents and entities). The data is focused on the Brazilian Portuguese context.

> **Related Repository:** The model trained on this data can be found at [Smart-Concierge/Model](https://github.com/Smart-Concierge/Model).

---

## 📊 Dataset Overview

The dataset is designed to train Small Language Models (SLMs) to perform **Joint Intent Detection and Slot Filling**.

- **Language:** Brazilian Portuguese (pt-BR)
- **Format:** JSONL (JSON Lines)
- **Domain:** Residential Concierge / Condominium Management
- **Total Samples:** ~5,000 (Approx.)

## 📝 Data Structure

Each line in the dataset represents a single interaction containing the user input and the expected logical output.

### Schema Example

```json
{
  "input": "O entregador do iFood chegou, é pra dona Maria do 304 bloco B, pode liberar.",
  "output": "{\"intent\": \"solicitar_entrega_refeicao\", \"sugestao_acao\": \"NOTIFICAR_MORADOR\", \"entities\": {\"empresa\": \"iFood\", \"requer_pagamento\": false, \"destino\": {\"tipo\": \"unidade\", \"identificador\": \"304\", \"bloco\": \"B\"}, \"nome_morador\": \"Maria\"}}"
}
```

> **Note:** The `output` field is stored as a stringified JSON to facilitate tokenization during the SFT (Supervised Fine-Tuning) process.

---

## 🏷️ Taxonomy & Intents

The dataset covers several scenarios typical of a building reception. The main intents (`intent`) include:

| Intent | Description |
| :--- | :--- |
| `solicitar_entrega_refeicao` | Delivery of food (e.g., iFood, Pizza). |
| `solicitar_entrega_encomenda` | General packages (e.g., Amazon, Mercado Livre, Correios). |
| `anunciar_visitante` | Arrival of a guest or service provider. |
| `anunciar_prestador_servico` | Specific flow for maintenance/repair workers. |
| `reservar_espaco` | Booking common areas (Party Hall, BBQ area). |
| `registrar_ocorrencia` | Noise complaints or maintenance issues. |
| `autorizar_entrada` | Pre-authorization for future visits. |

---

## 🛠️ How to Use

This dataset is intended to be processed before training. If you are using our [Model Training Pipeline](https://github.com/Smart-Concierge/Model), the workflow is:

1. **Download the Data:**
   Clone this repository to get the `.jsonl` files.

2. **Preprocessing:**
   Use the `formata_dataset.py` script (located in the Model repo) to convert this raw format into the specific **Phi-3 Chat Template** (`<|user|> ... <|assistant|> ...`).

   ```python
   # Example of how the data is transformed for the model:
   formatted_text = f"<|user|>\n{row['input']}<|end|>\n<|assistant|>\n{row['output']}<|end|>"
   ```

---

## ⚖️ License & Citation

This dataset is released under the **MIT License**.

If you use this dataset in your research or project, please link back to this repository.

**Authors:**
* Pietro Comin
* Nathan Endo
* Lucas Pedroso

*Project developed for the Computer Science Bachelor's degree at UFPR.*
