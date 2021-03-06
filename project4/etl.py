#!/usr/bin/env python

import configparser
import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import row_number
from pyspark.sql.functions import (year,
                                   month,
                                   dayofmonth,
                                   hour,
                                   weekofyear,
                                   date_format,
                                   from_unixtime,
                                   desc)
from pyspark.sql.window import Window


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*/*.json"

    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    cols = ["song_id", "title", "artist_id", "year", "duration"]
    songs_table = (df.filter(df.song_id.isNotNull())
                   .select(cols)
                   .distinct())

    # write songs table to parquet files partitioned by year and artist
    path = output_data + "songs_table.parquet"
    partition = ["year", "artist_id"]
    (songs_table.write
     .partitionBy(partition)
     .format("parquet")
     .save(path))

    # extract columns to create artists table
    cols = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
    artists_table = (df.filter(df.artist_id.isNotNull())
                     .select(cols)
                     .distinct()
                     .withColumnRenamed("artist_name", "name")
                     .withColumnRenamed("artist_location", "location")
                     .withColumnRenamed("artist_latitude", "latitude")
                     .withColumnRenamed("artist_longitude", "longitude"))


    # write artists table to parquet files
    path = output_data + "artists_table.parquet"
    (artists_table.write
     .format("parquet")
     .save(path))


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data =input_data + "log_data/*/*/*.json"

    # read log data file
    df = spark.read.json(log_data)

    # filter by actions for song plays
    df = df.filter(df.page == "NextSong")

    # create datetime column from original timestamp column
    df = df.withColumn("start_time", from_unixtime(df.ts / 1000.))

    # extract columns to create time table
    time_table = (df.select("start_time")
                  .withColumn("hour", hour(df.start_time))
                  .withColumn("dat", dayofmonth(df.start_time))
                  .withColumn("week", weekofyear(df.start_time))
                  .withColumn("month", month(df.start_time))
                  .withColumn("year", year(df.start_time))
                  .withColumn("weekday", date_format(df.start_time, "u")))

    # write time table to parquet files partitioned by year and month
    path = output_data + "time_table.parquet"
    partition = ["year", "month"]
    (time_table.write
     .partitionBy(partition)
     .format("parquet")
     .save(path))

    # extract columns to create users table
    cols = ["userId", "firstName", "lastName", "gender", "level"]
    window = Window.partitionBy("userId").orderBy(desc("start_time"))
    users_table = (df.filter(df.userId.isNotNull())
                   .withColumn("rn", row_number().over(window)))
    users_table = (users_table.filter(users_table.rn == 1)
                   .drop("rn")
                   .select(cols)
                   .withColumnRenamed("userId", "user_id")
                   .withColumnRenamed("firstName", "first_name")
                   .withColumnRenamed("lastName", "last_name"))

    # write users table to parquet files
    path = output_data + "users_table.parquet"
    (users_table.write
     .format("parquet")
     .save(path))

    # read in song data to use for songplays table
    path = output_data + "songs_table.parquet"
    song_df = spark.read.parquet(path)

    # extract columns from joined song and log datasets to create songplays table 
    cols = ["start_time", "userId", "level", "song_id", "artist_id", "sessionId", "location", "userAgent"]
    cond_song = [df.song == song_df.title, df.length == song_df.duration]
    window = Window.orderBy("start_time")
    songplays_table = (df.join(song_df, cond_song)
                       .select(cols)
                       .withColumn("songplay_id", row_number().over(window))
                       .withColumnRenamed("userId", "user_id")
                       .withColumnRenamed("sessionId", "session_id")
                       .withColumnRenamed("userAgent", "user_agent")
                       .withColumn("year", year(df.start_time))
                       .withColumn("month", month(df.start_time)))

    # write songplays table to parquet files partitioned by year and month
    path = output_data + "songplays_table.parquet"
    partition = ["year", "month"]
    (songplays_table.write
     .partitionBy(partition)
     .format("parquet")
     .save(path))


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3://ud-dataengineer/"

    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
