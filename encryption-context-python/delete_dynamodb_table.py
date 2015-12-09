#!/usr/bin/env python
# vim: set fileencoding=utf8 :
import boto3

from conf import TABLE

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE)
table.delete()

# Wait until the table exists.
table.meta.client.get_waiter('table_not_exists').wait(TableName=TABLE)
print "table deleted"
