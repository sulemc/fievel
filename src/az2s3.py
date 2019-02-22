from azure.storage.blob import BlockBlobService
import boto3
import botocore
from pyspark import SparkContext

class AZ2S3:
    def __init__(self, a_key, a_name, a_container, s_bucket):
        #azure information
        self.a_key = a_key #YOUR_AZURE_ACCOUNT_KEY
        self.a_name = a_name #YOUR_AZURE_ACCOUNT_NAME
        self.a_container = a_container
        #s3 information
        self.s_bucket = s_bucket #string of bucket name
        self.s3 = boto3.resource('s3')
        self.bbs = BlockBlobService(account_name= self.a_name, account_key= self.a_key)
        self.sc = SparkContext(appName='fievel')
        self.sc.setLogLevel("FATAL")

    
    def check_for_bucket(self):
        exists = True
        try:
            self.s3.meta.client.head_bucket(Bucket=self.s_bucket)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
        return exists

    def az_to_s3(self):
        if self.check_for_bucket:
            print('bucket exists, creating list of azure blobs')
            generator = self.bbs.list_blobs(self.a_container)
            print('list of blobs created beginning itteration')
            self.sc.parallelize(generator).foreach(lambda blob: self.helper(blob))
            self.sc.stop()

    def helper(self, blob):
        print('hit inside helper')
        b = self.bbs.get_blob_to_bytes(self.a_container, blob.name)
        print(b)
        print(self.s3.Bucket(self.s_bucket))
        self.s3.Bucket(self.s_bucket).put_object(Key=blob.name, Body=b.content)
    