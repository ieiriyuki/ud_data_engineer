# Document of Project 4 : Data Pipelines with Airflow

## Overview

This document describes the data warehouse for a music streaming app and its Data pipelines of ETL processes. Amazon Redshift and Apache Airflow are adopted for data warehouse and a data pipelines tool respectively, and raw data is stored in Amazon S3.

## Data
Raw log and song data are stored in the location below.

- Log data: `s3://udacity-dend/log_data`
- Song data: `s3://udacity-dend/song_data`

## Data Pipelines

## Tables

### Fact Table

**songplays**

|songplay_id|start_time|user_id|level|song_id|artist_id|session_id|location|user_agent|
|-|-|-|-|-|-|-|-|-|
|int, primary key|timestamp, not null|text, not null|text|text|text|int|text|text|

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

## Query examples

*if any*

# Memo

## Project: Data Pipelines with Airflow

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

## Project Overview

We have provided you with a project template that takes care of all the imports and provides four empty operators that need to be implemented into functional pieces of a data pipeline. The template also contains a set of tasks that need to be linked to achieve a coherent and sensible data flow within the pipeline.

You'll be provided with a helpers class that contains all the SQL transformations. Thus, you won't need to write the ETL yourselves, but you'll need to execute it with your custom operators.

<img src="./images/example-dag.png" title="example of dag">

## Datasets

### Project Template

The project template package contains three major components for the project:
The dag template has all the imports and task templates in place, but the task dependencies have not been set

- The dag template has all the imports and task templates in place, but the task dependencies have not been set
- The operators folder with operator templates
- A helper class for the SQL transformations

### Configuring the DAG

In the DAG, add default parameters according to these guidelines

- The DAG does not have dependencies on past runs
- On failure, the task are retried 3 times
- Retries happen every 5 minutes
- Catchup is turned off
- Do not email on retry

In addition, configure the task dependencies so that after the dependencies are set, the graph view follows the flow shown in the image below.

<img src="./images/example-dag.png" title="">

### Building the operators

To complete the project, you need to build four different operators that will stage the data, transform the data, and run checks on data quality.

All of the operators and task instances will run SQL statements against the Redshift database. However, using parameters wisely will allow you to build flexible, reusable, and configurable operators you can later apply to many kinds of data pipelines with Redshift and with other databases.
Stage Operator

The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.
Fact and Dimension Operators

With dimension and fact operators, you can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation.

Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, you could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.
Data Quality Operator

The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.

For example one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.
Note about Workspace
