import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function processes the song files and inserts the data into the postgres database as tables.

    Args:
        cur (psql cursor): connection cursor for postgres db.
        filepath (str): path to the song files.

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function processes the log files and inserts the data into the postgres database as tables.

    Args:
        cur (psql cursor): connection cursor for postgres db.
        filepath (str): path to the log files.

    Returns:
        None
    """

    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df.page == 'NextSong'].reset_index(drop=True)

    # convert timestamp column to datetime
    t = df.copy()
    t['ts'] = pd.to_datetime(t['ts'], unit='ms')

    # insert time data records
    time_data = (t.ts, t.ts.dt.hour, t.ts.dt.day, t.ts.dt.week, t.ts.dt.month, t.ts.dt.year, t.ts.dt.weekday)
    column_labels = ('start_time','hour', 'day', 'week', 'month', 'year', 'weekday')
    dict_t = dict(zip(column_labels,time_data))
    time_df = pd.DataFrame(dict_t)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.drop_duplicates().iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        start_time = pd.to_datetime(row.ts, unit='ms')
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song.encode('utf-8'), row.artist.encode('utf-8'), row.length))
        results = cur.fetchone()
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (start_time, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function processes the song and log files and inserts the data into the postgres database.

    Args:
        conn (psql connection): connection for postgres db using psycopg2.
        filepath (str): path to the files.
        cur (psql cursor): connection cursor for postgres db.
        func (python function): function used for processing song or log files.

    Returns:
        None
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Main function to connect to postgres and process all the data int the etl pipeline to create the star scheme database.

    Args:
        None

    Returns:
        None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
