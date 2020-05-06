#!/usr/bin/env python

from configparser import ConfigParser
from logging import (basicConfig,
                     getLogger,
                     INFO)

import psycopg2

from queries import (create_table_queries,
                     copy_template,
                     insert_template,
                     select_queries,
                     validate_queries)

basicConfig(level=INFO)
logger = getLogger(__name__)


def main():
    config = ConfigParser()
    config.read("../params.cfg")
    (access_key, secret_key) = config["aws"].values()
    bucket = config["s3"]["bucket"]
    prefix = "s3://" + bucket + "/"

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config['redshift'].values()))
    cur = conn.cursor()

    create_tables(cur, conn)

    # load data in S3 into Redshift
    staging_params = [
        ["stage_retail", config["files"]["retail"], "csv ignoreheader 1"],
        ["stage_rate", config["files"]["rate"], "csv ignoreheader 1 dateformat 'MON DD, YYYY'"],
        ["stage_weather", config["files"]["weather"], "json '{}{}'".format(prefix, config["files"]["jsonpath"])]
    ]
    for params in staging_params:
        stage_data(cur, conn, copy_template, params[0], prefix + params[1],
                   access_key, secret_key, params[2])

    # insert staging data into proper tables
    tables = ["retail", "rate", "weather"]
    for table, sql in zip(tables, select_queries):
        insert_data(cur, conn, table, sql)

    # Check the number of rows
    for sql in validate_queries:
        validate_data(cur, conn, sql)

    conn.close()
    return 1


def create_tables(cur, conn):
    """Create tables for staging and production

    Parameters
    ----------
    cur : cursor instance
        the cursor of psycopg2
    conn : connection instance
        the connection of psycopg2
    """

    global logger
    logger.info(f"Creating tables")
    cur.execute(create_table_queries)
    conn.commit()
    return 1


def stage_data(cur, conn, sql, table, path, access_key, secret_key, option=""):
    """Load data into a staging table

    Parameters
    ----------
    cur : cursor instance
        the cursor of psycopg2
    conn : connection instance
        the connection of psycopg2
    sql : str
        a sql query
    table : str
        a target table
    path : str
        an object path in S3
    access_key : str
        AWS access key
    secret_key : str
        AWS secret access key
    option : str
        query options
    """

    global logger
    query = sql.format(table, path, access_key, secret_key, option)
    logger.info(f"Stage {path} into {table}")
    cur.execute(query)
    conn.commit()
    return 1


def insert_data(cur, conn, table, sql):
    """Insert data from staging tables into production tables

    Parameters
    ----------
    cur : cursor instance
        the cursor of psycopg2
    conn : connection instance
        the connection of psycopg2
    table : str
        a table inserted into
    sql : str
        a sql query
    """

    global logger

    query = insert_template.format(table, sql)
    logger.info(f"Insert into {table}")
    cur.execute(query)
    conn.commit()
    return 1


def validate_data(cur, conn, sql):
    """Validate tables and check values

    Parameters
    ----------
    cur : cursor instance
        the cursor of psycopg2
    conn : connection instance
        the connection of psycopg2
    sql : str
        a sql query
    """

    global logger
    cur.execute(sql)
    row = cur.fetchone()
    names = [x.name for x in cur.description]
    for name, value in zip(names, row):
        logger.info(f"Check data: {name} = {value}")
    conn.commit()
    return 1


if __name__ == "__main__":
    main()
