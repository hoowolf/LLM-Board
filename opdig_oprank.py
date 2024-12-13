import requests
import json
import os
import time
# 获取组织仓库名称列表
def get_repo_names(org_name, token=None):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是 200，抛出异常
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred for {org_name}: {http_err}')
        return []
    except Exception as err:
        print(f'Other error occurred for {org_name}: {err}')
        return []
    
    repos = response.json()
    repo_names = [repo['name'] for repo in repos]
    return repo_names

# 下载并保存仓库数据
def download_and_save_openrank_data(repo_name, org_name, token=None):
    url = f"https://oss.open-digger.cn/github/{org_name}/{repo_name}/openrank.json"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        file_path = os.path.join(os.getcwd(), f"{repo_name}_openrank.json")
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON data for {repo_name} has been saved to {file_path}")
        return data
    else:
        print(f"Failed to retrieve data for {repo_name}: {response.status_code}")
        return None

# 将所有数据合并到一个JSON文件中
def merge_all_data_to_json(org_names, token=None):
    all_data = {}

    for org_name in org_names:
        print(f"Processing organization: {org_name}")
        repo_names = get_repo_names(org_name, token)
        org_data = {}
        
        for repo_name in repo_names:
            repo_data = download_and_save_openrank_data(repo_name, org_name, token)
            if repo_data is not None:
                org_data[repo_name] = repo_data
        
        all_data[org_name] = org_data
    
    output_file = 'all_openrank_data.json'
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)
    print(f"All data has been saved to {output_file}")

if __name__ == "__main__":
    org_names = ['SkyworkAI', 'QwenLM', 'InternLM', 'THUDM', 'OpenBMB', '01-ai', 'OpenMoss', 'FlagAI-Open', 'baichuan-inc', 'IDEA-CCNL', 'XVERSE-ai']
    token = 'your_token'  # 替换为你的个人访问令牌
    merge_all_data_to_json(org_names, token)