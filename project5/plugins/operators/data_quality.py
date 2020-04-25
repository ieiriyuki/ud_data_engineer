from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'
    SELECT_TEMPLATE = """
        SELECT
            count(1),
            count(distinct {target_col})
        FROM {target_table}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 column='',
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.column = column

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        query = DataQualityOperator.SELECT_TEMPLATE.format(
            target_col=self.column,
            target_table=self.table
        )
        self.log.info('Execute DataQualityOperator')
        records = redshift_hook.get_records(query)
        if len(records) > 0:
            if len(records[0]) > 0:
                self.log.info(f'Count is {}, Distinct Count of {} is {}'.format(
                    records[0], self.column, records[1]
                ))
            else:
                raise ValueError('Record has no counts')
        else:
            raise ValueError('No records found. Something wrong')
