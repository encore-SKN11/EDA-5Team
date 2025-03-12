import pandas as pd


def preprocess() -> pd.DataFrame:
    """
    Preprocess the data.
    1. Convert CSV file into DataFrames
    2. Merge two dataframes
    3. Drop useless columns.
    4. Fill out NaN values.
    """
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


    # more in this part 


    
    return merged

# =====================================================

# create new dataframes for 'genre', 'production', 'cast'
def get_genre_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    return genre dataframe from original dataframe.
    index : genre id (int)
    column : genre name (str)
    """
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
def get_production_companines_df(df):
    pass


# TODO : 'cast' dataframe
def get_cast_df(df):
    pass

# =====================================================

# create new columns
def add_useful_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add extra columns that are expected to be useful for EDA.
    """
    
    # 'year' column
    df['year'] = pd.to_datetime(df['release_date']).dt.year
    
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    # sns.countplot(x='year', data=merged)
    # plt.xticks(rotation=-90)
    # plt.show()
    
    # 'ROI' column
    
    # Only calculate ROI if 'both' and 'revenue' column values are nonzero.
    df_ = df.loc[df['budget'] > 0].loc[df['revenue'] > 0]
    # calculate ROI value.
    df_['ROI'] = (df_['revenue'] - df_['budget']) / df_['budget'] * 100
    # join into original df
    df = df.join(df_['ROI'], how='left')
    del df_

    # more on this part...

    
    return df

