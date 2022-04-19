"""AWS helper libraries for S3 and Redshift."""

import logging
from io import StringIO

import boto3
from pandas import DataFrame

log = logging.getLogger(__name__)
s3_client = boto3.client("s3")


def df_to_s3(df: DataFrame, bucket: str, file_name: str) -> str:
    """
    Upload Pandas dataframe to S3 bucket.

    :param df: Pandas dataframe
    :param bucket: bucket name
    :param file_name: file name
    :return: S3 file path
    """
    csv_buf = StringIO()
    df.to_csv(csv_buf, header=True, index=False)
    csv_buf.seek(0)
    s3_client.put_object(Bucket=bucket, Body=csv_buf.getvalue(), Key=file_name)

    s3_file_path = f"s3://{bucket}/{file_name}"
    log.info(f"Covid cases numbers was uploaded to {s3_file_path}")

    return s3_file_path
