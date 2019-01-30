# coding: utf-8
from __future__ import unicode_literals
import sys
import base64
import os
import ast
import six
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class PublicKeyFileExists(Exception): pass


class RSAEncryption(object):
   PRIVATE_KEY_FILE_PATH = "private.key"
   PUBLIC_KEY_FILE_PATH = "public.key"

   def encrypt(self, message):
      public_key = self._get_public_key()
      public_key_object = RSA.importKey(public_key)
      print public_key
      encryptor = PKCS1_OAEP.new(public_key_object)
      print message
      encrypted_message = encryptor.encrypt(self._to_format_for_encrypt(message))
      # use base64 for save encrypted_message in database without problems with encoding
      return base64.b64encode(encrypted_message)
   def decrypt(self, encoded_encrypted_message):
      encrypted_message = base64.b64decode(encoded_encrypted_message)
      #encrypted_message = encoded_encrypted_message

      private_key = self._get_private_key()
      #private_key_object = RSA.importKey(private_key)
      decryptor = PKCS1_OAEP.new(private_key)
      decrypted_message = decryptor.decrypt(encrypted_message)
      return six.text_type(decrypted_message, encoding='utf8')
   def generate_keys(self):
      """Be careful rewrite your keys"""
      random_generator = Random.new().read
      key = RSA.generate(1024, random_generator)
      private, public = key.exportKey(), key.publickey().exportKey()
      print self.PRIVATE_KEY_FILE_PATH
      with open(self.PRIVATE_KEY_FILE_PATH, 'w') as private_file:
         private_file.write(private)
      with open(self.PUBLIC_KEY_FILE_PATH, 'w') as public_file:
         public_file.write(public)
      return private, public

   def create_directories(self, for_private_key=True):
      public_key_path = "public.key"
      print public_key_path
      if not os.path.exists(public_key_path):
         os.makedirs(public_key_path)
      if for_private_key:
         private_key_path = "private.key"
         if not os.path.exists(private_key_path):
            os.makedirs(private_key_path)
            

   def _get_public_key(self):
      """run generate_keys() before get keys """
      with open(self.PUBLIC_KEY_FILE_PATH, 'r') as _file:
         return _file.read()

   def _get_private_key(self):
      """run generate_keys() before get keys """
      with open(self.PRIVATE_KEY_FILE_PATH, 'r') as _file:
         return _file.read()

   def _to_format_for_encrypt(self,value):
      if isinstance(value, int):
         return six.binary_type(value)
      for str_type in six.string_types:
         if isinstance(value, str_type):
            return value.encode('utf8')
      if isinstance(value, six.binary_type):
         return value
KEYS_DIRECTORY = ""           
class TestingEncryption(RSAEncryption):

   PRIVATE_KEY_FILE_PATH = KEYS_DIRECTORY + "private.key"
   PUBLIC_KEY_FILE_PATH = KEYS_DIRECTORY + "public.key"

# django/flask
from django.core.files import File

class ProductionEncryption(RSAEncryption):
   PUBLIC_KEY_FILE_PATH = "public.key"

   def _get_private_key(self):
      #run generate_keys() before get keys
      #from corportal.utils import global_elements
      #private_key = global_elements.request.FILES.get("private_key")
      private_key = RSA.importKey(open('private.key').read())
      #if private_key:
      #   private_key_file = File(private_key)
      return private_key
#ProductionEncryption().generate_keys()
def generate_key_pair():
   ProductionEncryption().generate_keys()
def encrypt(message):
   encrypted_mes = ProductionEncryption().encrypt(message)
   print encrypted_mes
   f = open("encrypted_message","w")
   f.write(encrypted_mes)
   f.close()
   return encrypted_mes
   print "Finish encrypting"
def decrypt():
   f_new = open("encrypted_message","r")
   encry_mes = f_new.read()
   f_new.close()
   decrypted_mes = ProductionEncryption().decrypt(encry_mes)
   print "The decrypted message is:"
   print decrypted_mes
   return decrypted_mes 

