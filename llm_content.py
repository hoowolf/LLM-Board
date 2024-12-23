import pandas as pd
import json

# 获得指标数据集且一直更新
df = pd.read_parquet("hf://datasets/open-llm-leaderboard/contents/data/train-00000-of-00001.parquet")

print(df.info())

df_needed = df[['Type', 'fullname', 'Average ⬆️', 'CO₂ cost (kg)', 'IFEval', 'BBH', 'MATH Lvl 5', 'GPQA', 'MUSR', 'MMLU-PRO']]

# 将 df_needed 转换为 JSON 文件并保存在当前目录
df_needed.to_json('df_needed.json', orient='records', indent=4, force_ascii=False)

# 读取原始 JSON 文件
with open('df_needed.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化目标结构
target_structure = {}

# 遍历原始数据并填充目标结构
for item in data:
    # 检查是否包含 'root_dir' 和 'sub_dir'
    if 'root_dir' not in item or 'sub_dir' not in item:
        print(f"跳过条目，缺少 'root_dir' 或 'sub_dir': {item}")
        continue
    
    root_dir = item['root_dir']
    sub_dir = item['sub_dir']
    
    if root_dir not in target_structure:
        target_structure[root_dir] = {}
    
    target_structure[root_dir][sub_dir] = {
        "Type": item["Type"],
        "root": root_dir,
        "name": sub_dir,
        "Average ⬆️": item["Average ⬆️"],
        "CO₂ cost (kg)": item["CO₂ cost (kg)"],
        "IFEval": item["IFEval"],
        "BBH": item["BBH"],
        "MATH Lvl 5": item["MATH Lvl 5"],
        "GPQA": item["GPQA"],
        "MUSR": item["MUSR"],
        "MMLU-PRO": item["MMLU-PRO"]
    }

# 将结果写入新的 JSON 文件
with open('transformed_df_needed_processed.json', 'w', encoding='utf-8') as file:
    json.dump(target_structure, file, ensure_ascii=False, indent=4)

print("转换完成，结果已保存到 transformed_df_needed_processed.json")