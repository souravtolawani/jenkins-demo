
import boto3
from datetime import datetime
from zoneinfo import ZoneInfo

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('TimeTable')

def lambda_handler(event, context):
    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    table.put_item(
        Item={
            'id': now.strftime('%Y-%m-%d-%H-%M-%S-%f'),
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S')
        }
    )

    return {
        'statusCode': 200,
        'body': 'Saved: ' + now.strftime('%Y-%m-%d %H:%M:%S')
    }


#----------------------------------------------------
# test
{}
