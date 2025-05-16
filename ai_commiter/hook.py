import sys
import subprocess
from openai import OpenAI

PASS = 0
FAIL = 1

def get_diff():
    #returns diff data
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True).stdout
    return result

def get_api_config():
    try:
        api_key = subprocess.check_output(['git', 'config', 'ai-commiter.api-key'], text=True).strip()
        base_url = subprocess.check_output(['git', 'config', 'ai-commiter.base-url'], text=True).strip()
        print(f"Retrieved API key: {api_key}")
        print(f"Retrieved API key: {base_url}")
        return api_key, base_url
    except Exception as e:
        print(f"Error retrieving config: {e}")
        return None, None

def generate_commit_msg(diff_data):
    api_key, base_url = get_api_config()

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        extra_body={},
        model="qwen/qwen3-1.7b:free",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that generates clear, concise git commit messages based on code diffs"
            },
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ]
    )
    return completion.choices[0].message.content

def write_commit_message(commit_file_path, commit_msg):
    #uses data from get_diff() and writes to the commit file, will return PASS or FAIL
    print(f"Received commit file path: {commit_file_path}")
    print(f"Diff data length: {len(commit_msg)}")
    print(f"First 100 chars of diff: {commit_msg}")
    return PASS

def main():
    if len(sys.argv) < 2:
        return FAIL
    # get_api_config()
    commit_msg_file = sys.argv[1]
    diff_data = get_diff()

#   print(diff_data)
    commit_message = generate_commit_msg(diff_data)
    if commit_message is None:
        return FAIL
    result = write_commit_message(commit_msg_file, commit_message)
    return result

if __name__ == '__main__':
    sys.exit(main())