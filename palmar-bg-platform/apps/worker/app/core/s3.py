"""
S3/MinIO client for file storage
"""
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
from app.core.config import settings
import io


class S3Client:
    """S3/MinIO client wrapper"""

    def __init__(self):
        self.client = None
        self.bucket_name = settings.S3_BUCKET_NAME

    def connect(self):
        """Initialize S3 client"""
        # Create S3 client
        self.client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version='s3v4'),
            use_ssl=settings.S3_USE_SSL,
        )

        # Create bucket if it doesn't exist
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            print(f"✓ Using S3 bucket: {self.bucket_name}")
        except ClientError:
            # Bucket doesn't exist, create it
            try:
                if settings.S3_REGION == 'us-east-1':
                    self.client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': settings.S3_REGION}
                    )
                print(f"✓ Created S3 bucket: {self.bucket_name}")
            except Exception as e:
                print(f"Warning: Could not create bucket: {e}")

    def upload_file(self, file_data: bytes, key: str, content_type: str = "image/png") -> bool:
        """
        Upload file to S3

        Args:
            file_data: File bytes to upload
            key: S3 object key (path)
            content_type: MIME type of the file

        Returns:
            bool: True if successful
        """
        try:
            file_obj = io.BytesIO(file_data)
            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs={'ContentType': content_type}
            )
            print(f"✓ Uploaded to S3: {key}")
            return True
        except Exception as e:
            print(f"✗ S3 upload failed for {key}: {e}")
            return False

    def download_file(self, key: str) -> Optional[bytes]:
        """
        Download file from S3

        Args:
            key: S3 object key (path)

        Returns:
            bytes: File data or None if failed
        """
        try:
            file_obj = io.BytesIO()
            self.client.download_fileobj(self.bucket_name, key, file_obj)
            file_obj.seek(0)
            return file_obj.read()
        except Exception as e:
            print(f"✗ S3 download failed for {key}: {e}")
            return None

    def get_presigned_url(self, key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate presigned URL for download

        Args:
            key: S3 object key (path)
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            str: Presigned URL or None if failed
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"✗ Failed to generate presigned URL for {key}: {e}")
            return None

    def delete_file(self, key: str) -> bool:
        """
        Delete file from S3

        Args:
            key: S3 object key (path)

        Returns:
            bool: True if successful
        """
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            print(f"✓ Deleted from S3: {key}")
            return True
        except Exception as e:
            print(f"✗ S3 delete failed for {key}: {e}")
            return False

    def file_exists(self, key: str) -> bool:
        """
        Check if file exists in S3

        Args:
            key: S3 object key (path)

        Returns:
            bool: True if file exists
        """
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False


# Global S3 client instance
s3_client = S3Client()
