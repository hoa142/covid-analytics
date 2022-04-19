"""Airflow DAG for Covid Analytics."""

import os
from datetime import datetime, timedelta

from airflow.models import Variable
from airflow.operators.python import PythonOperator
import sql_queries
from libs.aws_helpers import df_to_s3
from libs.corona_api import (
    get_covid_api_response,
    get_covid_df,
    get_covid_numbers,
    get_response_date,
)
from operators.redshift_operator import RedshiftOperator

from airflow import DAG

REDSHIFT_CONN = "redshift_dwh"
REDSHIFT_SQL_PATH = os.path.dirname(sql_queries.__file__)

covid_bucket = Variable.get("covid_bucket")
redshift_iam_role = Variable.get("redshift_iam_role")

default_args = {
    "owner": "hoa.tran",
    "email": ["hoatran142@outlook.com"],
    "start_date": datetime(2022, 4, 17),
    "catchup": False,
    "depends_on_past": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=10),
}

api_response = get_covid_api_response()
response_date = get_response_date(api_response)
covid_numbers = get_covid_numbers(api_response)
covid_df = get_covid_df(covid_numbers)
file_name = f"{response_date}.csv"


with DAG(
    dag_id="covid_analytics",
    description="Load Covid cases numbers of countries to S3 and Redshift",
    concurrency=1,
    schedule_interval="00 11,15 * * *",
    default_args=default_args,
    tags=["covid", "analytics"],
    max_active_runs=1,
    template_searchpath=REDSHIFT_SQL_PATH,
) as dag:
    load_covid_to_s3 = PythonOperator(
        task_id="load_covid_to_s3",
        python_callable=df_to_s3,
        op_kwargs={
            "df": covid_df,
            "bucket": covid_bucket,
            "file_name": file_name,
        },
    )

    load_covid_to_redshift = RedshiftOperator(
        task_id="load_covid_to_redshift",
        sql="load_covid_cases.sql",
        redshift_conn_id=REDSHIFT_CONN,
        params={
            "file_name": file_name,
            "redshift_iam_role": redshift_iam_role,
        },
    )

    load_covid_to_s3 >> load_covid_to_redshift
