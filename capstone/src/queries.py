
create_table_queries = """
begin;

drop table if exists stage_retail;
create table if not exists stage_retail (
    invoice text,
    stockcode text,
    description text,
    quantity int,
    invoicedate timestamp,
    price float,
    customerid float,
    country text
);

drop table if exists stage_rate;
create table if not exists stage_rate (
    "date" date,
    "usd" float,
    "open" float,
    "high" float,
    "low" float,
    "pct_change" text
);

drop table if exists stage_weather;
create table if not exists stage_weather (
    city text,
    latitude float,
    longitude float,
    temperature float,
    temperature_min float,
    temperature_max float,
    feel_like float,
    pressure float,
    humidity float,
    wind_speed float,
    wind_degree float,
    clouds text,
    weather_id int,
    weather text,
    description text,
    weather_icon text,
    dt bigint,
    dt_iso timestamp,
    timezone int
);

drop table if exists retail;
create table if not exists retail (
    invoice text not null,
    stockcode text,
    description text,
    quantity int,
    invoicedate timestamp not null,
    price float,
    customerid int,
    country text
)
diststyle key
distkey ( customerid )
sortkey ( invoice, invoicedate )
;

drop table if exists rate;
create table if not exists rate (
    "date" date not null,
    "usd" float not null,
    "open" float,
    "high" float,
    "low" float,
    "pct_change" float
)
diststyle key
distkey ( "date" )
sortkey ( "date" )
;

drop table if exists weather;
create table if not exists weather (
    city text not null,
    latitude float,
    longitude float,
    temperature float not null,
    temperature_min float,
    temperature_max float,
    feel_like float,
    pressure float,
    humidity float,
    wind_speed float,
    wind_degree float,
    clouds text,
    weather text not null,
    description text,
    dt bigint not null,
    dt_iso timestamp not null,
    timezone int
)
diststyle key
distkey ( dt )
sortkey ( dt )
;

commit;
"""

copy_template = """
copy {}
from '{}'
access_key_id '{}'
secret_access_key '{}'
{}
"""

insert_template = """
insert into {}
{}
"""

select_retail_query = """
select
    invoice,
    stockcode,
    description,
    quantity,
    invoicedate,
    price,
    cast(customerid as int),
    country
from
    stage_retail
where
    invoice is not null
    and invoicedate is not null
"""

select_rate_query = """
select
    "date",
    "usd",
    "open",
    "high",
    "low",
    cast(replace(pct_change, '%', '') as float)
from
    stage_rate
where
    "date" is not null
    and "usd" is not null
"""

select_weather_query = """
select
    city,
    latitude,
    longitude,
    temperature,
    temperature_min,
    temperature_max,
    feel_like,
    pressure,
    humidity,
    wind_speed,
    wind_degree,
    clouds,
    weather,
    description,
    dt,
    dt_iso,
    timezone
from
    stage_weather
where
    city is not null
    and temperature is not null
    and weather is not null
    and dt is not null
    and dt_iso is not null
"""

validate_retail_query = """
select
    count(1) as cnt,
    count(distinct invoice) as ctd_invoice,
    count(distinct invoicedate) as cnt_invdt
from
    retail
"""

validate_rate_query = """
select
    count(1) as cnt,
    count(distinct "date") as ctd_date,
    count(distinct usd) as ctd_usd
from
    rate
"""

validate_weather_query = """
select
    count(1) as cnt,
    count(distinct city) as ctd_city,
    count(distinct dt) as ctd_dt
from
    weather
"""

select_queries = [select_retail_query, select_rate_query, select_weather_query]
validate_queries = [validate_retail_query, validate_rate_query, validate_weather_query]
