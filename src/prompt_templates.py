# src/prompt_templates.py

TEMPLATES = {
    "product-name": {
        "template": "What is a good name for a company that makes {product}?",
        "variables": ["product"],
        "defaults": {"product": "colorful socks"}
    },
    "explain-simple": {
        "template": "Explain {topic} in a simple way for {audience}.",
        "variables": ["topic", "audience"],
        "defaults": {"topic": "income tax", "audience": "a 12-year-old"}
    },
    "translate": {
        "template": "Translate the following from {input_language} to {output_language}:\n\n{text}",
        "variables": ["input_language", "output_language", "text"],
        "defaults": {"input_language": "English", "output_language": "Hindi", "text": "I love programming"}
    }
}

FEW_SHOT_EXAMPLES = [
    {"input": "What is 2+2?", "output": "2+2 is 4."},
    {"input": "Explain GDP in simple terms", "output": "GDP is the total value of all goods and services produced in a country in a year."},
    {"input": "Name a company that makes comfy shoes", "output": "CloudStep — comfy shoes for everyday walking."}
]
