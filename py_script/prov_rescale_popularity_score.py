import pandas as pd

csv_file = 'paris_activities_high_touristic.csv'
df = pd.read_csv(csv_file)
#df["slug"] = df["name"].apply(lambda x: slugify(x))
df = df.drop(columns=df.filter(like='popularity_score').columns)

all_col = df.columns 
print(all_col)

df = df.groupby("name").agg({
    'description': 'first',
    'image_url': 'first',
    'chill_score': 'mean',
    'touristic_score': 'mean',
    'cultural_score': 'mean',
    'must_do_score': 'mean',
    'family_friendly_score': 'mean',
    'large_group_friendly_score': 'mean',
    'couple_friendly_score': 'mean',
    'small_group_friendly_score': 'mean',
    'budget': 'mean',
    'average_duration_hours': 'mean',
    'latitude': 'mean',
    'longitude': 'max'
}).reset_index()

pop_score_file = 'popularity_score.csv'
df_pop_score = pd.read_csv(pop_score_file)
df_pop_score["popularity_score"] = round(9 * ((df_pop_score['popularity_score'] - df_pop_score['popularity_score'].min()) / (df_pop_score['popularity_score'].max() - df_pop_score['popularity_score'].min())) + 1 )

duplicates = df_pop_score[df_pop_score['name'].duplicated(keep='first')]
print(duplicates)


df_pop_score = df_pop_score.groupby("name").agg({
    "popularity_score":"mean"
}).reset_index()

df_pop_score.to_csv('popularity_score.csv', index=False, encoding='utf-8-sig')

new_df = df.merge(df_pop_score, how="left", on="name").drop_duplicates()
print(new_df.head(5))

print(len(new_df.name))

new_df.to_csv('paris_activities_high_touristic.csv', index=False, encoding='utf-8-sig')