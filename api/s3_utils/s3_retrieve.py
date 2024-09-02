import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os


def get_image_url(object_name):
    load_dotenv()  # This loads the variables from .env

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

    """Generate a presigned URL for the S3 object"""
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': aws_bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=3600)
    except ClientError as e:
        print(e)
        return None
    return response

def list_images():
    load_dotenv()  # This loads the variables from .env

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = os.getenv('AWS_BUCKET_NAME')
    
    """List all images in the S3 bucket"""
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.list_objects_v2(Bucket=aws_bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except ClientError as e:
        print(e)
        return []