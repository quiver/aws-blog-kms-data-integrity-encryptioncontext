import base64
import traceback

import boto3
import botocore
from  boto3.dynamodb.types import Binary
from boto3.dynamodb.conditions import Key, Attr

# Turn on high-level logging:
# boto3.set_stream_logger(name='boto3')
# Turn on low-level and wire logging:
# boto3.set_stream_logger(name='botocore')

from conf import TABLE, ADDRESS, EMAIL

# Encrypt the data
dynamodb = boto3.resource('dynamodb')
kms = boto3.client('kms')

table = dynamodb.Table(TABLE)

for address in ("alice@example.com", "mallory@example.com"):
    print "delete: %s" % address
    table.delete_item(
      Key = {
        EMAIL : address
      }
    )
