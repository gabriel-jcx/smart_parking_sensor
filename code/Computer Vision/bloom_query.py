import base64
import struct
import numpy as np
from Crypto import Random
from Crypto.Cipher import AES
from binascii import unhexlify
from datetime import datetime
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
#unpad = lambda s : s[0:-ord(s[-1])]
temp_iv = '\xBA\x56\x9B\xEE\x2D\x68\x18\x02\x48\x13\x61\x16\x1e\x80\x33\x42'
class AESCipher:
   def __init__( self, key ,iv):
      self.key = key
      self.iv = iv
   def encrypt( self, raw ):
      raw = pad(raw)
      #iv = Random.new().read( AES.block_size )
      #print np.uint64(int(iv.encode('hex'),16))
      cipher = AES.new( self.key, AES.MODE_CBC, self.iv )
      #return base64.b64encode( iv + cipher.encrypt( raw ) )
      return cipher.encrypt(raw)
   """
   def decrypt( self, enc ):
      enc = base64.b64decode(enc)
      iv = enc[:16]
      cipher = AES.new(self.key, AES.MODE_CBC, iv )
      return unpad(cipher.decrypt( enc[16:] ))
   """

key1 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
key2 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
key3 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03'
key4 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04'
key5 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05'
bloom = [0] * 57
def bloom_query(param_iv):
   cipher1_text = ""
   cipher2_text = ""
   cipher3_text = ""
   cipher4_text = ""
   cipher5_text = ""
   query_index = []
   start = datetime.now()
   iv = ''
   for i in param_iv:
      temp = chr(i)
      iv += (temp)
   cipher1 = AESCipher(key1,iv)
   encrypted1 = cipher1.encrypt('test')
   for i in range(0,len(encrypted1)):
      cipher1_text = cipher1_text + str(int(encrypted1[i].encode('hex'),16))
   print int(cipher1_text)
   query_index.append(int(cipher1_text)%58)
   cipher2 = AESCipher(key2,iv)
   encrypted2 = cipher2.encrypt('test')
   for i in range(0,len(encrypted2)):
      cipher2_text = cipher2_text + str(int(encrypted2[i].encode('hex'),16))
   print int(cipher2_text)
   query_index.append(int(cipher2_text)%58)
   #print (int(encrypted2.encode('hex'),16))
   cipher3 = AESCipher(key3,iv)
   encrypted3 = cipher3.encrypt('test')
   for i in range(0,len(encrypted3)):
      cipher3_text = cipher3_text + str(int(encrypted3[i].encode('hex'),16))
   query_index.append(int(cipher3_text)%58)
   #print (int(encrypted3.encode('hex'),16))
   print int(cipher3_text)
   cipher4 = AESCipher(key4,iv)
   encrypted4 = cipher4.encrypt('test')
   for i in range(0,len(encrypted4)):
      cipher4_text = cipher4_text + str(int(encrypted4[i].encode('hex'),16))
   query_index.append(int(cipher4_text)%58)
   print int(cipher4_text)
   #print (int(encrypted4.encode('hex'),16))
   cipher5 = AESCipher(key5,iv)
   encrypted5 = cipher5.encrypt('test')
   for i in range(0,len(encrypted5)):
      cipher5_text = cipher5_text + str(int(encrypted5[i].encode('hex'),16))
   query_index.append(int(cipher5_text)%58)
   print int(cipher5_text)
   #print (int(encrypted5.encode('hex'),16))
   end = datetime.now()
   print end - start
   return query_index
query_index=bloom_query([133,235,86,95,46,255,59,63,196,230,175,5,220,141,194,246])
print query_index
for i in query_index:
    print i
#print(bloom)
#print struct.unpack("<L",encrypted)[0]
#print decrypted
