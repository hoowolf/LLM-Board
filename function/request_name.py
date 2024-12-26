import requests

# 设置目标组织名
org_name = 'QwenLM'
                                                                                                                                                                                                                                                                                                                                                            
# 发送请求
url = f'https://api.github.com/orgs/{org_name}/repos'
response = requests.get(url)

# 检查响应状态
if response.status_code == 200:
    repos = response.json()
    # 提取所有仓库的名字
    repo_names = [repo['name'] for repo in repos]
    print(f'所有仓库名：{repo_names}')
else:
    print(f'请求失败，状态码：{response.status_code}')