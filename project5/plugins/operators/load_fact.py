from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
    INSERT_TEMPLATE = """
        INSERT INTO {target_table}
        {sql}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 sql='',
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        query = LoadFactOperator.INSERT_TEMPLATE.format(
            target_table=self.table,
            sql=self.sql
        )
        self.log.info('Execute LoadFactOperator')
        redshift_hook.run(query)
