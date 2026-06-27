import pandas as pd

# 当有多个excel需要拼起来的时候，用下面的代码
excel1 = pd.read_csv('D:\垃圾桶二号\\1.csv',encoding='GBK')
excel2 = pd.read_csv('D:\垃圾桶二号\\2.csv',encoding='GBK')
excel3 = pd.concat([excel1,excel2])
df_row = excel3

# df_row = pd.read_csv(path,encoding='GBK')    # 读取文件

df_g = df_row.groupby(['一级分类','二级分类']).agg({'编辑人数':'sum','下载人数':'sum','素材ID':'nunique'})    # 每列怎么算

df_not_null = df_row[df_row['下载人数']>0]    # 筛掉0下载的素材

df_not_null_g = df_not_null.groupby(['一级分类','二级分类']).agg({'素材ID':'nunique'})    # 0下载的聚合

df_merge = pd.merge(df_g,df_not_null_g,how='left',on=['一级分类','二级分类'],suffixes=['被编辑内容数','被下载内容数'])    # 合并

# 这里为了给每一行加小计，代码抄的，我看不懂！
df_all = (pd.concat([df_merge,df_merge.groupby(level=0).sum().assign(二级分类='小计')
.set_index('二级分类', append=True)]).sort_index())

df_all['编辑下载率'] = df_all['下载人数'] / df_all['编辑人数']    # 创建一个新列，算下载率

df_sort = df_all.groupby(['一级分类'],as_index=False).apply(lambda x:x.sort_values('下载人数',ascending=False))
# as_index用于分组无标签，然后apply一个按下载人数降序

df_r = df_sort.reset_index()    # 打散groupby

df_end = df_r.drop(labels='level_0', axis=1)    # 删除多余的索引列

df_sort.to_csv('D:\ori-learn\\模板日下载.csv')    # 导出