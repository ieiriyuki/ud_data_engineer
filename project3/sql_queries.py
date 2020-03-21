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

staging_songs_table_create = ("""create table if not exists staging_songs (
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

songplay_table_create = ("""create table if not exists songplays (
    songplay_id int       not null identity(0, 1) distkey primary key,
    start_time  timestamp not null,
    user_id     text      not null sortkey,
    level       text,
    song_id     text      sortkey,
    artist_id   text      sortkey,
    session_id  text,
    location    text,
    user_agent  text
)
diststyle even;
""")

user_table_create = ("""create table if not exists users (
    user_id    text key not null distkey primary,
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
    artist_id text,
    year      int,
    duration  numeric
)
diststyle key;
""")

artist_table_create = ("""create table if not exists artists (
    artist_id text not null distkey primary key,
    name      text,
    location  text,
    lattitude numeric,
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
LOG_PATH=config.get("S3", "LOG_JSONPATH")
staging_events_copy = ("""copy staging_events
from '{}'
iam_role '{}'
json
region 'us-west-2'
""").format(LOG_PATH, ARN)

SONG_DATA=config.get("S3", "SONG_DATA")
staging_songs_copy = ("""copy staging_songs
from '{}'
iam_role '{}'
json
region 'us-west-2'
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""insert into songplays (
    select
        *
    from
        staging_events e
    join
        staging_songs s
        on
)
""")

user_table_insert = ("""insert into users (
    select
        *
    from
        staging_events e
    join
        staging_songs s
        on
)
""")

song_table_insert = ("""insert into songs (
    select
        *
    from
        staging_events e
    join
        staging_songs s
        on
)
""")

artist_table_insert = ("""insert into artists (
    select
        *
    from
        staging_events e
    join
        staging_songs s
        on
)
""")

time_table_insert = ("""insert into time (
    select
        *
    from
        staging_events e
    join
        staging_songs s
        on
)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

songplay_table_create = ("""
create table if not exists songplays (
    songplay_id serial primary key,
    start_time timestamp not null,
    user_id int not null,
    level text,
    song_id text,
    artist_id text,
    session_id int,
    location text,
    user_agent text
);
""")

user_table_create = ("""
create table if not exists users (
    user_id int primary key,
    first_name text,
    last_name text,
    gender text,
    level text
);
""")

song_table_create = ("""
create table if not exists songs (
    song_id text primary key,
    title text,
    artist_id text,
    year int,
    duration numeric
);
""")

artist_table_create = ("""
create table if not exists artists (
    artist_id text primary key,
    name text,
    location text,
    latitude numeric,
    longitude numeric
);
""")

time_table_create = ("""
create table if not exists time (
    start_time timestamp primary key,
    hour int,
    day int,
    week int,
    month int,
    year int,
    weekday int
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
insert into songplays
(songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
on conflict (songplay_id) do update set level = excluded.level;
""")

user_table_insert = ("""
insert into users
(user_id, first_name, last_name, gender, level)
values (%s, %s, %s, %s, %s)
on conflict (user_id) do update set level = excluded.level;
""")

song_table_insert = ("""
insert into songs
(song_id, title, artist_id, year, duration)
values (%s, %s, %s, %s, %s)
on conflict (song_id) do nothing;
""")

artist_table_insert = ("""
insert into artists
(artist_id, name, location, latitude, longitude)
values (%s, %s, %s, %s, %s)
on conflict (artist_id) do nothing;
""")

time_table_insert = ("""
insert into time
(start_time, hour, day, week, month, year, weekday)
values (%s, %s, %s, %s, %s, %s, %s)
on conflict (start_time) do nothing;
""")
