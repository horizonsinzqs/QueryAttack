# QueryAttack

This is the repository that contains the source code for QueryAttack. You can refer our work by [QueryAttack](https://never-far.github.io/llmqueryattack/) website.


## Project Structure

This project mainly contains the following Python files:

- `translator.py`: This file is responsible for the main translation tasks in the project. It take the input from the original CSV file, perform the necessary processing and translations based on the provided target language, and store the results in the specified storage path.
- `test.py`: It is used to test on different large language models, including the gpt series, deepseek series, llama series, etc.
- `test_gemini.py`: Used for testing on the gemini family of large language models.
- `demo.ipynb`: A Jupyter Notebook file for project presentation. It shows the performance of our proposed QueryAttack.
- `evaluate_responses.py`: This file is used to assess the harmfulness of responses generated by QueryAttack.

## Usage

### 1. Clone the project
```bash
git clone <Project repository address>
cd <Project directory>
```

### 2. Install dependencies and API Preparation
```bash
pip install -r requirements.txt
```

#### API Preparation

To use this project, you need to obtain API keys for the relevant large language models. Here are the steps and considerations for different models:

##### OpenAI Models (e.g., GPT series)
1. **Sign up for an OpenAI account**:
   - Go to the OpenAI official website (https://openai.com/) and sign up for an account if you don't have one already.
2. **Generate an API key**:
   - Log in to your OpenAI account and navigate to the API key management section.
   - Create a new API key. Make sure to keep this key secure, as it grants access to your OpenAI account resources.
3. **Configure the API key in the project**:
   - In the `openai_log.py`、`gpt_judge.py` files of this project, you will find the `API_CONFIGS` dictionary or `api_key`. Replace the placeholder `"sk-xxx"` with your actual OpenAI API key for the relevant models (e.g., `"gpt-4o"` and `"gpt-4-1106-preview"`).

##### Other Models (DeepSeek, Llama, etc.)
- Similar to OpenAI, you need to sign up for accounts on the respective platforms that provide these models.
- Obtain the API keys from their official websites or developer portals.
- Update the `API_CONFIGS` dictionary in the `openai_log.py` and `api_key` in `gpt_judge.py` 、`test_gemini.py` files with the obtained API keys for the corresponding models.

**Note**:
- Some models may require additional configuration, such as setting the base URL. Make sure to follow the official documentation of each model to correctly configure these settings.
- API keys are sensitive information. Do not share them publicly or commit them to version control systems. It is recommended to use environment variables or other secure methods to manage your API keys in a production environment.


### 3. Run the program
```bash
python translator.py --path <Path to the original CSV file> --store_path <Storage path> --target_language <Target language>
```
```bash
python test.py --target_language <Target language>
```
```bash
python test_gemini.py --target_language <Target language>
```
```bash
python evaluate_responses.py --your_model <the responses of the model you want to evaluate>  --target_language <Target language>
```

## Example
```bash
python translator.py --path data/harmful_behaviors.csv --store_path data --target_language Python
```
```bash
python test.py --target_language Python
```
```bash
python evaluate_responses.py --your_model gpt-4-1106-preview --target_language Python
```

## Contributing
If you want to contribute to this project, please follow these steps:
1. Fork the project repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Create a pull request to the original repository.

## License
This project is licensed under the [MIT License]. See the `LICENSE` file for more details.
