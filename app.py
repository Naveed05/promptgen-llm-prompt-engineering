from dotenv import load_dotenv
load_dotenv()

import os
import time
import json
import streamlit as st

from src.prompt_templates import TEMPLATES, FEW_SHOT_EXAMPLES
from src.llm_providers import ProviderFactory, ProviderUnavailableError
from src.utils import save_chat_history, export_history_as_json, validate_env_keys


# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="PromptGen — AI Prompt Engineering", layout="wide")

st.title("🧠 PromptGen — AI Prompt Engineering Playground")
st.markdown("Create, test, optimize prompts across OpenAI, Groq, Ollama, and Local models.")


# ---------------- SIDEBAR ----------------
st.sidebar.header("LLM Settings")

provider_choice = st.sidebar.selectbox(
    "Select Provider",
    ["openai", "groq", "ollama", "local-fallback"]
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 2048, 512)
system_prompt = st.sidebar.text_area("System Prompt", value="You are a helpful AI assistant.")
use_few_shot = st.sidebar.checkbox("Use Few-Shot Examples", True)

save_history_flag = st.sidebar.checkbox("Save Chat History", True)

st.sidebar.markdown("---")
missing_keys = validate_env_keys(["OPENAI_API_KEY", "GROQ_API_KEY"])
if missing_keys:
    st.sidebar.warning(f"Missing keys: {', '.join(missing_keys)}")


# ---------------- LOAD PROVIDER ----------------
try:
    provider = ProviderFactory.create_provider(provider_choice, temperature, max_tokens)
except ProviderUnavailableError as e:
    provider = None
    st.sidebar.error(str(e))


# ---------------- PROMPT DESIGNER ----------------
st.subheader("🎨 Prompt Designer")

col1, col2 = st.columns([2, 1])

with col1:
    template_name = st.selectbox("Choose Template", list(TEMPLATES.keys()))
    template = TEMPLATES[template_name]

    text_template = st.text_area("Template", value=template["template"], height=180)

    # dynamic variable inputs
    user_inputs = {}
    for var in template["variables"]:
        user_inputs[var] = st.text_input(var, template.get("defaults", {}).get(var, ""))

    extra_instruction = st.text_area("Extra User Instruction", "")

with col2:
    st.markdown("### Few-Shot Examples")
    st.write(FEW_SHOT_EXAMPLES[:3])
    if use_few_shot:
        st.info(f"Using {len(FEW_SHOT_EXAMPLES)} examples")


# ---------------- PROMPT PREVIEW ----------------
st.subheader("📌 Final Prompt Preview")

final_user_prompt = text_template
for k, v in user_inputs.items():
    final_user_prompt = final_user_prompt.replace("{" + k + "}", v)

if extra_instruction.strip():
    final_user_prompt += "\n\n" + extra_instruction.strip()

full_prompt_preview = f"SYSTEM: {system_prompt}\n\n"

if use_few_shot:
    for ex in FEW_SHOT_EXAMPLES:
        full_prompt_preview += f"Human: {ex['input']}\nAssistant: {ex['output']}\n\n"

full_prompt_preview += f"User: {final_user_prompt}\nAssistant:"

st.code(full_prompt_preview)


# ---------------- RUN PROMPT ----------------
st.subheader("🚀 Run Model")

user_input_override = st.text_area("User Input (Optional Override)", final_user_prompt)

run = st.button("Generate Response ▶️")


# chat history memory
if "chat" not in st.session_state:
    st.session_state.chat = []


if run:
    if provider is None:
        st.error("No provider loaded.")
    else:
        payload = {
            "system": system_prompt,
            "prompt": user_input_override,
            "few_shot": use_few_shot,
            "model": "llama3-8b"
        }

        slot = st.empty()
        slot.info("Contacting model...")

        try:
            result = provider.generate(payload)
            st.markdown(f"### 🤖 Assistant Response:\n{result}")

            st.session_state.chat.append({
                "provider": provider_choice,
                "user": user_input_override,
                "assistant": result
            })

            if save_history_flag:
                save_chat_history(st.session_state.chat)

        except Exception as e:
            st.error(f"Error: {e}")


# ---------------- HISTORY ----------------
st.subheader("🗂 Chat History")

for msg in reversed(st.session_state.chat[-10:]):
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**Assistant ({msg['provider']}):** {msg['assistant']}")


colA, colB = st.columns(2)

with colA:
    if st.button("Export as JSON"):
        st.download_button(
            "Download JSON",
            json.dumps(export_history_as_json(st.session_state.chat), indent=2),
            "promptgen_history.json"
        )

with colB:
    if st.button("Clear History"):
        st.session_state.chat = []
        st.success("History cleared!")
