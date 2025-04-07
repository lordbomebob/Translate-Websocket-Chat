# 1.1 Project  
## Translate-Websocket-Chat  

### 1.2 Description  
A live web chat that translates languages and key terms.  

## 2.1 Purpose  
To translate messages between different languages while also translating certain technical jargon.  

## 2.2 Scope  

## 2.3 Requirements  

### 2.3.1 Functional Requirements  
- Able to send messages to others.  
- Translate user language for other users to understand.  
- Translate certain words for their purpose rather than a 1-to-1 definition.  

### 2.3.2 Non-Functional Requirements  
- Performance  
- Reliability  

### 2.3.3 Technical Requirements  
- **Hardware:** AWS server  
- **Software:** AWS, Python  

## 3.1 WebSocket Operations  
- `WebSocket-connect`  
- `WebSocket-disconnect`  
- `SendMessage`  
- `WebSocket gateway`  

## 4. Database Schema  

### WebSocketConnections  
```json
{
  "connectionId": "<connection_id>"
}
###ChatMessages
Field	Type	Description
messageId	String	Unique identifier for the message
language	String	Language of the message
originalMessage	String	The original message sent by the user
sender	String	The user who sent the message
timestamp	String	The time the message was sent
translatedMessage	String	The translated version of the message
