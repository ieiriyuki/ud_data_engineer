import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events;"
staging_songs_table_drop = "drop table if exists staging_songs;"
songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"

# CREATE TABLES

staging_events_table_create= ("""create table if not exists staging_events (
    artist          text,
    auth            text,
    first_name      text,
    gender          text,
    item_in_session int,
    last_name       text,
    length          numeric,
    level           text,
    location        text,
    method          text,
    page            text,
    registration    bigint,
    session_id      int,
    song            text,
    status          int,
    ts              bigint,
    user_agent      text,
    user_id         int
)
diststyle even;
""")

staging_songs_table_create = ("""create table if not exists staging_songs (
    num_songs       int,
    artist_id       text,
    latitude        numeric,
    longitude       numeric,
    artist_location text,
    artist_name     text,
    song_id         text,
    title           text,
    duration        numeric,
    year            int
)
diststyle even;
""")

songplay_table_create = ("""create table if not exists songplays (
    songplay_id int       not null generated by default as identity (0, 1) primary key,
    start_time  timestamp not null,
    user_id     text      not null,
    level       text,
    song_id     text,
    artist_id   text,
    session_id  text,
    location    text,
    user_agent  text
)
diststyle even
sortkey (user_id, song_id, artist_id);
""")

user_table_create = ("""create table if not exists users (
    user_id    text not null distkey primary key,
    first_name text,
    last_name  text,
    gender     text,
    level      text
)
diststyle key;
""")

song_table_create = ("""create table if not exists songs (
    song_id   text not null distkey primary key,
    title     text,
    artist_id text sortkey,
    year      int,
    duration  numeric
)
diststyle key;
""")

artist_table_create = ("""create table if not exists artists (
    artist_id text not null distkey primary key,
    name      text,
    location  text,
    latitude numeric,
    longitude numeric
)
diststyle key;
""")

time_table_create = ("""create table if not exists time (
    start_time timestamp not null distkey sortkey primary key,
    hour       int,
    day        int,
    week       int,
    month      int,
    year       int,
    weekday    int
)
diststyle key;
""")

# STAGING TABLES

ARN = config.get("IAM_ROLE", "ARN")

LOG_DATA = config.get("S3", "LOG_DATA")
LOG_PATH = config.get("S3", "LOG_JSONPATH")
staging_events_copy = ("""copy staging_events
from {}
iam_role {}
region 'us-west-2'
json {}
""").format(LOG_DATA, ARN, LOG_PATH)

SONG_DATA = config.get("S3", "SONG_DATA")
staging_songs_copy = ("""copy staging_songs
from {}
iam_role {}
region 'us-west-2'
json 'auto'
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""insert into songplays
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
select
    timestamp 'epoch' + e.ts * interval '1 second',
    e.user_id,
    e.level,
    s.song_id,
    s.artist_id,
    e.session_id,
    e.location,
    e.user_agent
from
    staging_events e
join
    staging_songs s
    on
        e.artist = s.artist_name
        and e.song = s.title
        and e.length = s.duration
where
    e.page like 'NextSong'
    and e.ts is not null
    and e.user_id is not null
""")

user_table_insert = ("""insert into users
(user_id, first_name, last_name, gender, level)
select
    user_id,
    first_name,
    last_name,
    gender,
    level
from
    staging_events e
where
    user_id is not null
""")

song_table_insert = ("""insert into songs
(song_id, title, artist_id, year, duration)
select
    song_id,
    title,
    artist_id,
    year,
    duration
from
    staging_songs s
where
    song_id is not null
""")

artist_table_insert = ("""insert into artists
(artist_id, name, location, latitude, longitude)
select
    artist_id,
    artist_name,
    artist_location,
    latitude,
    longitude
from
    staging_songs s
where
    s.artist_id is not null
""")

time_table_insert = ("""insert into time
(start_time, hour, day, week, month, year, weekday)
select
    start_time,
    extract(h from start_time),
    extract(d from start_time),
    extract(w from start_time),
    extract(mon from start_time),
    extract(y from start_time),
    extract(dw from start_time)
from (
    select
        timestamp 'epoch' + ts * interval '1 second' start_time
    from
        staging_events
    where
        start_time is not null
    ) t
;
""")

select_songplays = ("""select *
from songplays
where songplay_id is not null
limit 2
""")

select_users = ("select * from users limit 2")

select_songs = ("select * from songs limit 2")

select_artists = ("select * from artists limit 2")

select_time = ("select * from time limit 2")
# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
test_tables = [select_songplays, select_users, select_artists, select_time]
