# Technical Report — Wasko offline Health AI: An Offline AI-Powered Health Assistant for Low-Resource Communities

**Team ID:** wasko_offline_health_ai  
**Domain:** Healthcare & Medical 
**Model:** TinyLlama-1.1b-Chat-v1.0.Q4_K_M

---

# Problem

Access to reliable healthcare information remains a significant challenge in many African communities due to poor internet connectivity, limited healthcare infrastructure, language barriers, and the high cost of online AI services. Rural communities, schools, humanitarian organizations, and primary healthcare workers often operate in environments where internet access is unavailable or unreliable.
Wasko offline health AI addresses this challenge by providing an entirely offline Artificial Intelligence-powered health information assistant capable of answering common health questions in both English and Hausa using a locally hosted Large Language Model (LLM) combined with Retrieval-Augmented Generation (RAG).

The system is specifically designed for:

- Rural communities
- Community health workers
- Educational institutions
- NGOs and humanitarian organizations
- Healthcare awareness campaigns
- Students learning basic health knowledge

Unlike cloud-based AI assistants, Wasko offline Health AI performs all inference locally, ensuring user privacy while eliminating internet dependency and recurring API costs.
The knowledge base currently includes curated healthcare information covering diseases, maternal health, child health, nutrition, emergency care, first aid, infectious diseases, chronic illnesses, and preventive healthcare in both English and Hausa.

---

# Design Decisions

## Base Model

TinyLlama-1.1B-Chat-v1.0

TinyLlama was selected because it offers an excellent balance between reasoning capability, inference speed, memory usage, and compatibility with consumer laptops commonly available across Africa.

---

## Quantization

GGUF Q4_K_M

The Q4_K_M quantization was selected because it:

- Reduces memory usage significantly
- Maintains good response quality
- Enables CPU-only inference
- Runs comfortably on 8 GB RAM laptops
- Provides faster response generation than higher precision models

---

## Runtime

- llama.cpp
- llama-cpp-python

The project uses llama.cpp for efficient CPU inference without requiring dedicated GPUs.

---

## Retrieval-Augmented Generation (RAG)

Instead of relying solely on the language model's internal knowledge, the application retrieves relevant information from a curated healthcare knowledge base before generating responses.

The retrieval pipeline consists of:

- Markdown health documents
- Sentence Transformer embeddings
- FAISS vector database
- Semantic similarity search
- Context-aware prompt construction

This significantly improves factual accuracy while reducing hallucinations.

---

## User Interface

A Streamlit-based interface was selected because it:

- Requires minimal system resources
- Is easy to deploy
- Supports rapid development
- Works well on Windows and Linux
- Provides an intuitive interface for non-technical users

---

## Multilingual Support

The system supports:

- English
- Hausa

Supporting Hausa improves accessibility for millions of users accross African countries.

---

## Alternatives Considered

Several alternatives were evaluated during development:

### Larger Language Models

Examples:

- Llama 3
- Mistral 7B

These models were rejected because they:

- Require substantially more RAM
- Produce slower inference
- Are less practical for offline deployment on standard laptops

### Lower Quantization (Q2)

Although Q2 reduced memory usage further, response quality degraded noticeably.

### Higher Quantization (Q8)

Q8 improved response quality slightly but exceeded the target hardware limitations and increased inference time.

The selected TinyLlama Q4_K_M configuration provided the best balance between performance and resource efficiency.

---

# Constraints

The design of Wasko offline Health AI was guided by real-world deployment constraints common across many African communities.

## Hardware Constraints

Target hardware:

- 8 GB RAM
- Consumer laptop
- Integrated graphics
- CPU-only inference

No dedicated GPU is required.

---

## Connectivity Constraints

The application is designed for environments where:

- Internet connectivity is unavailable
- Mobile data is expensive
- Network reliability is poor

All processing occurs locally.

---

## Power Constraints

Many deployment environments experience unstable electricity.

The lightweight TinyLlama model minimizes computation, reducing power consumption and allowing operation on battery-powered laptops for extended periods.

---

## Data Constraints

Reliable local healthcare datasets are limited.

To improve reliability, a curated healthcare knowledge base was developed using Markdown documents covering:

- Malaria
- Typhoid
- Tuberculosis
- HIV/AIDS
- Diabetes
- Hypertension
- Child Health
- Maternal Health
- Nutrition
- Emergency Care
- First Aid
- Infectious Diseases

The documents were indexed using FAISS to enable semantic retrieval.

---

## Language Constraints

Many existing AI healthcare systems primarily support English.

Wasko offline Health AI incorporates Hausa content to improve accessibility for local populations.

---

## Privacy Constraints

Healthcare information is sensitive.

Because all inference runs locally, no user queries or health information leave the user's device, improving privacy and security.

---

# Benchmarks

The following values were observed during development on consumer Windows laptop.

| Metric | Value |
|---|---|
| Development Machine | Windows 10/11 Laptop |
| Processor | Intel Core i5 (Consumer Laptop) |
| RAM | 8 GB |
| GPU | Integrated Graphics |
| Runtime | llama.cpp |
| Model | TinyLlama-1.1B-Chat-v1.0.Q4_K_M |
| Model Size | ~636 MB |
| Quantization | GGUF Q4_K_M |
| Embedding Model | Sentence Transformers |
| Vector Store | FAISS |
| User Interface | Streamlit |
| Internet Required | No |
| Offline Capability | Fully Offline |
| Supported Languages | English, Hausa |
| Knowledge Base | Markdown Documents with RAG |
| Inference | CPU Only |

These development observations are provided for reference. Official benchmarkingperformed using the Africa Deep Tech Challenge (ADTC) evaluation environment.

---

# Impact

Wasko offline Health AI demonstrates that practical healthcare AI systems can operate entirely offline using affordable consumer hardware.

Potential deployment environments include:

- Rural healthcare centres
- Schools
- Community health outreach
- NGOs
- Humanitarian missions
- Emergency response teams
- Public health awareness campaigns

By combining lightweight language models with Retrieval-Augmented Generation, the project delivers accurate, privacy-preserving, multilingual healthcare assistance suitable for low-resource African environments.

---

# Repository structure

wasko_offline_health_AI/
├── assets/
├── core/
├── knowledge_base/
├── models/
├── .gitignore
├── app.py
├── config.py
├── download.model.sh
├── LICENCE
├── metadata.json
├── README.md
├── REPORT.md
└── requirements.txt
# Conclusion

Wasko offline Health AI successfully meets the objectives of developing an efficient offline AI application for healthcare education and information dissemination.
The project demonstrates that lightweight open-source language models, combined with Retrieval-Augmented Generation and carefully curated healthcare knowledge, can provide reliable, multilingual, privacy-preserving healthcare assistance without requiring internet connectivity or specialized hardware.
This work contributes toward improving digital healthcare accessibility across Africa while aligning with the goals of the African Defence Technology Challenge (ADTC) by delivering a deployable AI solution optimized for real-world constraints.
