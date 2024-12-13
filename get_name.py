import requests
import json

# GitHub API URL for listing repositories of an organization
GITHUB_API_URL = "https://api.github.com/orgs/{}/repos"

# List of organization names
org_names = ['SkyworkAI', 'QwenLM', 'InternLM', 'THUDM', 'OpenBMB', '01-ai', 'OpenMoss', 'FlagAI-Open', 'baichuan-inc', 'IDEA-CCNL', 'XVERSE-ai']

# Dictionary to store organization names and their repositories
org_repos = {}


# Function to get all repositories for a given organization
def get_all_repos(org):
    page = 1
    per_page = 100  # Maximum number of results per page
    all_repos = []
    
    while True:
        response = requests.get(GITHUB_API_URL.format(org), params={'page': page, 'per_page': per_page})
        
        if response.status_code == 200:
            repos = response.json()
            if not repos:
                break
            all_repos.extend([repo['name'] for repo in repos])
            page += 1
        else:
            print(f"Failed to fetch repositories for {org} on page {page}: {response.status_code}")
            break
    
    return all_repos

# Iterate over each organization name
for org in org_names:
    repo_names = get_all_repos(org)
    org_repos[org] = repo_names

# Save the dictionary to a JSON file
with open('org_repos.json', 'w') as json_file:
    json.dump(org_repos, json_file, indent=4)

print("Repository data has been saved to org_repos.json")