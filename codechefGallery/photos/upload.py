import boto3
from datetime import datetime

def getFileName(userId):
    dt = datetime.now()
    return userId+str(dt)+'.png'

def uploadPhoto(userId,filePath):
    bucketName='codechefgallery'
    fileName=getFileName(userId)
    try:
        s3 = boto3.client('s3')
        s3.upload_file(filePath,bucketName,fileName),"OK"
        bucket_location = s3.get_bucket_location(Bucket=bucketName)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'],bucketName,fileName)
        return object_url,"OK"
    except Exception as e:
        return None,str(e)
