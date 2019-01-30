#The function import certain useful 


def upload_blob(bucket_name, source_file_name, destination_blob_name):
   import os
   from google.cloud import storage
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"
   storage_client = storage.Client()
   bucket = storage_client.get_bucket(bucket_name)
   blob = bucket.blob(destination_blob_name)
   blob.upload_from_filename(source_file_name)
   print('File {} upload to {}.'.format(source_file_name, destination_blob_name))

def download_blob(bucket_name, source_blob_name, destination_file_name):
   import os
   from google.cloud import storage
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"
   try:
      storage_client = storage.Client()
      bucket = storage_client.get_bucket(bucket_name)
      blob = bucket.blob(source_blob_name)
      blob.download_to_filename(destination_file_name)

      print('File {} download to {}.'.format(source_blob_name, destination_file_name))
      print blob
      return "Success"
   except:
      print('File {} not found in goolge cloud.'.format(source_blob_name))
      return "Doesn't Exist"

def log(log_bucket_name, Spot_ID, status, user_code):
   from datetime import datetime
   #upload_blob(image_bucket_name, source_image_filename, destination_image_name
   now = datetime.now()
   year = str(now.year) + "_"
   month = str(now.month) +"_"
   day = str(now.day) + "_"
   hour = str(now.hour)
   log_filename = Spot_ID+"_"+year+month+day+hour+".txt"
   data = str(now)+ "," + status+ "," + user_code+"\n"
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


def get_code(image_filename):
    from PIL import Image
    import zbarlight
    import sys
    if (image_filename.endswith('.bmp')):
        import sys
        import subprocess
        tmp_name = image_filename.split('.')
        subprocess.call(["convert",'-flop',image_filename,tmp_name[0]+'.jpg'])
        image_filename = tmp_name[0]+'.jpg'
    fp=open(image_filename,'rb')
    if not fp:
        print "Error: file " + image_filename + "doesn't exist"
        return 0
    image = Image.open(fp)
    image.load()
    codes = zbarlight.scan_codes('qrcode',image)
    if not codes:
        print "Cannot retrieve qr code from the image, ", image_filename
        return "ERROR"
    else:
        print ('QR code is: %s' % codes[0])
        return codes[0]
