import pandas as pd

csv_file = 'paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)
#df["slug"] = df["name"].apply(lambda x: slugify(x))
df = df.drop(columns=df.filter(like='popularity_score').columns)

pop_score_file = 'popularity_score.csv'
df_pop_score = pd.read_csv(pop_score_file)
df_pop_score["popularity_score"] = round(9 * ((df_pop_score['popularity_score'] - df_pop_score['popularity_score'].min()) / (df_pop_score['popularity_score'].max() - df_pop_score['popularity_score'].min())) + 1 )

new_df = df.merge(df_pop_score, how="left", on="name").drop_duplicates()
print(new_df.head(5))

new_df.to_csv('paris_activities_high_touristic.csv', index=False, encoding='utf-8-sig')