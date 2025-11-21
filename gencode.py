from transformers import pipeline
import gc

generators = {}

model_map = {
    "action": "afshaan/AIstoryGenerator-v2",
    "adventure": "afshaan/AIstoryGenerator-v2",
    "fantasy": "EleutherAI/gpt-neo-125M",
    "sci-fi": "openai-community/gpt2-large",
    "horror": "afshaan/AIstoryGenerator-v2"
}

def load_model(model_name):
    if model_name not in generators:
        # Clear old models from RAM
        generators.clear()
        gc.collect()

        generators[model_name] = pipeline(
            "text-generation",
            model=model_name
        )
    return generators[model_name]


def generate_story(genre, prompt, max_length=512, num_stories=1):
    model_name = model_map.get(genre.lower(), "EleutherAI/gpt-neo-125M")

    generator = load_model(model_name)

    results = generator(
        prompt,
        max_length=max_length,
        num_return_sequences=num_stories,
        do_sample=True,
        temperature=0.9,
        top_p=0.95
    )
    return [item["generated_text"] for item in results]
