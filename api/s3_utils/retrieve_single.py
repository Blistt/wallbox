import os
import sys
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

# Initialize S3 client
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)

def get_image(image_name, save_path, expiration=3600):
    # Load the image mapping
    with open('image_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    # Get the S3 key for the image
    s3_key = mapping.get(image_name)
    if s3_key:
        try:
            # Download the image from S3
            s3_client.download_file(aws_bucket_name, s3_key, save_path)
            print(f"Image saved to {save_path}")
        except ClientError as e:
            print(f"Error: {e}", file=sys.stderr)
    else:
        print(f"Error: Image '{image_name}' not found", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <image_filename> <save_path>", file=sys.stderr)
        sys.exit(1)
    
    image_name = sys.argv[1]
    save_path = sys.argv[2]
    get_image(image_name, save_path)