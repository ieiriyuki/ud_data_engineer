from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    INSERT_TEMPLATE = """
        INSERT INTO {target_table}
        {sql}
    """
    DELETE_TEMPLATE = """
        DELETE FROM {target_table}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 sql='',
                 append_data=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.append_data = append_data

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        query = LoadDimensionOperator.INSERT_TEMPLATE.format(
            target_table=self.table,
            sql=self.sql
        )
        self.log.info(f'Execute LoadDimensionOperator. append: {self.append_data}')
        if not self.append_data:
            del_query = LoadDimensionOperator.DELETE_TEMPLATE.format(target_table=self.table)
            redshift_hook.run(del_query)
        
        redshift_hook.run(query)
