import os
import io
from google.cloud import vision
from google.cloud.vision import types
import sys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"
client = vision.ImageAnnotatorClient()
file_name = sys.argv[1]
with io.open(file_name, 'rb') as image_file:
   content = image_file.read()
image = types.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')
for text in texts:
   print('\n"{}"'.format(text.description))
