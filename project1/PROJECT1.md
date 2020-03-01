# Project 1

Million Songs Data set をテーブルに格納する。

JSONファイルになっている。

曲データとメタデータがある。

# Scheme

スタースキーマ

## Fact Table: songplays
- songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

## Dimension
- users
    - user_id, first_name, last_name, gender, level
- songs
    - song_id, title, artist_id, year, duration
- artists
    - artist_id, name, location, latitude, longitude
- time
    - start_time, hour, day, week, month, year, weekday

## Template

- `test.ipynb` displays the first few rows of each table to let you check your database.
- `create_tables.py` drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.
- `etl.ipynb` reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
- `etl.py` reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.
- `sql_queries.py` contains all your sql queries, and is imported into the last three files above.
- `README.md` provides discussion on your project.

## Steps

### Create Tables

1. Write CREATE statements in sql_queries.py to create each table.
2. Write DROP statements in sql_queries.py to drop each table if it exists.
3. Run create_tables.py to create your database and tables.
4. Run test.ipynb to confirm the creation of your tables with the correct columns. Make sure to click "Restart kernel" to close the connection to the database after running this notebook.

### Build ETL Processes

Follow instructions in the etl.ipynb notebook to develop ETL processes for each table. At the end of each table section, or at the end of the notebook, run test.ipynb to confirm that records were successfully inserted into each table. Remember to rerun create_tables.py to reset your tables before each time you run this notebook.

### Build ETL Pipeline

Use what you've completed in etl.ipynb to complete etl.py, where you'll process the entire datasets. Remember to run create_tables.py before running etl.py to reset your tables. Run test.ipynb to confirm your records were successfully inserted into each table.

### Document Process

Do the following steps in your README.md file.

1. Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
1. State and justify your database schema design and ETL pipeline.
1. [Optional] Provide example queries and results for song play analysis.
