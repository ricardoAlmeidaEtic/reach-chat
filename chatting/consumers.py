from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chatting.models import Message
import json, os, datetime, base64
from projeto_chat.settings import BASE_DIR, STATIC_URL

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "chat_room"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        user = self.scope['user']
        
        message = text_data_json.get('message', '')
        imageData = text_data_json.get('imageData', '')
        imageName = text_data_json.get('imageName', '')

        filename = imageName

        if filename:
            self.handle_uploaded_file(imageData,imageName)
        
        # Send the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user.username,
                'message': message,
                'date': datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p"),
                'image': filename,
            }
        )

        message = Message(user=user, message=message, image=filename)
        
        message.save()


    # Receive message from group
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'user': event['user'],
            'message': event['message'],
            'date': event['date'],
            'image': event['image']
        }))
    
    def handle_uploaded_file(self, image_data: str, image_name: str):
        image_bytes = base64.b64decode(image_data.encode('utf-8'))

        filename = os.path.basename(image_name).split('/')[-1]

        print("fic: ",filename)

        file_path = os.path.join(BASE_DIR, STATIC_URL, filename)

        print("dir: ",file_path)

        with open(file_path, 'wb') as file:
            file.write(image_bytes)