# Documentation of Redshift Database

This document describes the ETL process to create the database of music app and its scheme.

## Data

The original data of JSON formatted are stored in S3, and those are loaded into Redshift

- Song data: `s3://udacity-dend/song_data`
- Log data: `s3://udacity-dend/log_data`
- Log data json path: `s3://udacity-dend/log_json_path.json`

## ETL Process

The original data are retrieved from S3 and loaded into staging tables in Redshift. The staging tables are transformed to tables below.

### Scripts
- `dwh.cfg` contains the information of the Redshift, IAM, S3
- `sql_queries.py` contains queries to drop, create, insert into and check the tables.
- `create_table.py` sets up tables using queries in `sql_queries.py`
- `etl.py` retrieve data from S3, insert them into staging tables, and insert formatted data into the final tables from staging ones.

To create databse, run `create_table.py` first and then `etl.py`.

## Tables

The ETL process above creates the tables below.

### Fact Table

**songplays**

|songplay_id|start_time|user_id|level|song_id|artist_id|session_id|location|user_agent|
|-|-|-|-|-|-|-|-|-|
|int, primary key|timestamp, not null|text, not null|text|text|text|int|text|text|

This table will be used joining other tables, therefore user_id, song_id and artist_id are defined as sortkey to be joined efficiently.

### Dimension Tables

**users**

|user_id|first_name|last_name|gender|level|
|-|-|-|-|-|
|text, primary key|text|text|text|text|

**songs**

|song_id|title|artist_id|year|duration|
|-|-|-|-|-|
|text, primary key|text|text|int|numeric|

**artists**

|artist_id|name|location|lattitude|longitude|
|-|-|-|-|-|
|text, primary key|text|text|numeric|numeric|

**time**

|start_time|hour|day|week|month|year|weekday|
|-|-|-|-|-|-|-|
|timestamp, primary key|int|int|int|int|int|int|

## Query Examples

Here shows some examples of queries to the created tables.

```sql
select
    count(1),
    count(distinct songplay_id),
    count(distinct user_id),
    count(distinct song_id),
    count(distinct artist_id)
from songplays;
     0    1   2    3    4
0  320  320  55  210  194
```

```sql
select
    distinct songplay_id,
    p.user_id,
    first_name,
    last_name,
    p.song_id,
    title,
    p.artist_id,
    name
from songplays p
join users u
    on p.user_id = u.user_id
join songs s
    on p.song_id = s.song_id
join artists a
    on p.artist_id = a.artist_id
limit 3;
     0   1       2        3                   4                      5                   6           7
0  298  44  Aleena    Kirby  SOAFQGA12A8C1367FA    I'm Still Breathing  AR0IVTL1187B9AD520  Katy Perry
1   14  55  Martin  Johnson  SOXQYSC12A6310E908  Bitter Sweet Symphony  AR0L04E1187B9AE90C   The Verve
2  265  95    Sara  Johnson  SOHTQAS12A6701C7BA                  Crazy  AR12F2S1187FB56EEF   Aerosmith
```

```sql
select count(1), count(distinct user_id) from users;
    0   1
0  97  97
```

```sql
select count(1), count(distinct song_id) from songs;
       0      1
0  14896  14896
```

```sql
select count(1), count(distinct artist_id) from artists;
       0     1
0  10021  9553
```

```sql
select * from time limit 3;
                    0   1  2   3   4     5  6
0 2018-11-01 20:57:10  20  1  44  11  2018  4
1 2018-11-01 21:01:46  21  1  44  11  2018  4
2 2018-11-01 21:01:46  21  1  44  11  2018  4
```

