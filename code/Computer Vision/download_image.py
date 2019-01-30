import os
from google.cloud import storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"
def download_blob(bucket_name, source_blob_name, destination_file_name):
   storage_client = storage.Client()
   bucket = storage_client.get_bucket(bucket_name)
   blob = bucket.blob(source_blob_name)
   blob.download_to_filename(destination_file_name)
   print('File {} upload to {}.'.format(source_blob_name, destination_file_name))

download_blob("images-uploadviagateway","qrcode.jpg", "123/123qrcode.jpg")
