from boto3 import client
from api.models import Event, Appointment

client = client('dynamodb', endpoint_url='http://localhost:8000')


def list_events():
    events = []
    for data in client.scan(TableName=Event.table_name)['Items']:
        events.append(Event(appointment=__fetch_appointment(data['Appointment']['N']),
                      description=data['Description']['S']))
    return events


def insert_event(event):
    item = {
        'Appointment': {'N': str(event.appointment.id)},
        'Description': {'S': event.description}
    }
    client.put_item(
        TableName=Event.table_name,
        Item=item
    )


def update_event(event):
    client.update_item(
        TableName=Event.table_name,
        Key={'Appointment': {'N': str(event.appointment.id)}},
        UpdateExpression='SET Description = :new_description',
        ExpressionAttributeValues={':new_description': {'S': event.description}}
    )


def __fetch_appointment(id):
    return Appointment.objects.get(id=id)
