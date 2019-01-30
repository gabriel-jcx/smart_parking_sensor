import os
from google.cloud import storage
from datetime import datetime
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"
def upload_blob(bucket_name, source_file_name, destination_blob_name):
   storage_client = storage.Client()
   bucket = storage_client.get_bucket(bucket_name)
   blob = bucket.blob(destination_blob_name)
   blob.upload_from_filename(source_file_name)
   print('File {} upload to {}.'.format(source_file_name, destination_blob_name))
def download_blob(bucket_name, source_blob_name, destination_file_name):
   try:
      storage_client = storage.Client()
      bucket = storage_client.get_bucket(bucket_name)
      blob = bucket.blob(source_blob_name)
      blob.download_to_filename(destination_file_name)
      print('File {} download to {}.'.format(source_blob_name, destination_file_name))
      return "Success"
   except:
      print('File {} not found in goolge cloud.'.format(source_blob_name))
      return "Doesn't Exist"

def log( log_bucket_name, Spot_ID):
   #upload_blob(image_bucket_name, source_image_filename, destination_image_name
   now = datetime.now()
   year = str(now.year) + "."
   month = str(now.month) +"."
   day = str(now.day) + "."
   hour = str(now.hour)
   log_filename = Spot_ID+"_"+year+month+day+hour+".txt"
   data = str(now)+"\n"
   status = download_blob(log_bucket_name, log_filename, log_filename)
   if status == "Success":
      log = open(log_filename, "a")
      log.write(data)
      log.close()
   else:   
      new_log = open(log_filename, "w")
      new_log.write(data)
      new_log.close()
   upload_blob(log_bucket_name, log_filename, log_filename)

#test functioncalls of this file
#download_blob("images-uploadviagateway","sfasdfwe/sdfasf","abc.abc")
#upload_blob("images-uploadviagateway","test.jpg", "qrcode.jpg")
log("log-uploadviagateway", "1_")
