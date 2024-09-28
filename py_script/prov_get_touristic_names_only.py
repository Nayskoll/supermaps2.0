import pandas as pd

csv_file = '/Users/davidbellaiche/PycharmProjects/chatgptapi/paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)
df = df[['name']].drop_duplicates()

df.to_csv('paris_activities_names.csv', index=False, encoding='utf-8-sig')