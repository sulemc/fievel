#imports?
#do i need to add s3 keys to init? automate boto3 setup?

class az2s3:
    def __init__(a_key, a_name, a_container, s_bucket):
        #azure information
        self.a_key = a_key
        self.a_name = a_name
        self.a_container = a_container
        #s3 information
        self.s_bucket = s_bucket #string of bucket name
        self.s3 = boto3.resource('s3')

    def create_azure_list(self):
        block_blob_service = BlockBlobService(account_name= self.a_name, account_key= self.a_key)
        #this creates a list of the blobs in the container to copy
        generator = block_blob_service.list_blobs(self.a_container)
        return generator
    
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
            generator = self.create_azure_list
            print('list of blobs created beginning itteration')
            for blob in generator:
                #get the blob
                b = block_blob_service.get_blob_to_bytes(self.a_container, blob.name)
                self.s3.Bucket(self.s_bucket).put_object(Key=blob.name, Body=b.content)
