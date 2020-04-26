from datetime import (datetime,
                      timedelta)

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.subdag_operator import SubDagOperator

from operators import (StageToRedshiftOperator,
                       LoadFactOperator,
                       LoadDimensionOperator)
from helpers import SqlQueries
from subdag import sub_dag


default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 12),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'catchup': False
}

DAG_NAME = 'udac_example_dag'

dag = DAG(DAG_NAME,
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          template_searchpath='/home/workspace/airflow'
        )

start_operator = PostgresOperator(
    task_id='Begin_execution_Create_tables',
    dag=dag,
    sql='create_tables.sql',
    postgres_conn_id='redshift_conn_id'
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table='staging_events',
    data='s3://' + Variable.get('s3_bucket') + '/' + Variable.get('logdata'),
    region=Variable.get('region'),
    json_option='s3://' + Variable.get('s3_bucket') + '/' + Variable.get('logpath'),
    redshift_conn_id='redshift_conn_id'
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table='staging_songs',
    data='s3://' + Variable.get('s3_bucket') + '/' + Variable.get('songdata'),
    region=Variable.get('region'),
    json_option='auto',
    redshift_conn_id='redshift_conn_id'
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    table='songplays',
    sql=SqlQueries.songplays_table_insert,
    redshift_conn_id='redshift_conn_id'
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    table='users',
    sql=SqlQueries.users_table_insert,
    redshift_conn_id='redshift_conn_id'
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    table='songs',
    sql=SqlQueries.songs_table_insert,
    redshift_conn_id='redshift_conn_id'
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    table='artists',
    sql=SqlQueries.artists_table_insert,
    redshift_conn_id='redshift_conn_id'
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    table='"time"',
    sql=SqlQueries.time_table_insert,
    redshift_conn_id='redshift_conn_id'
)

run_quality_checks = SubDagOperator(
    task_id='Run_data_quality_checks',
    subdag=sub_dag(DAG_NAME,
                   'Run_data_quality_checks',
                   datetime(2019, 1, 12),
                   '0 * * * *'),
    dag=dag,
)

end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

start_operator                >> [stage_events_to_redshift, stage_songs_to_redshift]
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
