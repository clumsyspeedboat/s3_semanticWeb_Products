import io
import base64
import qrcode
from datetime import datetime, timedelta
from minio import Minio
from minio.error import S3Error
import configparser
import os


#####################################################################
# Load MinIO credentials from .ini
def get_minio_client():
    config = configparser.ConfigParser()
    
    # Load the .ini file from the same directory as this script
    ini_file_path = os.path.join(os.path.dirname(__file__), '.ini')
    config.read(ini_file_path)

    # Fetch credentials from the .ini file
    access_key = config.get('minio_config', 'MINIO_ACCESS_KEY', fallback=None)
    secret_key = config.get('minio_config', 'MINIO_SECRET_KEY', fallback=None)

    # Raise an error if credentials are missing
    if not access_key or not secret_key:
        raise ValueError("MinIO credentials are missing from .ini file.")

    # Initialize and return MinIO client
    return Minio(
        endpoint='s3api.aimotions1.rz.fh-ingolstadt.de',
        access_key=access_key,
        secret_key=secret_key,
        secure=True
    )
#####################################################################

BUCKET_NAME = "aimotion-public-big-data-lecture-ws24"

#####################################################################

# List all objects in the dedicated bucket
def list_bucket_objects(minio_client):
    try:
        objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
        print("Existing data in bucket:")
        for obj in objects:
            print(obj.object_name)
        return [obj.object_name for obj in objects]
    except S3Error as e:
        raise Exception(f"Error listing bucket objects: {e}")
    
#####################################################################

# Upload data with an optional folder path
def upload_data(minio_client, data, object_name, folder_path=None):
    try:
        # If a folder path is provided, prepend it to the object name
        if folder_path:
            object_name = f"{folder_path.strip('/')}/{object_name}"

        # Convert data to BytesIO if it's not already
        if not isinstance(data, io.BytesIO):
            data = io.BytesIO(data.encode('utf-8'))

        # Upload data to the bucket
        minio_client.put_object(
            BUCKET_NAME,
            object_name,
            data,
            length=data.getbuffer().nbytes,
            content_type="application/octet-stream"
        )
        print(f"Data '{object_name}' uploaded successfully to bucket '{BUCKET_NAME}'.")
    except S3Error as e:
        raise Exception(f"Error uploading data: {e}")

#####################################################################

# Generate a presigned URL with inline Content-Disposition
def generate_presigned_url(minio_client, object_name, expiry_hours=1):
    try:
        # Generate presigned URL with custom response headers
        presigned_url = minio_client.presigned_get_object(
           ####################################
           ## Insert your code here##
           ####################################
           
        )
        print(f"Presigned URL: {presigned_url}")
        return presigned_url

    except S3Error as e:
        raise Exception(f"Error generating presigned URL: {str(e)}")

#####################################################################

# Generate a QR code for the file URL
def generate_qr_code(file_url):
    qr = qrcode.QRCode(version=1, box_size=3, border=5)
    qr.add_data(file_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()

    return qr_code

#####################################################################
