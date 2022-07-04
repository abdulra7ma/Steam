#consumers это весрия предствлений django для канала за исключением того что они делают больше чем просто 
#отвечают на запросы  от клиента они также могут инициировать запросы к клиенту сохраняя открытое соединение

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept() #        Accepts an incoming socket


        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': "you are now connected"
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))