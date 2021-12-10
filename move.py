#!/usr/bin/env python

import boto3
import logging
import argparse
import psycopg2
import os
import sys
import threading
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Env variables for database and S3 configuration
# -----------------------------------
# S3 buckets need to allow the IAM user access 
# to read the source bucket and write to the destination bucket
# -----------------------------------
DB_CONN_STRING = os.getenv(
    'DB_CONN_STRING', 'postgres://username:password@127.0.0.1/proddatabase')
S3_SOURCE_BUCKET_NAME = os.getenv('S3_SOURCE_BUCKET_NAME', 'legacy-s3')
S3_DEST_BUCKET_NAME = os.getenv('S3_DEST_BUCKET_NAME', 'production-s3')
S3_OBJECT_DEST_PREFIX = os.getenv('S3_OBJECT_DEST_PREFIX', 'avatar')

# Initializing S3 client
s3 = boto3.client("s3")

# -----------------------------------
# NB: The database user needs to have read and write permissions in the database.
# -----------------------------------

# Create database connection
try:
    conn = psycopg2.connect(DB_CONN_STRING)
except Exception as e:
    logging.error(f"Error while connecting to the database: {e}")
    sys.exit(1)

# -----------------------------------
# This function checks for the existence of a path in the database
# it returns a boolean to confirm the existence of the path.
# -----------------------------------
def check_exists(name):
    try:
        name_exists = False
        cur = conn.cursor()
        cur.execute("SELECT * FROM avatars WHERE path = (%s)", (name,))
        if len(cur.fetchall()) > 0:
            name_exists = True
        conn.commit()
        return name_exists
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

# -----------------------------------
# This updates the legacy path to the new path which is the
# production path.
# -----------------------------------
def update_db_row(new_path, old_path):
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE avatars SET path = (%s) WHERE path = (%s)", (new_path, old_path))
        conn.commit()
    except Exception as e:
        print(f"Error inserting to the database: {e}")
        sys.exit(1)

# -----------------------------------
# This function copies files between S3 buckets (legacy and production).
# -----------------------------------
def copy_file(key):
    file_name = key.split("/")[-1]
    dest_key = f"{S3_OBJECT_DEST_PREFIX}/{file_name}"
    copy_source = {
        'Bucket': S3_SOURCE_BUCKET_NAME,
        'Key': key
    }
    try:
        # Check if file exists so we dont 
        if not check_exists(dest_key):
            response = s3.copy_object(
                Bucket=S3_DEST_BUCKET_NAME,
                Key=dest_key,
                CopySource=copy_source
            )
            print(f"Successfully copied file {dest_key}")
            update_db_row(dest_key, key)
        else:
            print(f"The asset {dest_key} already exists")
    except Exception as e:
        logging.error(f"Error while copying file: {e}")
        sys.exit(1)

# -----------------------------------
# This function gets all the files that exists in the legacy bucket
# -----------------------------------
def get_files():
    files = []
    try:
        files = [file["Key"] for file in s3.list_objects(
            Bucket=S3_SOURCE_BUCKET_NAME
        )['Contents'] if file["Key"] != "image/"]
    except Exception as e:
        logging.error(f"Error while getting files: {e}")
        sys.exit(1)
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This script moves files accross s3 buckets')
    args = parser.parse_args()
    files = get_files()
    for file in files:
        x = threading.Thread(target=copy_file, args=(file,))
        x.start()
