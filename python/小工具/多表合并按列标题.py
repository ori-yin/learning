import os
import pandas as pd

def merge_excel_files(directory, output_file):
    # 初始化一个空的DataFrame用于存储合并后的数据
    combined_df = pd.DataFrame()

    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx') and not filename.startswith('~$'):  # 确保是Excel文件且不是临时文件
            file_path = os.path.join(directory, filename)
            # 读取每个Excel文件的第一个工作表到一个DataFrame中
            df = pd.read_excel(file_path)
            
            # 如果combined_df为空，则直接赋值
            if combined_df.empty:
                combined_df = df
            else:
                # 使用列名来合并行，相同的列名会自动对齐
                combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)

    # 去除重复行（如果需要的话）
    combined_df.drop_duplicates(inplace=True)

    # 将合并后的DataFrame写入新的Excel文件
    combined_df.to_excel(output_file, index=False)

# 使用函数，假设你的文件在'./excels'目录下，输出文件名为'merged.xlsx'
merge_excel_files('./excels', 'merged.xlsx')