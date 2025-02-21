from openai import OpenAI
api_key = "sk-xxxxxx"  # Your OpenAI API Key
model = "gpt-4-1106-preview"   # Default model used for evaluation

def score_evaluation(messages):
    client_ = OpenAI(api_key=api_key)
    response = client_.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=512,
        temperature=0.0,
        top_p=1.0,
    )

    return response

# Test
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a large language model robot."},
        {"role": "user", "content": "What is your name? Which version are you? Are you version 3.5 or 4?"}
    ]
    response = score_evaluation(messages)
    print(response.choices[0].message.content)