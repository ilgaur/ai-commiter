import sys
import subprocess
import os
from openai import OpenAI
from dataclasses import dataclass

DEFAULT_SYSTEM_PROMPT = "You are a developer creating semantic git commit messages following the convention: type(scope): description. Types include feat, fix, docs, style, refactor, perf, test, build, ci, and chore. Keep messages explanatory and comprehensive and provide technical explanation, make sure you do not lose details, use imperative present tense, and focus on what the change does, not how. Don't capitalize first letter or use period at end. Include relevant scope in parentheses when applicable."
DEFAULT_USER_PROMPT = "Create a clear and well organized semantic commit message for this diff"
DEFAULT_MODEL = "deepseek/deepseek-chat:free"

@dataclass
class Config:
    api_key: str
    base_url: str
    model: str
    system_prompt: str
    user_prompt: str

def get_diff():
    #returns diff data
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True).stdout
    return result

def get_config_env_vars():
    try:
        return {
            "api_key": os.environ.get("AI_COMMITER_API_KEY", ""),
            "base_url": os.environ.get("AI_COMMITER_BASE_URL", ""),
            "model": os.environ.get("AI_COMMITER_MODEL", DEFAULT_MODEL),
            "system_prompt": os.environ.get("AI_COMMITER_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
            "user_prompt": os.environ.get("AI_COMMITER_USER_PROMPT", DEFAULT_USER_PROMPT)
        }
    except Exception as e:
        raise Exception(f"Error retrieving environment variables: {e}")

def create_config_from_env_vars(env_vars):
    try:
        if not env_vars["api_key"]:
            raise Exception("API Key is missing")
        if not env_vars["base_url"]:
            raise Exception("Base URL is missing")

        return Config(
            api_key=env_vars["api_key"],
            base_url=env_vars["base_url"],
            model=env_vars["model"],
            system_prompt=env_vars["system_prompt"],
            user_prompt=env_vars["user_prompt"]
        )
    except Exception as e:
        raise Exception(f"Can't  create the configuration: {e}")

def generate_commit_msg(diff_data, config):
    try:
        client = OpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
        )

        completion = client.chat.completions.create(
            extra_body={},
            model=config.model,
            messages=[
                {
                    "role": "system",
                    "content": f"{config.system_prompt}"
                },
                {
                    "role": "user",
                    "content": f"{config.user_prompt}:\n\n{diff_data}"
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating commit message: {e}")

def write_commit_message(commit_file_path, commit_msg):
    #uses data from get_diff() and writes to the commit file, will return PASS or FAIL
    print(f"Received commit file path: {commit_file_path}")
    print(f"Diff data length: {len(commit_msg)}")
    print(f"{commit_msg}")
    try:
        with open(commit_file_path, 'w') as f:
            f.write(commit_msg)
        return 0
    except Exception as e:
        raise Exception(f"Error writing commit message: {e}")

def main():
    #first arg is the script name and the second arg is the file which I'm validating to make sure it exists
    if len(sys.argv) < 2:
        return 1

    try:
        env_vars = get_config_env_vars()
        config = create_config_from_env_vars(env_vars)

        commit_msg_file = sys.argv[1]
        diff_data = get_diff()
        if not diff_data:
            return 1

        commit_message = generate_commit_msg(diff_data, config)
        if commit_message is None:
            return 1
        result = write_commit_message(commit_msg_file, commit_message)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())


#testing the hook