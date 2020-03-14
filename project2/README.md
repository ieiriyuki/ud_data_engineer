# README.md

## Project Template

To get started with the project, go to the workspace on the next page, where you'll find the project template (a Jupyter notebook file). You can work on your project and submit your work through this workspace.

The project template includes one Jupyter Notebook file, in which:

- you will process the event_datafile_new.csv dataset to create a denormalized dataset
- you will model the data tables keeping in mind the queries you need to run
- you have been provided queries that you will need to model your data tables for
- you will load the data into tables you create in Apache Cassandra and run your queries

### メモ

元データの列情報

```platintext
['artist', 'V1', 'firstName', 'gender', 'itemInSession', 'lastName',
'length', 'level', 'location', 'request', 'operation', 'V11',
'sessionId', 'song', 'http_status', 'V15', 'userId']
```

`shape = (8056, 17)`

- artist が空の行は取り除く
- V1, request, operation, V11, http_status, V15は取り除く
- 結果、`shape = (6821, 11)` になる

できる整形済みファイル

|artist|firstName|gender|itemInSession|lastName|length|level|location|sessionId|song|userId|
|-|-|-|-|-|-|-|-|-|-|-|
|0|1|2|3|4|5|6|7|8|9|10|

## Project Steps

Below are steps you can follow to complete each component of this project.
Modeling your NoSQL database or Apache Cassandra database

- Design tables to answer the queries outlined in the project template
- Write Apache Cassandra CREATE KEYSPACE and SET KEYSPACE statements
- Develop your CREATE statement for each of the tables to address each question
- Load the data with INSERT statement for each of the tables
- Include IF NOT EXISTS clauses in your CREATE statements to create tables only if the tables do not already exist. We recommend you also include DROP TABLE statement for each table, this way you can run drop and create tables whenever you want to reset your database and test your ETL pipeline
- Test by running the proper select statements with the correct WHERE clause

## Build ETL Pipeline

- Implement the logic in section Part I of the notebook template to iterate through each event file in event_data to process and create a new CSV file in Python
- Make necessary edits to Part II of the notebook template to include Apache Cassandra CREATE and INSERT statements to load processed records into relevant tables in your data model
- Test by running SELECT statements after running the queries on your database

## Query 1

Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4

```sql
select
    session_id, item_in_session, artist, song, length
from sessions
where session_id = 338
    and item_in_session = 4;
```
