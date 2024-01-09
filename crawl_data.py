import requests
from datetime import datetime
import json

def get_repo_data(repo_url, access_token):
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return repo_data
    else:
        print(f"Failed to fetch commits. Status code: {response.status_code}")
        return None

def get_all_commits(repo_url, access_token):
    all_commits = []
    page = 1
    per_page = 10000

    while True:
        commits_url = f"{repo_url}/commits"
        params = {"page": page, "per_page": per_page}
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(commits_url, headers=headers, params=params)

        if response.status_code == 200:
            commits = response.json()
            if not commits:  # Không còn commits nữa
                break
            all_commits.extend(commits)
            page += 1
        else:
            print(f"Failed to fetch commits. Status code: {response.status_code}")
            return None
    return all_commits


def extract_commit_info(commit):
    sha = commit['sha']
    message = commit['commit']['message']
    author = commit['commit']['author']['name']
    timestamp = commit['commit']['author']['date']
    
    files_changed = commit.get('files', [])

    return {'sha': sha, 'message': message, 'author': author, 'timestamp': timestamp, 'files_changed': files_changed}

def extract_code_changes(files_changed):
    added_lines = sum(file.get('additions') for file in files_changed)
    removed_lines = sum(file.get('deletions') for file in files_changed)
    total_lines_before = sum(file.get('changes') for file in files_changed) + removed_lines

    return {'added_lines': added_lines, 'removed_lines': removed_lines, 'total_lines_before': total_lines_before}

def analyze_developer_experiences(commits):
    developers = set()
    unique_files_changed = set()
    time_intervals = []

    for commit in commits:
        author_name = commit['commit']['author']['name']
        developers.add(author_name)
        
        files_changed = commit.get('files', [])

        unique_files_changed.update(file.get('filename', '') for file in files_changed)

        timestamp = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        time_intervals.append(timestamp)

    num_developers = len(developers)
    num_unique_files_changed = len(unique_files_changed)
    avg_time_interval = (max(time_intervals) - min(time_intervals)) / len(time_intervals)

    return {'num_developers': num_developers, 'num_unique_files_changed': num_unique_files_changed, 'avg_time_interval': avg_time_interval}

if __name__ == "__main__":
    access_token = "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"
    with open('input.txt', 'r') as f:
        owner, repo= f.readlines()
    repo_url = f"https://api.github.com/repos/{owner.rstrip()}/{repo.rstrip()}"

    repo_data = get_repo_data(repo_url, access_token)
    commits = get_all_commits(repo_url, access_token)

    with open('infor_repo_&_list_commits.txt', 'w') as f:
        language = f"Language: {repo_data['language']}\n"
        author = f"Author: {repo_data['owner']['login']}\n"
        publishing_time = f"Created at: {repo_data['created_at']}\n"
        commits_json = json.dumps(get_all_commits(repo_url, access_token), indent=4)
        f.write(f"{language}{author}{publishing_time}")
        f.write(f'Numsber of commits: {len(commits)}\n')
        f.write(commits_json)

    # if commits:
    #     for commit in commits:
    #         print(json.dumps(commit,indent=4))
    #         break
    #         commit_info = extract_commit_info(commit)
    #         code_changes = extract_code_changes(commit_info['files_changed'])
    #         developer_experiences = analyze_developer_experiences(commits)

    #         # Print or save the extracted information as needed
    #         print("Commit Information:")
    #         print(commit_info)
    #         print("\nCode Changes:")
    #         print(code_changes)
    #         print("\nDeveloper Experiences:")
    #         print(developer_experiences)
    #         print("\n-----------------------\n")

