"""Custom Redshift Operator."""

from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator
from hooks.redshift_hook import RedshiftHook


class RedshiftOperator(RedshiftSQLOperator):
    """Custom Redshift Operator including sqlparse."""

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def get_hook(self) -> RedshiftHook:
        """Get custom Redshift Hook."""
        return RedshiftHook(redshift_conn_id=self.redshift_conn_id)
