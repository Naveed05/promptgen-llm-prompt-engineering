<div align="center">

# 🧠 PromptGen — LLM Prompt Engineering Playground  
### A modular, multi-provider prompt engineering platform powered by OpenAI, Groq & Ollama

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![LLM](https://img.shields.io/badge/LLM-OpenAI%20%7C%20Groq%20%7C%20Ollama-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Project%20Status-Active-brightgreen)

</div>

---

## 🚀 Overview
**PromptGen** is a powerful prompt-engineering platform that allows users to:

- Design, test, and optimize prompts  
- Use few-shot examples  
- Run prompts across **multiple LLM providers**  
- Build custom templates  
- Export chat history  
- Perform professional prompt-engineering experiments

This project is structured in a **production-ready modular architecture** suitable for real-world enterprise GenAI workflows.

---

## ✨ Key Features

### 🔹 1. Multi-Provider LLM Support  
Supports the following:

| Provider | Status | Model Used |
|---------|--------|-------------|
| **OpenAI** | ✅ | GPT-3.5 / GPT-4 (optional) |
| **Groq** | ✅ | Llama-3.1-8B |
| **Ollama** | ✅ | Mistral / Llama / Gemma |
| **Local-Fallback** | ✅ | Offline mode (no API key needed) |

---

### 🔹 2. Advanced Prompt Engineering Tools  
- Create dynamic templates  
- Add variables and auto-fill them  
- Few-shot prompting  
- System prompt customization  
- Prompt preview engine  
- Token & temperature control  

---

### 🔹 3. Rich UI (Streamlit)  
- Real-time streaming responses  
- Interactive playground  
- Multi-turn conversation  
- Chat history viewer  
- JSON export  

---

### 🔹 4. Production-Ready Code  
- Modular architecture  
- Separation of providers  
- CI/CD workflow  
- API-key security (via `.env` + `.gitignore`)  
- Extensible for new models  

---

## 🗂 Folder Structure


PROMPTGEN/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── .env (ignored)
│
├── src/
│ ├── llm_providers.py
│ ├── prompt_templates.py
│ ├── utils.py
│ └── pycache/
│
├── history/
│── .github/
└── workflows/
└── ci.yml

yaml
Copy code



---

## 🔧 Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/Naveed05/promptgen-llm-prompt-engineering.git
cd promptgen-llm-prompt-engineering

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Set API keys
Create a .env file (DO NOT upload to GitHub):
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
OLLAMA_API_KEY=your_key

4️⃣ Run the app
streamlit run app.py

🧪 CI/CD Pipeline (GitHub Actions)
This repository includes a zero-config deployment-ready automation pipeline.

Features:
Build & dependency installation
Lint check
Streamlit run validation
Artifact generation
GitHub badge integration

Workflow file:
.github/workflows/ci.yml

⭐ Support
If you like this project, please ⭐ star this repo.
It helps visibility and motivates further development!

👨‍💻 Author

Mirza Naveed Baig
AI & Data Science | GenAI Developer
India

