#!/usr/bin/env python

import boto3
import logging
import argparse
import psycopg2
import os
import sys

# Env variables for database and S3 configuration
DB_CONN_STRING = os.getenv(
    'DB_CONN_STRING', 'postgres://postgres:gopher@127.0.0.1/proddatabase')
S3_SOURCE_BUCKET_NAME = os.getenv('S3_SOURCE_BUCKET_NAME', 'legacy-s3-ut')
S3_DEST_BUCKET_NAME = os.getenv('S3_DEST_BUCKET_NAME', 'production-s3-ut')
S3_OBJECT_DEST_PREFIX = os.getenv('S3_OBJECT_DEST_PREFIX', 'avatar')

# Initializing S3 client
s3 = boto3.client("s3")

# Create database connection
try:
    conn = psycopg2.connect(DB_CONN_STRING)
except Exception as e:
    logging.error(f"Error while connecting to the database: {e}")
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This script moves files accross s3 buckets')
    args = parser.parse_args()

