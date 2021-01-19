#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import boto3

logger = logging.getLogger(__name__)


class AwsUtils:
    s3 = boto3.client("s3")

    @staticmethod
    def put_content_in_s3(bucket_name, s3_file_path, data_str):
        """
        Saves the string as bytes in a new s3 object given by s3_file_path
        Args:
            bucket_name: s3 bucket name
            s3_file_path: s3 file path (without bucketname) for new file
            data_str: data in string format
        """
        AwsUtils.s3.put_object(Bucket=bucket_name, Key=s3_file_path, Body=data_str)
