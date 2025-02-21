from openai import OpenAI, PermissionDeniedError, APIConnectionError, RateLimitError, AuthenticationError, BadRequestError, InternalServerError
import time

# API configurations
API_CONFIGS = {
    "deepseek": {
        "api_key": "sk-xxx",
        "base_url": "",
        "model": "deepseek-chat"
    },
    "gpt-3.5-turbo": {
        "api_key": "sk-xxx",
        "base_url": "",
        "model": "gpt-3.5-turbo"
    },
    "gpt-4-1106-preview": {
        "api_key": "sk-xxx",
        "base_url": "",
        "model": "gpt-4-1106-preview"
    },
    "gpt-4o": {
        "api_key": "sk-xxx",
        "base_url": "",
        "model": "gpt-4o"
    },
}

# Default model
LLM_MODEL = "gpt-4-1106-preview"

# Get the configuration for the selected model
config = API_CONFIGS.get(LLM_MODEL)
if not config:
    raise ValueError(f"Invalid LLM model: {LLM_MODEL}")

your_api_key = config["api_key"]
your_base_url = config["base_url"]
your_model = config["model"]
sleep_time = config.get("sleep_time", 3)

def ask_response(system_content, user_content):
    client = OpenAI(api_key=your_api_key, base_url=your_base_url)
    response = None
    while response is None:
        response = client.chat.completions.create(
            model=your_model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            stream=False
        )
    print("response:", response.choices[0].message.content)
    return response
