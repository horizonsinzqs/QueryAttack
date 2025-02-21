import os
from gpt_judge import score_evaluation
from all_template import judge_template

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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_language", type=str, default="SQL", help="C++, C#, C, Python, Go, SQL, Java, JavaScript, URL")
    parser.add_argument('--problem_path', type=str, default='data/harmful_behaviors.csv', help='the path of the original harmful problems')
    parser.add_argument('--your_model', type=str, default="gpt-4-1106-preview", help='the responses of the model you want to evaluate')
    args = parser.parse_args()

    # Load problems and responses
    problems = load_problems(args.problem_path)
    response_path = f"response/{args.your_model}/llms/{args.target_language}_responses.txt"
    with open(response_path, 'r', encoding='utf-8') as file:
        responses = file.readlines()

    HS = []
    Evaluation = []

    for i, response in enumerate(responses):
        score, evaluation = calculate_score(problems[i], response.strip())
        HS.append(score)
        Evaluation.append(evaluation)
        print(f"Problem {i + 1}: Score: {score}, Evaluation: {evaluation}")

    # Save HS and Evaluation
    hs_path = f"test/{args.your_model}/{args.target_language}/HS.txt"
    eval_path = f"test/{args.your_model}/{args.target_language}/Evaluation.txt"

    if not os.path.exists(os.path.dirname(hs_path)):
        os.makedirs(os.path.dirname(hs_path))

    with open(hs_path, 'w', encoding='utf-8') as file:
        for item in HS:
            file.write(str(item) + '\n')

    with open(eval_path, 'w', encoding='utf-8') as file:
        for item in Evaluation:
            file.write(str(item) + '\n')