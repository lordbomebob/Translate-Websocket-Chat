import json
import boto3
import time
import uuid

dynamodb = boto3.resource('dynamodb')
translate = boto3.client(service_name='translate', region_name='us-west-1', use_ssl=True)


table = dynamodb.Table('WebSocketConnections')
table_chat = dynamodb.Table('ChatMessages')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event['body'])
    message = body['message']
    sender_lang = body['senderLang']  # e.g., "es" for Spanish
    endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
    apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url) 
    
    # Get sender info (username)
    sender_info = table.get_item(Key={'connectionId': connection_id}).get('Item', {})
    sender_name = sender_info.get('username', 'Guest')
    
    table_chat.put_item(Item={
        'messageId': str(uuid.uuid4()),
        'timestamp': int(time.time()),
        'sender': connection_id,
        'originalMessage': message,
        'senderUsername': sender_name,
        'language': sender_lang
    })
    # Retrieve all connections
    connections = table.scan().get('Items', [])


    # Send translated message to all users
    for conn in connections:
        try:
            target_lang = conn.get('lang', 'en')
            translated_text = translate.translate_text(
                Text=message, 
                SourceLanguageCode=sender_lang, 
                TargetLanguageCode=target_lang
            )['TranslatedText']
            apigateway.post_to_connection(
                ConnectionId=conn['connectionId'],
                Data=json.dumps({
                    'original': message, 
                    'translated': translated_text,
                    'originLang': sender_lang,
                    'sender': sender_name,
                    })
            )
        except Exception as e:
            print(f"Error sending message to connection {conn['connectionId']}: {str(e)}")
    return {'statusCode': 200}
