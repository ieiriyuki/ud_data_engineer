# Documentation of Redshift Database

This is ...

## Tables

**Fact Table**

songplays

|songplay_id|start_time|user_id|level|song_id|artist_id|session_id|location|user_agent|
|-|-|-|-|-|-|-|-|-|
|int, primary key|timestamp, not null|text, not null|text|text|text|int|text|text|

**Dimension Tables**

users

|user_id|first_name|last_name|gender|level|
|-|-|-|-|-|
|text, primary key|text|text|text|text|

songs

|song_id|title|artist_id|year|duration|
|-|-|-|-|-|
|text, primary key|text|text|int|numeric|

artists

|artist_id|name|location|lattitude|longitude|
|-|-|-|-|-|
|text, primary key|text|text|numeric|numeric|

time

|start_time|hour|day|week|month|year|weekday|
|-|-|-|-|-|-|-|
|timestamp, primary key|int|int|int|int|int|int|

## B
