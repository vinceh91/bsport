from boto3 import client

client = client('dynamodb', endpoint_url='http://localhost:8000')


def create_table():
    table_name = 'Event'
    existing_tables = client.list_tables()['TableNames']
    if table_name not in existing_tables:
        client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'a',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'a',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )


if __name__ == '__main__':
    my_table = create_table()
