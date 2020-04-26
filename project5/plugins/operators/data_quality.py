from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'
    COUNT_TEMPLATE = """
        SELECT
            count(1),
            count(distinct {target_col})
        FROM {target_table}
    """
    NULL_CHECK = """
        SELECT count({is_null_col})
        FROM {target_table}
        WHERE {is_null_col} IS NULL
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 column='',
                 is_null=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.column = column
        self.is_null = is_null

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)

        # Check counts of rows
        query = DataQualityOperator.COUNT_TEMPLATE.format(
            target_col=self.column,
            target_table=self.table
        )
        self.log.info(f'Count {self.column} in {self.table}')
        records = redshift_hook.get_records(query)
        if len(records) > 0:
            if len(records[0]) > 0:
                for r in records:
                    self.log.info('Counts: {}, Distinct Counts of {}: {}'.format(
                        records[0][0], self.column, records[0][1]))
            else:
                raise ValueError('Record has no counts')
        else:
            raise ValueError('No records found. Something wrong')

        # Check null rows
        for col in self.is_null:
            self.log.info(f'Check null counts of {col} in {self.table}')
            query = DataQualityOperator.NULL_CHECK.format(
                is_null_col = col,
                target_table = self.table
            )
            records = redshift_hook.get_records(query)
            if records[0][0] == 0:
                self.log.info(f'{col} does not have null')
            else:
                raise ValueError(f'{col} contains null')
