import pandas as pd
from datetime import datetime, timedelta


languages = ["es", "fr", "ja", "ko", "pt-br", "ru", "zh-cn", "zh-tw"]

# 读取数据
distances_df = pd.read_csv('distances.csv')
last_commit_date_df = pd.read_csv('last_commit_date.csv')
no_sourceCommit_df = pd.read_csv('no_sourceCommit.txt', header=None, names=['Data'])  # 每行一个数据，没有分隔符
untranslated_df = pd.read_csv('untranslated.txt', header=None, names=['Data'])  # 每行一个数据，没有分隔符

distances_df = distances_df[distances_df['Distance'] != 0]

# 处理 Last Modified Date 列，删除在当前日期三个月之内的行
current_date = datetime.now()
three_months_ago = current_date - timedelta(days=90)
three_months_ago_str = three_months_ago.strftime('%Y-%m-%d')
last_commit_date_df = last_commit_date_df[last_commit_date_df['Last Modified Date'] < three_months_ago_str]

# 排序数据
distances_df = distances_df.sort_values(by='Distance', ascending=False)
last_commit_date_df = last_commit_date_df.sort_values(by='Last Modified Date')
no_sourceCommit_df = no_sourceCommit_df.sort_values(by='Data')
untranslated_df = untranslated_df.sort_values(by='Data')

# 写入 Excel 文件
with pd.ExcelWriter('output/all.xlsx') as writer:
    distances_df.to_excel(writer, sheet_name='Distances', index=False)
    last_commit_date_df.to_excel(writer, sheet_name='Last_Commit_Date', index=False)
    no_sourceCommit_df.to_excel(writer, sheet_name='No_Source_Commit', index=False)
    untranslated_df.to_excel(writer, sheet_name='Untranslated', index=False)

# 按语言写入 Excel 文件
for lang in languages:
    lang_dist_df = distances_df[distances_df['File'].str.startswith(lang)]
    lang_last_commit_df = last_commit_date_df[last_commit_date_df['File'].str.startswith(f'files/{lang}')]
    lang_no_sourceCommit_df = no_sourceCommit_df[no_sourceCommit_df['Data'].str.startswith(lang)]
    lang_untranslated_df = untranslated_df[untranslated_df['Data'].str.startswith(lang)]
    
    with pd.ExcelWriter(f'output/{lang}.xlsx') as writer:
        lang_dist_df.to_excel(writer, sheet_name='Distances', index=False)
        lang_last_commit_df.to_excel(writer, sheet_name='Last_Commit_Date', index=False)
        lang_no_sourceCommit_df.to_excel(writer, sheet_name='No_Source_Commit', index=False)
        lang_untranslated_df.to_excel(writer, sheet_name='Untranslated', index=False)

print(f"written to ./output")
