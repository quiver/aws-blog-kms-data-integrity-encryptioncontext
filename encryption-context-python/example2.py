#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import boto3
from  boto3.dynamodb.types import Binary
from boto3.dynamodb.conditions import Key

from conf import TABLE, ADDRESS, EMAIL, KEYID

# DO NOT USE
def save_address(email, address):
    ciphertext = kms.encrypt(
      KeyId = KEYID,
      Plaintext = address)['CiphertextBlob']
   
    table.put_item(
      TableName = TABLE,
      Item = {
        EMAIL : email,
        ADDRESS : Binary(ciphertext)
    })

# DO NOT USE
def get_address(email):
    response = table.query(
      KeyConditionExpression=Key(EMAIL).eq(email))
    item = response['Items'][0]

    #dec = kms.decrypt(CiphertextBlob = item[ADDRESS]) # <- fails
    dec = kms.decrypt(CiphertextBlob = str(item[ADDRESS]))
    return dec['Plaintext']

# Encrypt the data
dynamodb = boto3.resource('dynamodb')
kms = boto3.client('kms')

table = dynamodb.Table(TABLE)

# Alice stores her address
save_address("alice@example.com", "Alice Lovelace, 123 Anystreet Rd., Anytown, USA");
# Mallory stores her address
save_address("mallory@example.com", "Mallory Evesdotir, 321 Evilstreed Ave., Despair, USA");

# Output saved addresses
print "Alice's Address: " + get_address("alice@example.com")
print "Mallory's Address: " + get_address("mallory@example.com")

# Mallory tampers with the database by swapping the encrypted addresses.
# Note that this doesn't require modifying the ciphertext at all.
# First, retrieve the records from DynamoDB

mallorysRecord = table.query(
      KeyConditionExpression=Key(EMAIL).eq("mallory@example.com"))['Items'][0]

allicesRecord = table.query(
      KeyConditionExpression=Key(EMAIL).eq("alice@example.com"))['Items'][0]

# Second, extract the encrypted addresses
mallorysEncryptedAddress = mallorysRecord[ADDRESS]
allicesEncryptedAddress = allicesRecord[ADDRESS]

# Third, swap the encrypted addresses
mallorysRecord[ADDRESS] = allicesEncryptedAddress
allicesRecord[ADDRESS] = mallorysEncryptedAddress

# Finally, store them back in DynamoDB
table.put_item(
  TableName = TABLE,
  Item = mallorysRecord)

table.put_item(
  TableName = TABLE,
  Item = allicesRecord)

# Now, when Alice tries to use her address (say to get something shipped to her)
# it goes to Mallory instead.
print "Alice's Address: " + get_address("alice@example.com")
# Likewise, if Mallory tries to look up her address, she can view Alice's instead
print "Mallory's Address: " + get_address("mallory@example.com")
