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

# depricated log function since the cloud have log functionality
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


#get the qr code, extract the license plate and then npr
def get_code(image_filename):
   print ("decoding" + image_filename)
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
   try:
    image = Image.open(fp)
    image.load()
   except IOError:
       return "ERROR Image"
   codes = zbarlight.scan_codes('qrcode',image)
   print("The decoded code is ", codes)
   if not codes:
       print "Cannot retrieve qr code from the image, ", image_filename
       return "ERROR detecting QR"
   else:
       print ('QR code is: %s' % codes[0])
       permit_id = codes[0]
   user_plate = get_user_license_plate(permit_id)
   plate_length = len(user_plate)
   vehicle_plates = detect_license_plate(image_filename, plate_length)
   if vehicle_plates == "ERROR":
       return "ERROR IMGAE"
   print "The recognized vehicle plate is {}".format(vehicle_plates)
   for vehicle_plate in vehicle_plates:
      err_count = 0
      for i in range(0, plate_length):
         if(vehicle_plate[i] != user_plate[i]):
            err_count += 1
      if(err_count <= 1):
         return permit_id
   return "ERROR Permit and License Plate doesn't match"
# extract the license plate from cloud
def get_user_license_plate(permit_id):
   from google.cloud import datastore
   datastore_client = datastore.Client()
   ID = 'Permit Code-{}'.format(permit_id)
   with datastore_client.transaction():
      user_key = datastore_client.key('Student-Permit-Database', ID)
      user = datastore_client.get(user_key)
      print(user + "with permit" +ID)
      license_plate = user['License Plate(s)']
      print("User with permit {}, has the license plate {}".format(permit_id,license_plate))
      return license_plate

# npr based on google cloud vision
def detect_license_plate(image_file_name, length):
   from google.cloud import vision
   from google.cloud.vision import types
   import io
   try:
    client = vision.ImageAnnotatorClient()
    file_name = image_file_name
    with io.open(file_name, 'rb') as image_file:
       content = image_file.read()
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    #print response
    texts = response.text_annotations
    license_plates = []
    for text in texts:
       print text.description
       if len(text.description) == length:
          print "Detected Number Plate is:"
          print text.description
          license_plates.append(text.description)
    return license_plates
   except IOError:
       return "ERROR"
