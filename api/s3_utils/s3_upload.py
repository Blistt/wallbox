import boto3
import os
import json
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()  # Load environment variables once at the beginning

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

print(f"Using bucket: {aws_bucket_name}")

s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)

file_mapping = {}


def upload_file(file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        print(f"Uploading file: {file_name} to {object_name}")
        s3_client.upload_file(file_name, aws_bucket_name, object_name)
        file_mapping[os.path.splitext(os.path.basename(file_name))[0]] = object_name    # Ensures the key has no file extension
        print(f"Successfully uploaded {file_name}")
        return True
    except ClientError as e:
        print(f"Error uploading {file_name}: {e}")
        return False


def upload_directory(directory):
    print(f"Starting upload of directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, directory)
            s3_path = relative_path.replace("\\", "/")
            upload_file(local_path, s3_path)
    
    # Save the mapping to a JSON file
    mapping_file = 'image_mapping.json'
    with open(mapping_file, 'w') as f:
        json.dump(file_mapping, f, indent=2)
    print(f"File mapping saved to {mapping_file}")

# Usage
if __name__ == "__main__":
    upload_directory("public/dataset/images")
    print(f"Total files uploaded: {len(file_mapping)}")