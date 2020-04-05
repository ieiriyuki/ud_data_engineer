# Documentation for Project 4: Data Lake

This document describes the databases of music app, their schemas and their ETL processes using Spark on Amazon EMR.

## Data Lake Setup

Spark is built on Amazon EMR, and transformed data as well as raw data are stored in Amazon S3.

## ETL Process

To start ETL process, please run `etl.py`, which retrieves raw data of songs and logs from S3, transform them to tables below, and save these tables as parquet format into S3.
`dl.cfg` includes information of AWS access keys.

## Tables

The schemas of tables are explained below.

### Fact Table

**songplays**

|songplay_id|start_time|user_id|level|song_id|artist_id|session_id|location|user_agent|year|month|
|-|-|-|-|-|-|-|-|-|-|-|
|int, not null|timestamp|text|text|text|text|int|text|text|int, partition|int, partition|

### Dimension Tables

**users**

|user_id|first_name|last_name|gender|level|
|-|-|-|-|-|
|text, not null|text|text|text|text|

**songs**

|song_id|title|artist_id|year|duration|
|-|-|-|-|-|
|text, not null|text|text, partition|int, partition|numeric|

**artists**

|artist_id|name|location|latitude|longitude|
|-|-|-|-|-|
|text, not null|text|text|numeric|numeric|

**time**

|start_time|hour|day|week|month|year|weekday|
|-|-|-|-|-|-|-|
|timestamp|int|int|int|int, partition|int, partition|int|
