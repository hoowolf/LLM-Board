import requests
import json
import pandas as pd

# 基础URL和参数
base_url = 'https://oss.x-lab.info/open_digger/github/'
repo_name = 'QwenLM/Qwen2.5'  # 你可以通过参数化来获取这个值
type_name = 'stars'  # 你可以通过参数化来获取这个值

# 构建完整的URL
url = f"{base_url}{repo_name}/{type_name}.json"

# 获取JSON数据
response = requests.get(url)
data = response.json()

# 提取月份和数据
dates = [k for k in data.keys() if len(k) == 7]
values = [data[k] for k in dates]

# 计算累积值
acc_values = []
cumulative_sum = 0
for value in values:
    cumulative_sum += value
    acc_values.append(cumulative_sum)

# 创建DataFrame
df = pd.DataFrame({
    'month': dates,
    'value': values,
    'accumulated_value': acc_values
})

# 保存到JSON文件
output_file = 'output_data.json'
df.to_json(output_file, orient='records', lines=True)

print(f"数据已保存到 {output_file}")