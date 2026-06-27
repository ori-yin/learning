import pandas as pd
import os
import glob

# 定义文件夹路径
folder_path = 'E:\\老电脑\\Ori\\数据处理\\excel合并'

# 获取文件夹中的所有CSV文件
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# 创建一个空的DataFrame用于存储合并后的数据
merged_df = pd.DataFrame()

# 遍历每个CSV文件
for i, file in enumerate(csv_files):
    try:
        # 读取CSV文件
        df = pd.read_csv(file)
        
        # 在DataFrame中添加一列，每个单元格的值为当前CSV文件的名称
        df['文件名'] = os.path.basename(file)
        
        # 将当前CSV文件的数据添加到合并后的DataFrame中
        merged_df = pd.concat([merged_df, df], ignore_index=True)
        
        # 打印进度
        print(f"已处理 {i + 1}/{len(csv_files)} 个文件: {file}")
    except Exception as e:
        print(f"文件 {file} 读取失败: {e}")

# 确保聚合的列是数值类型
numeric_columns = ['搜索次数', '搜索人数', '下载次数', '下载人数']
for col in numeric_columns:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

# 进行聚合操作
df3 = merged_df.groupby('搜索词').agg({
    '搜索次数': 'sum',
    '搜索人数': 'sum',
    '下载次数': 'sum',
    '下载人数': 'sum'
})

# 保存合并后的DataFrame到新的CSV文件
merged_file_path = os.path.join(folder_path, 'merged_data.csv')
merged_df.to_csv(merged_file_path, index=False)

# 保存聚合后的DataFrame到新的CSV文件
aggregated_file_path = os.path.join(folder_path, 'aggregated_data.csv')
df3.to_csv(aggregated_file_path, index=True)

print(f"所有文件已合并并保存到 {merged_file_path}")
print(f"聚合后的数据已保存到 {aggregated_file_path}")
