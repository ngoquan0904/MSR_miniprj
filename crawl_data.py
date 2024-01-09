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
            if not commits:
                break
            all_commits.extend(commits)
            page += 1
        else:
            print(f"Failed to fetch commits. Status code: {response.status_code}")
            return None
    return all_commits

def get_contributor(repo_url, access_token):
    contributors_url = f"{repo_url}/contributors"
    contributors = len(get_repo_data(contributors_url, access_token))
    return contributors

def extract_commit_info(detail_commit):

    sha = detail_commit['sha']
    message = detail_commit['commit']['message']
    author = detail_commit['commit']['author']['name']
    committer = detail_commit['commit']['committer']['name']
    num_dev_involved.add(author)
    timestamp = commit['commit']['author']['date']
    # timestamp = datetime.strptime(detail_commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
    # time_intervals.append(timestamp)
    added_lines = detail_commit['stats']['additions']
    removed_lines = detail_commit['stats']['deletions']

    return {'sha': sha, 'message': message, 'author': author,'committer': committer, 'timestamp': timestamp, 'total of addlines':added_lines, 'total of removed lines':removed_lines}

def extract_code_changes_file(file):
    sha = file['sha']
    file_name = file['filename']
    added_lines = file['additions']
    removed_lines = file['deletions']

    return {'sha': sha, 'file_name': file_name, 'numbers of addlines': added_lines, 'numbers of removed lines': removed_lines}



if __name__ == "__main__":
    access_token = "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"
    with open('input.txt', 'r') as f:
        owner, repo= f.readlines()
    repo_url = f"https://api.github.com/repos/{owner.rstrip()}/{repo.rstrip()}"

    repo_data = get_repo_data(repo_url, access_token)
    commits = get_all_commits(repo_url, access_token)

    
    if commits:
        # time_intervals = []
        contributors = set()
        num_dev_involved = set()
        with open('code_changes.txt', 'w') as f:
            for commit in commits:
                detail_commit = get_repo_data(commit['url'], access_token)
                commit_infor = json.dumps(extract_commit_info(detail_commit), indent=4)
                f.write(f"Commit Information:\n{commit_infor}")
                f.write("\nCode Changes File:\n")
                for file in detail_commit['files']:
                    file_changes = json.dumps(extract_code_changes_file(file), indent=4)
                    f.write(f"{file_changes}\n")
                f.write("\n---------------\n")
            f.write(f"Numbers of developer involved: {len(num_dev_involved)}")
            # avg_time_interval = (max(time_intervals) - min(time_intervals)) / len(time_intervals)
            # print(avg_time_interval)


        with open('infor_repo_and_list_commits.txt', 'w') as f:
            language = f"Language: {repo_data['language']}\n"
            author = f"Author: {repo_data['owner']['login']}\n"
            publishing_time = f"Created at: {repo_data['created_at']}\n"
            commits_json = json.dumps(get_all_commits(repo_url, access_token), indent=4)
            f.write(f"{language}{author}{publishing_time}")
            f.write(f"Numbers of contributors:{get_contributor(repo_url, access_token)}\n")
            f.write(f'Numsber of commits: {len(commits)}\n')
            f.write(commits_json)

        
