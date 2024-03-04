# Packages
import pandas as pd
import pytz
import logging
from sqlalchemy import create_engine

# Modules
from Data_Parser.parse import parse_tweets

# Convert to utc time
def safely_localize_to_utc(series, timezone=pytz.UTC):
    if hasattr(series.iloc[0], 'tz') and series.iloc[0].tz:  # if already timezone-aware
        return series.dt.tz_convert(timezone)
    else:
        return series.apply(lambda x: x.tz_localize(timezone) if pd.notna(x) else x)

# organize tweets data
def get_dataframe(page_sources_1, page_sources_2,query_wordstring, query_kol):
    all_tweets = []
    for page_source in page_sources_1:
        tweets_info = parse_tweets(page_source,query_wordstring, query_kol)
        if tweets_info is not None:
            all_tweets.append(tweets_info)
    for page_source in page_sources_2:
        tweets_info = parse_tweets(page_source,query_wordstring, query_kol)
        if tweets_info is not None:
            all_tweets.append(tweets_info)
    if len(all_tweets) > 0:
        all_tweets_ = [item for sublist in all_tweets for item in sublist]
        tweets_df = pd.DataFrame(all_tweets_, columns = ['username', 'text','date', 'replies', 'reposts', 'likes', 'bookmarks','views','query_wordstring','query_kol','language'])
        tweets_df['date'] = pd.to_datetime(tweets_df['date'])
        tweets_df.sort_values(by = 'date',ascending = False, inplace = True)
        tweets_df = tweets_df.drop_duplicates(subset=['text','date','username','query_wordstring','query_kol']) 
        return tweets_df

def save_to_database(sql_connector, tweets_df, database_tosave, post_counter, counter_lock):
    engine = create_engine(sql_connector)
    tweets_df['date'] = safely_localize_to_utc(tweets_df['date'])
    try:
        existing_data_query = f"SELECT username, text, date, query_wordstring FROM {database_tosave}"
        existing_data = pd.read_sql(existing_data_query, engine)
        existing_data['date'] = safely_localize_to_utc(existing_data['date'])
        # Merge dataframes
        merged = pd.merge(tweets_df, existing_data, on=['username', 'text', 'date', 'query_wordstring'], how='left', indicator=True)

        # Rows to insert
        to_insert = merged[merged['_merge'] == 'left_only'][tweets_df.columns]

        # Rows to potentially update
        to_update = merged[merged['_merge'] == 'both']

        # Update only if the other columns differ
        for index, row in to_update.iterrows():
            # Fetch the existing row from the database
            existing_row = pd.read_sql(f"SELECT * FROM {database_tosave} WHERE username = %s AND text = %s AND date = %s AND query_wordstring = %s AND query_kol = %s", engine, params=(row['username'], row['text'], row['date'], row['query_wordstring'], row['query_kol'])).iloc[0]
            # Compare the non-key columns and update if they differ
            if not (existing_row['likes'] == row['likes'] and existing_row['reposts'] == row['reposts'] and existing_row['views'] == row['views'] and existing_row['replies'] == row['replies'] and existing_row['bookmarks'] == existing_row['bookmarks']):
                update_query = f"""
                UPDATE {database_tosave} SET
                replies = %s,
                retweets = %s,
                likes = %s,
                bookmarks = %s,
                views = %s
                WHERE username = %s AND text = %s AND date = %s
                """
                engine.execute(update_query, (row['replies'], row['retweets'], row['likes'], row['bookmarks'], row['views'], row['username'], row['text'], row['date']))

        # Insert new rows
        with counter_lock:
            post_counter.value += len(to_insert)
        to_insert.to_sql(name=database_tosave, con=engine, index=False, if_exists='append')
        logging.critical("Data insert to database: %s for %d tweets", database_tosave, len(to_insert))

        engine.dispose()
    except:
        with counter_lock:
            post_counter.value += len(to_insert)
        tweets_df.to_sql(name=database_tosave, con=engine, index=False, if_exists='append')
        logging.critical("Data append to database: %s for %d tweets", database_tosave, len(tweets_df))
        engine.dispose()