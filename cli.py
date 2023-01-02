import os
import time

import boto3
import sh
import typer
from botocore.exceptions import ClientError
from rich import print as rprint
from datetime import datetime

# create a typer app
app = typer.Typer()


@app.command()
def fly_db_connect(app_name="app-name", bg: int = 0):
    """
    Connect to the database
    :param app_name: The name of the app
    :param bg: Run in the background (0-false, 1-true)
    """
    rprint(f"[green]Connecting to {app_name}, {bg}")
    _bg = bg == 1
    rprint(
        f"[green]Connecting to the database: Running in the background: {_bg}")
    try:
        proxy_app_name = os.getenv("PROXY_APP_NAME")
        return sh.flyctl("proxy", "5432", a=proxy_app_name, _out=rprint, _bg=_bg)
    except sh.ErrorReturnCode as e:
        rprint(e)


@app.command()
def fly_db_backup(
    port=5432,
    host="127.0.0.1",
):
    """Connect to fly.io and backup the database"""
    password = os.getenv("PG_PASSWORD")
    user = os.getenv("PG_USER")
    db_name = os.getenv("PG_DATABASE")
    app_name = os.getenv('APP_NAME')

    db_connection = None

    try:
        rprint("[green] Backing up the database")
        # start timer
        start = time.time()
        db_connection = fly_db_connect(app_name=app_name, bg=1)
        # wait for the connection here

        time.sleep(15)

        filename = f"dbbackup-connector-{datetime.now().timestamp()}.sql"
        rprint(f"[green]Backing up the database to {filename}, please wait...")
        process = sh.pg_dump(
            "-h",
            host,
            "-p",
            port,
            "-U",
            user,
            "-f",
            filename,
            db_name,
            _out=rprint,
            _in=password,
            _bg=False,
        )
        rprint(process)

        rprint("[green] backup complete, uploading to s3")
        upload_file(filename)

        # end timer
        end = time.time()
        rprint(f"[green] Total runtime of the program is [red] {end - start}")
        db_connection.terminate()

    except sh.ErrorReturnCode as e:
        rprint(e)
        if db_connection:
            db_connection.terminate()


@app.command()
def upload_file(file_name):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """

    bucket = os.getenv('S3_BUCKET')
    region = os.getenv('AWS_REGION')

    # Upload the file
    rprint(f"[green] Uploading {file_name} to {bucket}")
    s3_client = boto3.client(
        "s3",
        region,
        # endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),

    )
    try:
        s3_client.upload_file(file_name, bucket, f"production/{file_name}")
    except ClientError as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    app()
