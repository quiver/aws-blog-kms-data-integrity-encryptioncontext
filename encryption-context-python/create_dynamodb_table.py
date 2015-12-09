#!/usr/bin/env python
# vim: set fileencoding=utf8 :
import boto3

from conf import TABLE, EMAIL

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName=TABLE,
    KeySchema=[
        {
            'AttributeName' : EMAIL,
            'KeyType' : 'HASH'
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName' : EMAIL,
            'AttributeType' : 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits'  : 1,
        'WriteCapacityUnits' : 1
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName=TABLE)

# Print out some data about the table.
print(table.item_count)
