#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import traceback

import boto3
import botocore

from conf import KEYID

kms = boto3.client('kms')

plaintext = "My very secret message"
print "Plaintext: " + plaintext

# Encrypt the data
ciphertext = kms.encrypt(
  KeyId = KEYID,
  Plaintext = plaintext)['CiphertextBlob']

# Decrypt the data
decrypted = kms.decrypt(CiphertextBlob = ciphertext)['Plaintext']
print "Decrypted: " + decrypted

# Attempt to tamper with the ciphertext
tamperedCt = ciphertext
# Flip all the bits in a byte 24 bytes from the end
tamperedCt = ''.join(chr(ord(c) ^ 0xff) if idx == len(tamperedCt) - 24 else c for idx, c in enumerate(tamperedCt))

try:
    decrypted2 = kms.decrypt(CiphertextBlob = tamperedCt)['Plaintext']
except botocore.exceptions.ClientError as e:
    print traceback.format_exc()
