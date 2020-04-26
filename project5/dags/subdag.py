from airflow.models import DAG
from operators import DataQualityOperator

def sub_dag(
    parent_dag_name,
    child_dag_name,
    start_date,
    schedule_interval,
    *args, **kwargs):
    dag = DAG('%s.%s' % (parent_dag_name, child_dag_name),
              start_date=start_date,
              schedule_interval=schedule_interval,
              )

    run_check_songplays = DataQualityOperator(
        task_id='Run_data_check_songplays',
        dag=dag,
        table='songplays',
        column='playid',
        is_null=['playid', 'start_time', 'userid'],
        redshift_conn_id='redshift_conn_id'
    )

    run_check_user = DataQualityOperator(
        task_id='Run_data_check_user',
        dag=dag,
        table='users',
        column='userid',
        is_null=['userid'],
        redshift_conn_id='redshift_conn_id'
    )

    run_check_song = DataQualityOperator(
        task_id='Run_data_check_song',
        dag=dag,
        table='songs',
        column='songid',
        is_null=['songid'],
        redshift_conn_id='redshift_conn_id'
    )

    run_check_artist = DataQualityOperator(
        task_id='Run_data_check_artist',
        dag=dag,
        table='artists',
        column='artistid',
        is_null=['artistid'],
        redshift_conn_id='redshift_conn_id'
    )

    run_check_time = DataQualityOperator(
        task_id='Run_data_check_time',
        dag=dag,
        table='"time"',
        column='start_time',
        is_null=['start_time'],
        redshift_conn_id='redshift_conn_id'
    )

    return dag
