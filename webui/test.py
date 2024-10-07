from datetime import timedelta
from minio import Minio
import requests
import io
import json
from minio.error import S3Error
from requests.auth import HTTPBasicAuth

# Initialize MinIO client
client = Minio(
    "s3api.aimotions1.rz.fh-ingolstadt.de",  # Replace with your endpoint
    access_key="NnAXUNysIAppobHYKVQs",  # Replace with your access key
    secret_key="Cl2gChOixKAg2thBTLidTgOlnXmxwg269eQPVvyO",  # Replace with your secret key
    secure=True  # Use True if SSL is enabled
)

# Define the bucket name
bucket_name = "aimotion-s3drop-mondal-cato-8c3ec3"

# Define a bucket policy that grants public (anonymous) read and write (upload) access
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",  # '*' means anyone can access (anonymous access)
            "Action": [
                "s3:GetBucketLocation",   # Allow access to get bucket location
                "s3:ListBucket",          # Allow listing objects in the bucket (required for browsing)
                "s3:GetObject",           # Allow downloading (reading) objects
                "s3:PutObject"            # Allow uploading (writing) objects
            ],
            "Resource": [
                f"arn:aws:s3:::{bucket_name}",         # Permissions for the bucket (ListBucket, GetBucketLocation)
                f"arn:aws:s3:::{bucket_name}/*"        # Permissions for all objects within the bucket
            ]
        }
    ]
}

# Convert the policy to a JSON string
policy_json = json.dumps(policy)

# Apply the policy to the bucket
try:
    client.set_bucket_policy(bucket_name, policy_json)
    print(f"Public read and write access has been granted to all objects in the bucket '{bucket_name}'.")

    # Define the object name (optional: to demonstrate generating URL)
    object_name = "bucket-metadata/readme.txt"  # Replace with your actual object name

    # Print the HTTPS access URL
    access_url = f"https://s3api.aimotions1.rz.fh-ingolstadt.de/{bucket_name}/{object_name}"
    print(f"Access URL: {access_url}")

except S3Error as e:
    print(f"Error applying policy: {e}")