import os
import io
from google.cloud import vision
from google.cloud.vision import types
import sys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"
def detect_license_plate(image_file_name, length):
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
      if len(text.description) == length:
         print "Detected Number Plate is:"
         print text.description
         license_plates.append(text.description)
   return license_plates
license = "6LIK274" 
rets = detect_license_plate(sys.argv[1], len(license))
print rets
print rets[0]
for ret in rets:
   err = 0
   for i in range(0,len(ret)):
      if(license[i] != ret[i]):
         err+=1
   print err
   if (err <= 1):
      print "Success!"
