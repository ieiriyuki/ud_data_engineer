from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    COPY_TEMPLATE = """
        copy {}
        from '{}'
        iam_role '{}'
        region '{}'
        json '{}'
        compupdate off
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 data='',
                 arn='',
                 region='',
                 json_option='',
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.data = data
        self.arn = arn
        self.region = region
        self.json_option = json_option

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)

        self.log.info('Execute StageToRedshiftOperator')
        sql = StageToRedshiftOperator.COPY_TEMPLATE.format(
            self.table,
            self.data,
            self.arn,
            self.region,
            self.json_option
        )
        redshift_hook.run(sql)
