import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WebSocketConnections')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event.get('body', ))
    lang = body.get('lang', 'unknown')
    #just in case selected language has not been set
    if lang not in ['en', 'es','fr']:
        lang = 'en'
    username = body.get('username', 'Guest')
    # Update the language for the current connectionId and update user name
    table.update_item(
         Key={'connectionId': connection_id},
        UpdateExpression="SET lang = :lang, username = :username",
        ExpressionAttributeValues={
            ':lang': lang,
            ':username': username
        }
    )

    return {'statusCode': 200}