# Document of Project 1

Here is a documentation for the database of usage of music streaming app.
This documentation describes the purpose of the database, its design and ETL process, and some examples of queries.

## Purpose of Database

The purpose is to analyze user activity on our music streaming app.
This database contains data of songs, artists, users, time of listening and songplay.
These data can be analized in order to find what songs are popular, what kinds of songs each user likes, and how frequently users play musics.

## Scheme Design and ETL Process

This database includes one fact table of songplays as wel as four dimension tables of users, songs, artists and time.
The dimension tables can be joined to songplays table using corresponding columns.

### Fact Table

songplays table is defined as below.

|songplay_id|start_time|user_id|level|song_id|artist_id|session_id|location|user_agent|
|-|-|-|-|-|-|-|-|-|-|
|int, primary key|timestamp, not null|text, not null|text|text|text|text|text|text|

### Dimension Tables

songs table is defined as below.

|song_id|title|artist_id|year|duration|
|-|-|-|-|-|
|int, primary key|text|text|int|numeric|

users table is defined as below.

|user_id|first_name|last_name|gender|level|
|-|-|-|-|-|
|text, primary key|text|text|text|text|

artists table is defined as below.

|artist_id|name|location|latitude|longitude|
|-|-|-|-|-|
|text, primary key|text|text|numeric|numeric|

time table is defined as below.

|start_time|hour|day|week|month|year|weekday|
|-|-|-|-|-|-|-|
|timestamp, primary key|int|int|int|int|int|int|

### Codes

- `sql_queries.py` contains queries to drop and create the tables above as well as insert rows into them.
- `create_table.py` drops and creates the tables by using queries in `sql_queries.py`.
- `etl.py` loads the files of songs and logs, process them, and inserts them into the tables using queries in `sql_queries.py`.

### ETL Process

1. Run `create_table.py` and set up the database and tables.
1. Run `etl.py` and inserts data into the tables.

Some columns have unique constraint, therefore queries avoid duplicating the same ids of songs, artists, and times with `on conflict (column) do nothing` option. The tables of songplays and users can be updated with `on conflict (column) do update set level = excluded.level`, because users may change their status of level.

## Examples of Queries

Here you can find a user who played a song and has its log by joining songplays and users, artists and songs tables.

```sql
select p.user_id, u.first_name, u.last_name, s.title, a.name
from songplays p
    join users u
        on p.user_id = u.user_id
    join songs s
        on p.song_id = s.song_id
    join artists a
        on p.artist_id = a.artist_id;

user_id first_name last_name          title  name
     15       Lily      Koch Setanta matins Elena
```

Another example it to calculate the number of songplays per user in a month

```sql
select t.month, user_id, count(song_id)
from songplays p
    join time t on p.start_time = t.start_time
where p.start_time between '2018-11-01 00:00:00' and '2018-11-30 23:59:59'
group by month, user_id;

month user_id count
   11      54     0
   11      98     0
   11      86     0
```
