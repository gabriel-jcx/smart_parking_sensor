# This file need python library zbarlight, a qrcode scanner
# wrapper in python. 
# In order to run the following code, run:
# for PIL library:
# sudo pip install pillow   
# for zbarlight:
# sudo apt-get install libzbar0 libzbar-dev
# sudo pip install zbarlight
import sys
def get_code(image_filename):
    from PIL import Image
    import zbarlight
    import sys
    fp=open(image_filename,'rb')
    if not fp:
        print "Error: file " + image_filename + "doesn't exist"
        return "Error: file " + image_filename + "doesn't exist"
    image = Image.open(fp)
    image.load()
    codes = zbarlight.scan_codes('qrcode',image)
    if not codes:
        print "Cannot retrieve qr code from the image, ",image_filename
        return "ERROR"
    else:
        print ('QR code is: %s' % codes[0])
        return codes[0]
qr_code = get_code(sys.argv[1])
print qr_code
