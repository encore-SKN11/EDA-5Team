import pandas as pd

credits = pd.read_csv('./data/tmdb_5000_credits.csv') # change path 
movies = pd.read_csv('./data/tmdb_5000_movies.csv')

# Check if both id columns are unique

# print(credits[credits['movie_id'].duplicated()]) 
# print(movies[movies['id'].duplicated()]) 


# merge two dataframes

credits['id'] = credits['movie_id']

merged = pd.merge(credits, movies, left_on=['id', 'title'], right_on=['id', 'title'])
merged.index.rename = ['id']
merged = merged.sort_index()

# drop useless columns and id

merged = merged.drop(columns=['homepage', 'tagline', 'overview', 'id', 'movie_id'])

# =====================================================

# find NaN values and fill them : 1 in release_date, 2 in runtime

# for col in merged.columns:
#   is_nan = merged[col].isna().sum()
#   print(f'{col} : {is_nan}') if is_nan else print('',end='')

merged.fillna({'release_date': '2022-06-10'}, inplace=True) 
merged.fillna({'runtime': int(merged['runtime'].mean())}, inplace=True)


# filter useful parts 

# print(merged.nunique()) # Observe that there are only 3 unique values in 'status'
# print(merged['status'].value_counts())
# 4795 Released, 5 rumored, 3 post production -- drop the latter two

merged = merged[merged['status']=='Released']

# =====================================================

# create new dataframes for 'genre', 'production', 'cast'

def get_genre_df(df):
    import json
    genres_dict = {}
    
    for genre_json in df['genres']:
        genres = json.loads(genre_json)
        for genre in genres:
            genres_dict[genre['id']] = genre['name'] # genre= {'id': int, 'name': str}
    
    genre_df = pd.DataFrame.from_dict(data=genres_dict, orient='index').sort_index()
    genre_df.rename(columns={0 : 'name'}, inplace=True)
    return genre_df

# TODO : 'production_companies' dataframe



# TODO : 'cast' dataframe

# =====================================================

# create new columns


# 'year' column

merged['year'] = pd.to_datetime(merged['release_date']).dt.year

# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.countplot(x='year', data=merged)
# plt.xticks(rotation=-90)
# plt.show()


# 'ROI' column

merged_ = merged.loc[merged['budget'] > 0].loc[merged['revenue'] > 0]
merged_['ROI'] = (merged_['revenue'] - merged_['budget']) / merged_['budget'] * 100
merged = merged.join(merged_['ROI'], how='left')
del merged_

