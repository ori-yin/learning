import pandas as pd
from snownlp import SnowNLP

df = pd.read_excel('D:\垃圾桶二号\数据处理\千库用户反馈.xlsx')

# 创建一个新列存储情感值
df['sentiment'] = 0.0

df.head()

# 遍历文本列，使用SnowNLP计算情感值
for i, text in enumerate(df['text']):
    sentiment = SnowNLP(text).sentiments
    df.at[i, 'sentiment'] = sentiment

df.to_csv('D:\垃圾桶二号\数据处理\文本情感分析结果.csv', index=False)

# sentiment列为结果的评分，越靠近1表示评价越积极，越靠近0表示评价越消极，0.5左右为一般评价