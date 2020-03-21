import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, test_tables


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


def select_tables(cur, conn):
    """select data from the created tables to check
    """
    for query in test_tables:
        print("select data", query, sep="\n")
        for row in cur.execute(query):
            print(row)
        conn.commit()


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

    conn.close()


if __name__ == "__main__":
    main()
