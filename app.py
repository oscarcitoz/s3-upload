from http.client import HTTPException

import boto3
import base64
import os
from pydantic import BaseModel
import json


session = boto3.Session(aws_access_key_id=os.environ.get("ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("SECRET_KEY"))
s3_client = session.client("s3")
s3 = boto3.resource('s3')
S3_BUCKET = 'fluxi-bucket'
S3_PREFIX = 'prod/assets/'

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "pdf", "txt", "json", "html"}


class FileUpload(BaseModel):
    file: str
    folder: str = ""
    filename: str


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS


def get_content_type(filename):
    extension = filename.rsplit('.', 1)[-1].lower()
    if extension == 'jpg' or extension == 'jpeg':
        return "image/jpeg"
    elif extension == 'png':
        return "image/png"
    elif extension == 'gif':
        return "image/gif"
    elif extension == 'bmp':
        return "image/bmp"
    elif extension == 'pdf':
        return "application/pdf"
    elif extension == 'txt':
        return "text/plain"
    elif extension == 'html':
        return "text/html"
    elif extension == 'json':
        return "application/json"
    else:
        return "application/octet-stream"  # Default


def upload_to_s3(file_content, folder, filename):
    try:
        s3_path = f"{folder}/{filename}" if folder else filename
        s3_path_full = S3_PREFIX + s3_path
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_path_full,
            Body=file_content,
            ContentType=get_content_type(filename)
        )

        s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_path_full}"

        return {"message": "File uploaded successfully", "s3_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        file_upload = FileUpload(**body)
        file_content = base64.b64decode(file_upload.file)
        if not allowed_file(file_upload.filename):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "File extension not allowed"})
            }

        result = upload_to_s3(file_content, file_upload.folder, file_upload.filename)

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Error: {str(e)}"})
        }