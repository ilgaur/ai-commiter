import sys
import subprocess
from openai import OpenAI

PASS = 0
FAIL = 1

def get_diff():
    #returns diff data
    result = subprocess.run(['git', 'diff', '--staged'], capture_output=True, text=True).stdout
    return result

def generate_commit_msg(diff_data):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
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
    print(f"First 100 chars of diff: {commit_msg[:100]}")
    return PASS

def main():
    if len(sys.argv) < 2:
        return FAIL
    commit_msg_file = sys.argv[1]
    diff_data = get_diff()
#   print(diff_data)
    commit_message = generate_commit_msg(diff_data)
    if commit_message is None
        return FAIL
    result = write_commit_message(commit_msg_file, commit_message)
    return result

if __name__ == '__main__':
    sys.exit(main())