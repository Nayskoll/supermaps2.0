import pandas as pd


csv_file2 = 'new_activities.csv'
df2 = pd.read_csv(csv_file2, encoding='utf-8', on_bad_lines='skip')
df = pd.read_csv(csv_file2, encoding='utf-8', on_bad_lines='warn')



