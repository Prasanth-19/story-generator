from transformers import AutoTokenizer, AutoModelForCausalLM

model_map = {
    "afshaan": "afshaan/AIstoryGenerator-v2",
    "gpt2-large": "gpt2-large",
    "gpt-neo-125M": "EleutherAI/gpt-neo-125M"
}

for name, model_id in model_map.items():
    print(f"Downloading {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    tokenizer.save_pretrained(f"models/{name}")
    model.save_pretrained(f"models/{name}")
    print(f"Saved {name} to models/{name}")
