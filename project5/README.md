# Document of Project 4 : Data Pipelines with Airflow

## Overview

This document describes the data warehouse of a music streaming app and its data pipelines of ETL processes. Amazon Redshift and Apache Airflow are adopted for the data warehouse and the tool of data pipelines respectively. Raw data is stored in Amazon S3.

## Data Pipelines

Data Pipelines built on Apache Airflow operate data retrieving from S3, load them to tables, and quality check on the tables.
Pipelines consists of some processes below.

1. **Begin execution**: DummyOperator to indicate the start of pipelines
1. **Staging operation**: Using StageToRedshiftOperator, these operations load log and song data in S3 to staging tables
1. **Load songplays**: Insert data into the fact table of songplays from staging tables
1. **Load dimension tables**: Insert data into the dimension tables of users, artists, songs and time
1. **Data Quality check**: Count the numbers of rows and distinct keys in the tables
1. **End execution**: DummyOperator to represent the end of pipelines

## Execution of Data Pipelines
To execute data pipelines, run the commands below.

```bash
airflow initdb  # This initialize database for airflow
airflow scheduler  # This starts the scheduler for task execution
airflow webserver  # This creates GUI webserver and starts task execution
```

## Directory and Files

```bash
${AIRFLOW_HOME}
  ├dags
  |  └udac_example_dag.py
  ├plugins
  |  ├operators
  |  |  ├data_quality.py
  |  |  ├load_dimension.py
  |  |  ├load_fact.py
  |  |  └stage_redshift.py
  |  └helpers
  |     └sql_queries.py
  ├create_tables.sql
  └README.md
```

- `udac_example_dag.py` contains main dag, tasks and its dependency of data pipelines.
- `stage_redshift.py` includes StageToRedshiftOperator to load raw log and song data to staging tables.
- `load_fact.py` has LoadFactOperator to append fact data to the fact table.
- `load_dimension.py` denotes LoadDimensionOperator to insert data to the dimension tables.
- `data_quality.py` defines an operator to validate data in the tables.
- `sql_queries.py` stores queries to insert data into the fact and dimension tables from staging ones.
- `create_tables.sql` is sql file to create staging, fact and dimensions tables.
- `README.md` represents this document of data pipelines.

## Configuration

The DAG of Airflow requires some parameters.
These are defined by Airflow GUI as well as environment variables.

|Key|Value|Environment Variable|
|-|-|-|
|s3_bucket|udacity-dend|AIRFLOW_VAR_S3_BUCKET=udacity-dend|
|region|us-west-2|AIRFLOW_VAR_REGION=us-west-2|
|logdata|log_data|AIRFLOW_VAR_LOGDATA=log_data|
|logpath|log_json_path.json|AIRFLOW_VAR_LOGPATH=log_json_path.json|
|songdata|song_data|AIRFLOW_VAR_SONGDATA=song_data|

Connection also has to be set to access Amazon Redshift.
This connection can be defined by GUI or environmental variable too.
An example is shown below.

|Conn Id|Conn Type|Login|Password|Host|Port|Schema|Environment Variable|
|-|-|-|-|-|-|-|-|
|redshift_conn_id|postgres|awsuser|password|your-cluster-host|5439|dev|AIRFLOW_CONN_REDSHIFT_CONN_ID=postgres://awsuser:password@your-cluster-host:5439/dev|
|aws_conn_id|aws|your-access-key|your-secret-key||||AIRFLOW_CONN_AWS_CONN_ID=aws://your-access-key:your-secret-key@|

## Data
Raw log and song data are stored in S3 buckets below.

- Log data: `s3://udacity-dend/log_data`
- Song data: `s3://udacity-dend/song_data`

A JSON file, `s3://udacity-dend/log_json_path.json`, is also used to load the data format of log data properly.

## Tables
Tables below are created by the pipelines.

### Fact Table

**songplays**

|playid|start_time|userid|level|songid|artistid|sessionid|location|user_agent|
|-|-|-|-|-|-|-|-|-|
|int, primary key|timestamp, not null|text, not null|text|text|text|int|text|text|

### Dimension Tables

**users**

|userid|first_name|last_name|gender|level|
|-|-|-|-|-|
|text, primary key|text|text|text|text|

**songs**

|songid|title|artistid|year|duration|
|-|-|-|-|-|
|text, primary key|text|text|int|numeric|

**artists**

|artistid|name|location|lattitude|longitude|
|-|-|-|-|-|
|text, not null|text|text|numeric|numeric|

**time**

|start_time|hour|day|week|month|year|weekday|
|-|-|-|-|-|-|-|
|timestamp, primary key|int|int|int|text|int|text|
