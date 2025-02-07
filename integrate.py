import pandas as pd

distances_df = pd.read_csv('distances.csv')
last_commit_date_df = pd.read_csv('last_commit_date.csv')
no_sourceCommit_df = pd.read_csv('no_sourceCommit.txt', header=None, names=['Data'])  # 每行一个数据，没有分隔符
untranslated_df = pd.read_csv('untranslated.txt', header=None, names=['Data'])  # 每行一个数据，没有分隔符

distances_df = distances_df.sort_values(by='Distance', ascending=False)
last_commit_date_df = last_commit_date_df.sort_values(by='Last Modified Date')
no_sourceCommit_df = no_sourceCommit_df.sort_values(by='Data')
untranslated_df = untranslated_df.sort_values(by='Data')

with pd.ExcelWriter('output.xlsx') as writer:
    distances_df.to_excel(writer, sheet_name='Distances', index=False)
    last_commit_date_df.to_excel(writer, sheet_name='Last_Commit_Date', index=False)
    no_sourceCommit_df.to_excel(writer, sheet_name='No_Source_Commit', index=False)
    untranslated_df.to_excel(writer, sheet_name='Untranslated', index=False)

print("数据已成功写入 output.xlsx")
