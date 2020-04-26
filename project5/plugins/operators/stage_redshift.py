from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    COPY_TEMPLATE = """
        copy {}
        from '{}'
        access_key_id '{}'
        secret_access_key '{}'
        region '{}'
        json '{}'
        compupdate off
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 aws_conn_id='',
                 table='',
                 data='',
                 region='',
                 json_option='',
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.table = table
        self.data = data
        self.region = region
        self.json_option = json_option

    def execute(self, context):
        aws_hook = AwsHook(self.aws_conn_id)
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(self.redshift_conn_id)

        self.log.info('Execute StageToRedshiftOperator')
        sql = StageToRedshiftOperator.COPY_TEMPLATE.format(
            self.table,
            self.data,
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.json_option
        )
        redshift_hook.run(sql)
