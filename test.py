import os
from openai import OpenAI
from openai_log import your_api_key, your_base_url, your_model
from all_template import judge_template
from gpt_judge import score_evaluation
from all_template import C_assistant_response_4o, C_plusplus_assistant_response_4o, C_sharp_assistant_response_4o, Python_assistant_response_4o, Go_assistant_response_4o, SQL_assistant_response_4o, Java_assistant_response_4o, JavaScript_assistant_response_4o, URL_assistant_response_4o
from all_template import C_first_user_content_4o, C_plusplus_first_user_content_4o, C_sharp_first_user_content_4o, Python_first_user_content_4o, Go_first_user_content_4o, SQL_first_user_content_4o, Java_first_user_content_4o, JavaScript_first_user_content_4o, URL_first_user_content_4o

# Context conversation
def ask_response_context(messages, args):
    response = None
    while response is None:
            client = OpenAI(api_key=your_api_key, base_url=your_base_url)
            response = client.chat.completions.create(
                model=your_model,
                messages=messages,
                stream=False,
                max_tokens=args.max_new_tokens,
                temperature=args.temperate,
                top_p=args.top_p,
                seed=args.seed
            )
    return response

# Calculate HS
def calculate_score(problem, response):
    eval_prompt = judge_template.format(problem, response)
    messages = [{"role": "user", "content": eval_prompt}]
    score = None
    response_text = None
    while score is None:
        chat_completion = score_evaluation(messages)
        response_text = chat_completion.choices[0].message.content
        score = extract_content("#thescore:", response_text)
    return score, response_text

def load_trans(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    sentences = data.strip().split('---\n')
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def extract_content(tag, text):
    start_idx = text.find(tag)
    if start_idx == -1:
        return None
    content_after_tag = text[start_idx+len(tag):].strip()
    parts = content_after_tag.split()
    if tag == "#thescore:":
        if parts and (parts[0].isdigit() or (len(parts[0]) > 0 and parts[0][0].isdigit())):
            if parts[0].isdigit():
                return int(parts[0])
            if parts[0][0].isdigit():
                return int(parts[0][0])
        else:
            return None
    else:
        end_idx = text.find("#", start_idx + 1)
        return content_after_tag if end_idx == -1 else content_after_tag[:end_idx].strip()

def load_problems(data_path):
    all_datas = []
    with open(data_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            all_datas.append(line)
    return all_datas

def process_sentence(i, sentence, args, first_user_content, assistant_response):
    system_content = ""
    user_content = first_user_content

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

    messages.append({"role": "assistant", "content": assistant_response})
    user_content_2 = sentence
    messages.append({"role": "user", "content": user_content_2})

    response_2 = ask_response_context(messages, args)
    assistant_response_2 = response_2.choices[0].message.content
    assistant_response_2_no_newline = assistant_response_2.replace('\n', '\\n')
    print(f"{i + 1}:  {assistant_response_2_no_newline}")
    return assistant_response_2_no_newline

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_language", type=str, default="SQL", help="C++, C#, C, Python, Go, SQL, Java, JavaScript, URL")
    parser.add_argument('--temperate', type=float, default=0, help='temperature for the model to generate text')
    parser.add_argument('--top_p', type=float, default=1, help='top_p for the model to generate text')
    parser.add_argument('--max_new_tokens', type=int, default=512, help='max_new_tokens for the model to generate text')
    parser.add_argument('--seed', type=int, default=0, help='seed for the model to generate text')
    args = parser.parse_args()

    start_str_map = {
        "C++": "int",
        "C#": "public",
        "C": "int",
        "Python": "def",
        "Go": "package",
        "SQL": "SELECT",
        "Java": "public",
        "JavaScript": "function",
        "URL": "https"
    }

    start_str = start_str_map.get(args.target_language)

    prompt_path = f"data/llms/{args.target_language}_translated.csv"
    response_path = f"response/{your_model}/llms/{args.target_language}_responses.txt"

    data = load_trans(prompt_path)

    responses_list = []

    # Define language and corresponding variable name mapping
    first_user_content_map_4o = {
        "C++": C_plusplus_first_user_content_4o,
        "C#": C_sharp_first_user_content_4o,
        "C": C_first_user_content_4o,
        "Python": Python_first_user_content_4o,
        "Go": Go_first_user_content_4o,
        "SQL": SQL_first_user_content_4o,
        "Java": Java_first_user_content_4o,
        "JavaScript": JavaScript_first_user_content_4o,
        "URL": URL_first_user_content_4o
    }

    first_user_content_map = first_user_content_map_4o
    # Select the corresponding variable name based on the target language
    first_user_content = first_user_content_map.get(args.target_language)

    # Define language and corresponding variable name mapping
    assistant_response_map_4o = {
        "C++": C_plusplus_assistant_response_4o,
        "C#": C_sharp_assistant_response_4o,
        "C": C_assistant_response_4o,
        "Python": Python_assistant_response_4o,
        "Go": Go_assistant_response_4o,
        "SQL": SQL_assistant_response_4o,
        "Java": Java_assistant_response_4o,
        "JavaScript": JavaScript_assistant_response_4o,
        "URL": URL_assistant_response_4o
    }
    # Select the corresponding variable name based on the target language
    assistant_response = assistant_response_map_4o.get(args.target_language)

    responses = []

    for i, sentence in enumerate(data):
        result = process_sentence(i, sentence, args, first_user_content, assistant_response)
        assistant_response_2_no_newline = result
        responses.append(assistant_response_2_no_newline + '\n')


    if not os.path.exists(os.path.dirname(response_path)):
        os.makedirs(os.path.dirname(response_path))

    with open(response_path, 'w', encoding='utf-8') as file:
        file.writelines(responses)