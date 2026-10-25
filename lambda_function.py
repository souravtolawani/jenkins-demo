import json
import uuid
import base64
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Registration')   

def lambda_handler(event, context):
    try:
        body = event.get('body') or '{}'

        
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body).decode('utf-8')

      
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {k: v[0] for k, v in parse_qs(body).items()}

        
        data['id'] = str(uuid.uuid4())

        
        table.put_item(Item=data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Registration successful', 'id': data['id']})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
