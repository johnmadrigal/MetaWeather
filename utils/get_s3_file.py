import boto3
import codecs

#get file from s3 with boto3
def get_s3_file(bucket_name, object_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    stream = bucket.Object(object_name).get()["Body"]
    return codecs.getreader("utf-8")(stream)