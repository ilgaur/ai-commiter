import sys
import subprocess

PASS = 0
FAIL = 1

def get_diff():
    #returns diff data
    result = subprocess.run(['git', 'diff', '--staged'], captured_output=True, text=True)
    return result.stdout
def create_commit_message(commit_file_path, diff_data):
    #uses data from get_diff() and writes to the commit file, will return PASS or FAIL
    pass
def main():
    if len(sys.argv) < 2:
        return FAIL
    commit_msg_file = sys.argv[1]
    diff_data = get_diff()
    result = create_commit_message(commit_msg_file, diff_data)

if __name__ == '__main__':
    sys.exit(main())