import os
import sys
import requests

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Emoji symbols
EMOJI_CHECK = '✅'
EMOJI_FAIL = '❌'
EMOJI_WARN = '⚠️'
EMOJI_INFO = 'ℹ️'
EMOJI_DELETE = '🗑️'
EMOJI_EXIT = '🚪'

# Configuration
TOKEN = os.getenv('GITHUB_TOKEN')
if not TOKEN:
    print(f"{RED}{BOLD}{EMOJI_FAIL} Error:{RESET} GITHUB_TOKEN environment variable not found.")
    print(f"{YELLOW}Set it using: {BOLD}export GITHUB_TOKEN=your_token_here{RESET}")
    sys.exit(1)

API_URL = 'https://api.github.com'
OWNER = '0x062'
REPOS_FILE = 'repos.txt'
LOG_FILE = 'log.txt'

HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_repos(owner):
    print(f"\n{CYAN}{BOLD}{EMOJI_INFO} Fetching repositories for user: {owner}{RESET}")
    repos = []
    page = 1
    while True:
        url = f"{API_URL}/user/repos?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"{RED}{EMOJI_FAIL} Failed to fetch: {response.status_code} - {response.json().get('message')}{RESET}")
            sys.exit(1)
        data = response.json()
        if not data:
            break
        for r in data:
            if r.get('owner', {}).get('login', '').lower() == owner.lower():
                if r.get('permissions', {}).get('admin'):
                    repos.append(r['name'])
                else:
                    print(f"{YELLOW}{EMOJI_WARN} Skipped (no admin rights): {r['name']}{RESET}")
        page += 1

    if not repos:
        print(f"{YELLOW}{EMOJI_WARN} No repositories found for '{owner}'.{RESET}")
        sys.exit(0)

    with open(REPOS_FILE, 'w') as f:
        for name in sorted(repos):
            f.write(name + '\n')
    print(f"{GREEN}{EMOJI_CHECK} {len(repos)} repositories saved to {REPOS_FILE}{RESET}\n")

def delete_repo(owner, repo, log):
    url = f"{API_URL}/repos/{owner}/{repo}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"{GREEN}{EMOJI_DELETE} Deleted: {repo}{RESET}")
        log.write(f"OK     {owner}/{repo}\n")
    else:
        msg = response.json().get('message')
        print(f"{RED}{EMOJI_FAIL} Failed to delete {repo}: {response.status_code} - {msg}{RESET}")
        log.write(f"FAIL   {owner}/{repo} - {response.status_code} {msg}\n")

def delete_from_file(owner):
    try:
        with open(REPOS_FILE, 'r') as f:
            repos = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}{EMOJI_FAIL} Error reading {REPOS_FILE}: {e}{RESET}")
        sys.exit(1)

    if not repos:
        print(f"{YELLOW}{EMOJI_WARN} Repository list is empty.{RESET}")
        sys.exit(0)

    print(f"\n{BLUE}{BOLD}{EMOJI_DELETE} You are about to delete {len(repos)} repositories for {owner}.{RESET}")
    confirm = input(f"{YELLOW}Type '{BOLD}y{RESET}{YELLOW}' to confirm: {RESET}")
    if confirm.lower() != 'y':
        print(f"{CYAN}{EMOJI_EXIT} Operation cancelled.{RESET}")
        sys.exit(0)

    with open(LOG_FILE, 'w') as log:
        for repo in repos:
            delete_repo(owner, repo, log)

    print(f"\n{GREEN}{EMOJI_CHECK} Deletion complete. Log saved to {LOG_FILE}{RESET}")

if __name__ == '__main__':
    print(f"{CYAN}{BOLD}\n=== GitHub Repo Manager ==={RESET}")
    print(f"{BLUE}1. {EMOJI_INFO} {BOLD}Fetch repository list{RESET}")
    print(f"{BLUE}2. {EMOJI_DELETE} {BOLD}Delete repositories from file{RESET}")
    print(f"{BLUE}0. {EMOJI_EXIT} {BOLD}Exit{RESET}")
    choice = input(f"{CYAN}Choose an action (1/2/0): {RESET}")

    if choice == '1':
        fetch_repos(OWNER)
    elif choice == '2':
        delete_from_file(OWNER)
    elif choice == '0':
        print(f"{GREEN}{EMOJI_EXIT} Goodbye!{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}{EMOJI_FAIL} Invalid option. Exiting.{RESET}")
        sys.exit(0)
