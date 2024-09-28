import pandas as pd

csv_file = 'paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)
df = df[['name']].drop_duplicates()

csv_file2 = 'new_activities.csv'
df2 = pd.read_csv(csv_file2)
df = pd.concat([df, df2[['name']].drop_duplicates()], ignore_index=True)

df.to_csv('paris_activities_names.csv', index=False, encoding='utf-8-sig')