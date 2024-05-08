from google.cloud import storage
from .singleton import singleton
from io import BytesIO
import logging

@singleton
class CloudStorageService:

    """
    Cloud Storage Service 

    Helper functions to upload and download files from Google Cloud Storage
    """
    def __init__(self) -> None:
        self.storage_client = storage.Client()

        self.bucket_name = "proteus-local"

        # TODO: do i need to create the bucket? - just do that in the console? 
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def upload_file(self, file_name, file_data):
        """
        Upload file
        Given a file name (defined before calling this function, and the file data, upload the file to the cloud storage)
        Returns the url of the newly created resource
        """
        blob = self.bucket.blob(file_name)
        blob.upload_from_file(BytesIO(file_data))

        logging.info(f"Uploaded {file_name} to {blob.public_url}")
        
        return blob.public_url



    
