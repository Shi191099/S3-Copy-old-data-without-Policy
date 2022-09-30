import boto3
import os 
from datetime import datetime, timedelta 
session = boto3.Session( 
#Add Destination credentials 
aws_access_key_id='************', 
aws_secret_access_key='***************' 
) 
s3 = session.resource('s3') 
SOURCE_BUCKET = 'source-bucket-name' 
DESTINATION_BUCKET = 'destination-bucket-name' 
s3_client = boto3.client('s3') 
  
# Create a reusable Paginator 
paginator = s3_client.get_paginator('list_objects_v2') 
  
# Create a PageIterator from the Paginator 
page_iterator = paginator.paginate(Bucket=SOURCE_BUCKET) 
  
# Loop through each object, looking for ones older than a given time period, and download them to the local machine 
for page in page_iterator: 
    for object in page['Contents']: 
        if object['LastModified'] < datetime.now().astimezone() - timedelta(days=90):   # <-- Change time period here 
            print(f"Moving {object['Key']}") 
            #download object to local machine 
            s3_client.download_file(SOURCE_BUCKET, object['Key'], object['Key']) 
            #upload to s3 from local machine 
            object = s3.Object(DESTINATION_BUCKET, object['Key']) 
            result = object.put(Body='') 
            res = result.get('ResponseMetadata') 
            print(object.key) 
            #remove object from local 
            os.remove(object.key) 
            if res.get('HTTPStatusCode') == 200: 
                print('File Uploaded Successfully') 
            else: 
                print('File Not Uploaded') 
