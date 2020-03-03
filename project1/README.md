# Documentation: Project 1

Here is a documentation for the database of usage of music streaming app.
This documentation describes the purpose of the database, its design and ETL process, and some examples of queries.

## Purpose of Database

We would like to analyze user activity on our music streaming app.
This database contains data of songs, artists, users, time of listening and songplay.
These data can be analized in order to reveal what songs are popular, what kinds of songs each user likes, and how frequently users play musics.

## Scheme Design and ETL Process

This database includes one fact table of songplays as wel as four dimension tables of users, songs, artists and time.
The dimension tables can be joined to songplays table using corresponding columns.

When we insert data, we avoid duplicating the same  information of songs, artists and users by adding `on confilct (column) do nothing` to queries.

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
        on p.artist_id = a.artist_id
limit 1;

> user_id first_name last_name          title  name
>      15       Lily      Koch Setanta matins Elena
```
