# Document for Capstone Project of Data Engineer Nano Degree

This document describes the data model of my capstone project and the process of its ETL.

# Purpose

The sales data of online retail store is used here.
This is because online stores are getting more and more popular thesedays, and hence it is important to analyze their data for their growth.
Possible analyses are the amount of sales per day, the total sold price per item, and the total sold price per customer.

# Data

Three data are included. One is the sales data of online retail store which is based on United Kingdom. Customers are not only in U.K. but also in other places such as France. Therefore, the exchange rate between GBP and USD is incorporated in database to investigate the effect of exchange rate on retail sales. The weather data in London is also included because online shopping would be affected by weather.

1. `online_retail_II.csv`: The sales data of a online retail store is obtained from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II). This data contains 1,067,371 rows and 8 columns.
1. `GBP_USD_Historical_Data.csv`: The exchange price data between GBP and USD comes from [Investing.com](https://www.investing.com/). This include 782 rows and 6 columns.
1. `London_weather_N.json`: The weather information in London is aquired from [OpenWeather](https://openweathermap.org/).
    - The original file consists of 26,280 rows and 19 columns and its size is about 9MB.
    - Redshift does not accept to read more than 4MB JSON file ([link](https://forums.aws.amazon.com/thread.jspa?threadID=216796)).
    - Therefore it is splited into three files.

# Data model

Here data model is assumed as below.
There are three services, the online store, the exchange market, and the weather report.
Each service produces their raw data, and these raw data have to be processed for datamart as describe here.

<img src="images/datamodel.png" width="640">

Star schema is adopted here, because just three kinds of data exist and joining them is not so intensive.
A simple model should be more useful than sophisticated ones in this situation.

# Tables

Three tables created are explained here.
All the data are sorts of timeseries data, so they can be combined with their date or timestamp columns.

## Fact Table
**retail**
|invoice|stockcode|description|quantity|invoicedate|price|customerid|country|
|-|-|-|-|-|-|-|-|
|text not null|text|text|int|timestamp not null|float|int|text|

## Dimension Table
**rate**

|date|usd|open|high|low|pct_change|
|-|-|-|-|-|-|
|date not null|float not null|float|float|float|float|

**weather**
|city|latitude|longitude|temperature|temperature_min|temperature_max|feel_like|pressure|humidity|wind_speed|wind_degree|clouds|weather|description|dt|dt_iso|timezone|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|text not null|float|float|float not null|float|float|float|float|float|float|float|text|text not null|text|bigint not null|timestamp not null|int|

# ETL Tools and Processes

Raw data are stored in Amazon S3 and Amazon Redshift is used for Data Warehouse.
This is because both are scalable for the increase of data size, and they are integrated to each other well.
This make it easy to load data into Data Warehouse from storage and to analyize data seemlessly.

## ETL scripts

Here, scripts for ETL are introduced.

- `etl.py` does the actual ETL processes. Main steps are
  1. Create tables
  1. Load raw data into staging tables
  1. Insert relevant data from staging tables into datamart
  1. Validate data and check the numbers of rows, distinct values, etc
- `queries.py` denotes queries to create tables and load data into them. These queries are imported by `etl.py`.
- `params.cfg` contains values necessary for such as data retrieval and connection to Redshift.

### Directory of Source Codes

```bash
capstone
  ├src
  |  ├etl.py
  |  └queries.py
  ├images
  |  └image.png
  ├params.cfg
  └README.md
```

### S3 Bucket structure

```bash
bucket
  ├online_retail_II.csv
  ├GBP_USD_Historical_Data.csv
  ├weather
  |  ├London_weather_0.json
  |  ├London_weather_1.json
  |  └London_weather_2.json
  └weather_json_path.json
```

# Future Work

- The data was increased by 100x.
- The pipelines would be run on a daily basis by 7 am every day.
- The database needed to be accessed by 100+ people.

# Rubrics

## Data Model

- The ETL processes result in the data model outlined in the write-up.
- A data dictionary for the final data model is included.
- The data model is appropriate for the identified purpose.

## Suggestions

To make your project stand out:

- Work with large amounts of data.
- Combine datasets that are difficult to combine.
- Enrich the data from several disparate sources.
- Include recommendations for how to use to data to come up with insights.
- Write a blog post about your project and link to it.
