import json
import boto3
import time
import uuid

dynamodb = boto3.resource('dynamodb')
translate = boto3.client(service_name='translate', region_name='us-west-1', use_ssl=True)


table = dynamodb.Table('WebSocketConnections')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    message = body['message']
    target_lang = body['targetLang']  # e.g., "es" for Spanish
    endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
    apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
    # Translate message
    translated_text = translate.translate_text(Text=message, SourceLanguageCode="en", TargetLanguageCode=target_lang)['TranslatedText']
    print(translated_text)   
    # Retrieve all connections
    connections = table.scan()['Items']
    
    table_chat = dynamodb.Table('ChatMessages')
    table_chat.put_item(Item={
        'messageId': str(uuid.uuid4()),
        'timestamp': int(time.time()),
        'sender': connection_id,
        'originalMessage': message,
        'translatedMessage': translated_text,
        'language': target_lang
    })

    # Send translated message to all users
    for conn in connections:
        try:
            apigateway.post_to_connection(
                ConnectionId=conn['connectionId'],
                Data=json.dumps({'original': message, 'translated': translated_text})
            )
        except Exception as e:
            print(f"Error sending message to connection {conn['connectionId']}: {str(e)}")
    return {'statusCode': 200}