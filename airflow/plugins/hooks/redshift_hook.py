"""Custom Redshift Hook."""

from contextlib import closing

import sqlparse
from airflow.providers.amazon.aws.hooks.redshift import RedshiftSQLHook


class RedshiftHook(RedshiftSQLHook):
    """Custom Redshift Hook including sqlparse."""

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def run(self, sql, autocommit=False, parameters=None, handler=None):
        """
        Run a command or a list of commands sequentially.

        :param sql: the sql statement to be executed (str) or a list of
            sql statements to execute
        :type sql: str or list
        :param autocommit: What to set the connection's autocommit setting to
            before executing the query.
        :type autocommit: bool
        :param parameters: The parameters to render the SQL query with.
        :type parameters: dict or iterable
        :param handler: The result handler which is called with the result of each statement.
        :type handler: callable
        :return: query results if handler was provided.
        """
        sql = sqlparse.split(sqlparse.format(sql, strip_comments=True))

        scalar = isinstance(sql, str)
        if scalar:
            sql = [sql]

        with closing(self.get_conn()) as conn:
            if self.supports_autocommit:
                self.set_autocommit(conn, autocommit)

            with closing(conn.cursor()) as cur:
                results = []
                for sql_statement in sql:
                    self._run_command(cur, sql_statement, parameters)
                    if handler is not None:
                        result = handler(cur)
                        results.append(result)

            if not self.get_autocommit(conn):
                conn.commit()

        if handler is None:
            return None

        if scalar:
            return results[0]

        return results
