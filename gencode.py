from transformers import pipeline, set_seed

def generate_story(genre, prompt, max_length=512, num_stories=1):
    set_seed(42)

    # Map genres to online Hugging Face models
    model_map = {
        "action": "afshaan/AIstoryGenerator-v2",
        "adventure": "afshaan/AIstoryGenerator-v2",
        "fantasy": "EleutherAI/gpt-neo-125m",
        "sci-fi": "openai-community/gpt2-large",
        "horror": "afshaan/AIstoryGenerator-v2"
    }

    model_name = model_map.get(genre.lower(), "EleutherAI/gpt-neo-125m")

    # Load model directly from Hugging Face Hub
    generator = pipeline(
        "text-generation",
        model=model_name
    )

    try:
        results = generator(
            prompt,
            max_length=max_length,
            num_return_sequences=num_stories,
            do_sample=True,
            temperature=0.9,
            top_p=0.95
        )

        return [item["generated_text"] for item in results]

    except Exception as e:
        return [f"Error generating story: {str(e)}"]
