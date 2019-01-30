import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
random = Random.new().read
key = RSA.generate(2048, random)
public_key = key.publickey()
encrypted = public_key.encrypt('encrypt this message', 32)
print encrypted
