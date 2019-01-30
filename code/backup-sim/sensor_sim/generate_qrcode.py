# In order for the following code to run, couple dependent libraries
# need to be installed.
# Do command:
# sudo pip install pypng
# sudo apt-get install libpng-dev
# sudo apt-get install zlib1g-dev
import pyqrcode
import sys
from PIL import Image
qr = pyqrcode.create(sys.argv[1])
qr.png(sys.argv[2], scale=6)
im = Image.open(sys.argv[2])
rgb_im = im.convert('RGB')
rgb_im.save(sys.argv[2])
def generate_qrcode(input_string,out_filename):
   code = pyqrcode.create(input_string)
   code.png(out_filename, scale = 6)
   im = Image.open(out_filename)
   rgb_im = im.convert('RGB')
   rgb_im.save(out_filename)
