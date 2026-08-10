from openai import OpenAI

client = OpenAI()

def generate_ai_review(prompt):
    response = client.responses.create(model = "gpt-5.6", input = prompt)

    return response.output_text