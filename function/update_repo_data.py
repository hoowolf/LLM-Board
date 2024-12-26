import requests
import json

# 你的个人访问令牌
TOKEN = ''

# 从JSON文件中读取仓库列表
with open('source/org_repos.json', 'r', encoding='utf-8') as f:
    repos = json.load(f)

repo_data = {}

# 获取每个仓库的Star数、Fork数、Issues数和贡献者数
for org, repo_list in repos.items():
    for repo in repo_list:
        repo_full_name = f"{org}/{repo}"
        url = f"https://api.github.com/repos/{repo_full_name}"
        headers = {
            'Authorization': f'token {TOKEN}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            contributors_url = data['contributors_url']
            contributors_response = requests.get(contributors_url, headers=headers)
            if contributors_response.status_code == 200:
                contributors = contributors_response.json()
                repo_data[repo_full_name] = {
                    'stargazers_count': data['stargazers_count'],
                    'forks_count': data['forks_count'],
                    'issues_count': data['open_issues'],
                    'contributors_count': len(contributors)
                }
        else:
            print(f"Failed to fetch data for {repo_full_name}")

# 将数据保存到JSON文件中
with open('source/repo_data.json', 'w', encoding='utf-8') as f:
    json.dump(repo_data, f, ensure_ascii=False, indent=4)