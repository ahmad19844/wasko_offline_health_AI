# WASKO Offline Health AI

## Overview

Wasko Offline Health AI is an open-source, offline Artificial Intelligence-powered health information assistant designed to improve access to reliable healthcare information in low-resource environments. The application uses Retrieval-Augmented Generation (RAG) with a locally hosted Large Language Model (LLM) to provide context-aware responses based on a curated health knowledge base.

The system is designed to operate entirely offline, making it suitable for rural communities, educational institutions, healthcare outreach programs, humanitarian operations, and locations with unreliable internet connectivity.

---

## Key Features

* Fully offline operation
* Retrieval-Augmented Generation (RAG)
* Local GGUF Large Language Model
* Semantic search using Sentence Transformers
* FAISS vector database
* Streamlit web interface
* English and Hausa health knowledge base
* Privacy-preserving local inference
* Modular and extensible architecture

---

## Technology Stack

* Python
* Streamlit
* LangChain
* FAISS
* Sentence Transformers
* Hugging Face Transformers
* GGUF Local Language Model
* Markdown Knowledge Base

---

## Project Structure

```text
wasko_offline_health-AI/
│
├── assets/
├── core/
├── knowledge_base/
├── models/
├── .gitignore
├── app.py
├── config.py
├── download_model.sh
└── LICENCE
├── metadata.json
├── README.md
├── app.py
├── REPORT.md
├── requirements.txt
└── run_the_app.sh

```

---

## Installation

1. Clone the repository.

```bash
git clone https://github.com/ahmad19844/wasko_offline_health_AI.git
```

2. Navigate to the project directory.

```bash
cd wasko_offline_health_AI
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Launch the application.

```bash
streamlit run app.py
or 
click run_the_app.sh direct

```

---

## Example Questions

* what are the causes of cholera?
* mene bambanci tsakanin HIV da AIDS?
* Explain hypertension.
* What is HIV/AIDS?
* mene banbanci tsakanin HIV da AIDS?

---

## Disclaimer

Wasko offline health AI provides educational health information only. It is not intended to diagnose diseases, prescribe medications, or replace professional medical advice. Users should consult qualified healthcare professionals for diagnosis and treatment.

---

## Future Enhancements

* Voice interaction
* Android application
* Additional Nigerian languages
* Expanded health knowledge base
* Medical image support
* Knowledge base update tools
* African language expansion

---

## License

This project is released under the MIT License.

---

## Developer

**Ahmad Muhammad**

Position: Principal Program Analyst
Organization: National Environmental Standards and Regulation Enforcement Agency
Location: Abuja, Nigeria, email: amy33375@gmail.com mobile: +2348065510549

Africa Deep Tech Challenge (ADTC) 2026 Project
