"""
S3 client for the IoT security camera system.
"""
import boto3
from utils.logger import logger

class S3Client:
    """Client for AWS S3 storage operations."""
    
    def __init__(self, bucket_name):
        """Initialize the S3 client.
        
        Args:
            bucket_name: Name of the S3 bucket
        """
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')
        logger.info(f"S3 client initialized for bucket: {bucket_name}")
        
    def upload_file(self, local_file, s3_key):
        """Upload a file to S3.
        
        Args:
            local_file: Path to local file
            s3_key: S3 object key (path in bucket)
            
        Returns:
            str or None: S3 URL if successful, None otherwise
        """
        logger.info(f"Uploading {local_file} to S3 bucket {self.bucket_name}")
        try:
            self.client.upload_file(local_file, self.bucket_name, s3_key)
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            logger.info(f"Upload complete: {s3_url}")
            return s3_url
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            return None
            
    def upload_files(self, file_paths, s3_prefix):
        """Upload multiple files to S3 with the same prefix.
        
        Args:
            file_paths: List of local file paths
            s3_prefix: S3 prefix to prepend to filenames
            
        Returns:
            list: List of successful S3 URLs
        """
        urls = []
        for file_path in file_paths:
            # Extract the filename from the path
            filename = file_path.split('/')[-1]
            # Create the S3 key with the prefix
            s3_key = f"{s3_prefix}/{filename}"
            # Upload the file
            url = self.upload_file(file_path, s3_key)
            if url:
                urls.append(url)
        return urls
