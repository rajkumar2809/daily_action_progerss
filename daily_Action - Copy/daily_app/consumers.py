
from concurrent.futures import thread
from channels.generic.websocket import WebsocketConsumer 
from channels.consumer import SyncConsumer
# from channels.generic.websocket import WebsocketConsumer , SyncConsumer
from asgiref.sync import async_to_sync 
import json

from django.contrib.auth.models import User
from .models import Message, NewUser , Thread


# Chat MEssage consumer 


class ChatMessageConsumer(SyncConsumer):
    def websocket_connect(self , event):
        # when websocket connected successfully
        # print("connected successfully")
        self.room_name = "broadcast"
        self.send({
            "type":"websocket.accept"
        })

        async_to_sync(self.channel_layer.group_add)(self.room_name , self.channel_name)

        print(f'[{self.channel_name}] - You are connected ====...---')

    # data received part from fronted or from the server 
    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        # print(event)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type":"websocket.message",
                "text":event.get("text")
            }
        )

    
    def websocket_message(self , event):
        print("+++++web_socket message function get called ")
        print(event)
        # print(f'[{self.channel_name}] - Message Sent - {event["text"]}')
        self.send({
            "type":"websocket.send",
            "text":event.get("value")
        })

    
        # data received part from fronted or from the server 
    def websocket_disconnect(self, event):
        # print("connection disconnected")
        print(event)
        print(f'[{self.channel_name}] - Disconnected ')

        async_to_sync(self.channel_layer.group_discard(self.room_name , self.channel_name))
        # print(event)




class ChatConsumer(SyncConsumer):
    def websocket_connect(self , event):
        # when websocket connected successfully
        print("connected successfully")
        # scope of the users can be get from the module which is imported in the asgi.py Authmiddlewarestack
        me = self.scope['user'] # me means the login user 
        other_username = self.scope['url_route']['kwargs']['username'] # other_username is the user with whom you want chat
        print("other name is ")
        print(other_username)
        other_user = NewUser.objects.get(user_name = other_username)
        # other_user = User.objects.get(username = other_username)
        self.thread_obj = Thread.objects.get_or_create_personal_thread(me , other_user)
        self.room_name = f'personal_thread_{self.thread_obj.id}'


        async_to_sync(self.channel_layer.group_add)(self.room_name , self.channel_name)
        self.send({
            "type":"websocket.accept"
        })
        print(f'[{self.channel_name}] - You are connected ====...---')

    # data received part from fronted or from the server 
    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        print("=========the username is from websocket receive======")
        print(self.scope['user'].user_name)
        # print(event)
        msg = json.dumps({
            'text':event.get('text'),
            'username': self.scope['user'].user_name
        })
        print("the message is " , msg)

        #to sotre the message
        self.store_message(event.get('text'))

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type":"websocket.message",
                "text": msg
            }
        )
        # send the same message that has been received from js 
        # self.send ({
        #     "type":"websocket.send",
        #     "text":event.get('text')
        # })
    
    def websocket_message(self , event):
        print("+++++web_socket message function get called ")
        print(f'[{self.channel_name}] - Message Sent - {event["text"]}')
        self.send({
            "type":"websocket.send",
            "text":event.get("text")
        })

    
        # data received part from fronted or from the server 
    def websocket_disconnect(self, event):
        # print("connection disconnected")
        print(f'[{self.channel_name}] - Disconnected ')

        async_to_sync(self.channel_layer.group_discard(self.room_name , self.channel_name))
        # print(event)

    
    def store_message(self, text):

        Message.objects.create(
            thread = self.thread_obj,
            sender = self.scope['user'],
            text = text
        )


class GroupChatConsumer(SyncConsumer):
    def websocket_connect(self , event):
        # when websocket connected successfully
        # print("connected successfully")
        self.room_name = "broadcast"
        self.send({
            "type":"websocket.accept"
        })

        async_to_sync(self.channel_layer.group_add)(self.room_name , self.channel_name)

        print(f'[{self.channel_name}] - You are connected ====...---')

    # data received part from fronted or from the server 
    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        # print(event)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type":"websocket.message",
                "text":event.get("text")
            }
        )
        # send the same message that has been received from js 
        # self.send ({
        #     "type":"websocket.send",
        #     "text":event.get('text')
        # })
    
    def websocket_message(self , event):
        print("+++++web_socket message function get called ")
        print(f'[{self.channel_name}] - Message Sent - {event["text"]}')
        self.send({
            "type":"websocket.send",
            "text":event.get("text")
        })

    
        # data received part from fronted or from the server 
    def websocket_disconnect(self, event):
        # print("connection disconnected")
        print(event)
        print(f'[{self.channel_name}] - Disconnected ')

        async_to_sync(self.channel_layer.group_discard(self.room_name , self.channel_name))
        # print(event)