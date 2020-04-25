from datetime import (datetime,
                      timedelta)
from logging import info
import os

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator,
                               LoadFactOperator,
                               LoadDimensionOperator,
                               DataQualityOperator)

from helpers import SqlQueries

# CATCHUP https://knowledge.udacity.com/questions/104333
default_args = {
    'owner': 'udacity',
    'start_date': datetime(2020, 1, 1),
    # 'end_date': datetime(2020, 4, 30)
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          catchup=False,
          template_searchpath='/opt/airflow'
        )

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

create_tables = PostgresOperator(
    task_id='Create_tables',
    dag=dag,
    sql='create_tables.sql',
    postgres_conn_id='redshift_conn_id'
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    sql=SqlQueries.copy_from_s3.format(
        'staging_events',
        's3://' + Variable.get('s3_bucket') + '/' + Variable.get('logdata'),
        Variable.get('ARN'),
        Variable.get('region'),
        's3://' + Variable.get('s3_bucket') + '/' + Variable.get('logpath')
    ),
    redshift_conn_id='redshift_conn_id'
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    sql=SqlQueries.copy_from_s3.format(
        'staging_songs',
        's3://' + Variable.get('s3_bucket') + '/' + Variable.get('songdata'),
        Variable.get('ARN'),
        Variable.get('region'),
        'auto'),
    redshift_conn_id='redshift_conn_id'
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

start_operator                >> create_tables
create_tables                 >> [stage_events_to_redshift, stage_songs_to_redshift]
[stage_events_to_redshift,
 stage_songs_to_redshift]     >> load_songplays_table
load_songplays_table          >> [load_user_dimension_table,
                                  load_song_dimension_table,
                                  load_artist_dimension_table,
                                  load_time_dimension_table]
[load_user_dimension_table,
 load_song_dimension_table,
 load_artist_dimension_table,
 load_time_dimension_table]   >> run_quality_checks
run_quality_checks            >> end_operator
