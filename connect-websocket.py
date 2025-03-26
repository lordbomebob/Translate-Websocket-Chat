import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_connections = dynamodb.Table('WebSocketConnections')
table_chat = dynamodb.Table('ChatMessages')


def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"]
    apigateway = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
    # Store connection ID
    table_connections.put_item(Item={'connectionId': connection_id})
    
    # Fetch last 10 messages (adjust as needed)
    response = table_chat.scan(
        Limit=10,  # Get last 10 messages
    )
    
    chat_history = response.get('Items', [])

    # Send chat history to the new user
    if chat_history:
        print(chat_history)
        #apigateway.post_to_connection(
        #    ConnectionId=connection_id,
        #    Data=json.dumps({'chatHistory': chat_history})
        #)
    
    return {'statusCode': 200}

