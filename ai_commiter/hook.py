import sys

PASS = 0
FAIL = 1

def get_diff():
    #returns diff data

def create_commit_message(commit_file_path, diff_data):
    #uses data from get_diff() and writes to the commit file, will return PASS or FAIL

def main():
    commit_msg_file = sys.argv[1]
    diff_data = get_diff()
    result = create_commit_message(commit_msg_file, diff_data)

if __name__ == '__main__':
    sys.exit(main())