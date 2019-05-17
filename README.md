# Data Modeling with PostgreSQL on Sparkify Data


__Sparkify__, a startup music streaming company, wanted to analyze their data they've collected on song and user activity on their music streaming application. The analytics team would like to find out what songs are users listening to most, but currently there is no way for the analytics team to query their data. Their data currently resides in a directory of json logs on user activity on the app, and json metadata on their songs. This pipeline and data model were created to make analyzing the data easier for the analytics team.

### Schema:       
The Fact and dimension tables are defined with a star schema optimized for queries on song play analysis.

#### Fact Table:      
__songplays__ - records in log data associated with song plays i.e. records with page ___NextSong___       
    -_songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent_       

### Dimension Tables:     
__users__ - users in the app    
    - _user_id, first_name, last_name, gender, level_    
__songs__ - songs in music database     
    - _song_id, title, artist_id, year, duration_     
__artists__ - artists in music database     
    - _artist_id, name, location, lattitude, longitude_       
__time__ - timestamps of records in songplays broken down into specific units     
    - _start_time, hour, day, week, month, year, weekday_   


Running files:
1. Run ___create_tables.py___ to create the database and tables.
2. Run ___etl.py___ to populate the database with sparkifys data.
3. You can also run ___test.ipynb___ to verify that the data is being uploaded correctly.

#### To run these files you need to have PostgreSQL installed.
