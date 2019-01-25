#imports
#Youll need azure-storage and azure-sdk
from azure.storage.blob import BlockBlobService
import boto3
import botocore

#Azure Access
block_blob_service = BlockBlobService(account_name='YOUR_AZURE_ACCOUNT_NAME', account_key='YOUR_AZURE_ACCOUNT_KEY')
#this creates a list of the blobs in the container to copy
generator = block_blob_service.list_blobs('THE_CONTAINER_YOU_WANT_TO_ACCESS')

#S3 access
client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('YOUR_BUCKET_NAME')
exists = True
try:
    s3.meta.client.head_bucket(Bucket='YOUR_BUCKET_NAME')
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = e.response['Error']['Code']
    if error_code == '404':
        exists = False

#The grunt work - copying each blob from Azure and putting it in S3 bucket
for blob in generator:
    #get the blob
    b = block_blob_service.get_blob_to_bytes('htmlarchive', blob.name)
    #check that it doesn't already exist in the bucket
    content = client.head_object(Bucket='fievel',Key=blob.name)
    if content.get('ResponseMetadata',None) is not None:
        next
    else:
        #if file is not already in bucket, put it in bucket
        bucket.put_object(Key=blob.name, Body=b.content)
    