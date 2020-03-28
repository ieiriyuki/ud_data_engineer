import configparser
import pandas as pd
import psycopg2

from sql_queries import (copy_table_queries,
                         insert_table_queries,
                         check_table_queries)


def load_staging_tables(cur, conn):
    """load original data to staging tables
    """
    for query in copy_table_queries:
        print("copying data", query, sep="\n")
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """insert the data of staging tables into rearranged tables
    """
    for query in insert_table_queries:
        print("inserting data", query, sep="\n")
        cur.execute(query)
        conn.commit()


def check_tables(cur, conn, n=3):
    """check data in the tables
    """
    for query in check_table_queries:
        try:
            cur.execute(query)
            data = cur.fetchall()
            if data is None:
                print("None")
            else:
                print(query, pd.DataFrame(data).head(n), sep="\n")
            conn.commit()
        except Exception as e:
            conn.commit()
            raise e


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            *config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)
    select_tables(cur, conn)
    check_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
