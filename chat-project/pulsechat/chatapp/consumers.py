from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import Group, GroupMessages, PulseChatUsers, Chat, Messages
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user'] 
        url_path = self.scope['path']

        if '/ws/chatroom/' in url_path:
            # Group chat connection

            self.chatroom_name = self.scope['url_route']['kwargs']['g_name'] 
            self.chatroom = get_object_or_404(Group, name=self.chatroom_name)
            self.chat_type = 'group'

            async_to_sync(self.channel_layer.group_add)(
                self.chatroom.name, self.channel_name
            )

            # add and update online users
            if self.user not in self.chatroom.online_members.all():
                self.chatroom.online_members.add(self.user)
                self.update_online_count()

            self.accept()

        elif '/ws/chat/' in url_path:
        
            # One-on-one chat connection
            self.freind_email = self.scope['url_route']['kwargs']['freind_email'] 
            self.chat_user1 = get_object_or_404(PulseChatUsers, email=self.user.email)
            self.chat_user2 = get_object_or_404(PulseChatUsers, email=self.freind_email)
            chat_names = [f'{self.chat_user1.username}_{self.chat_user2.username}', f'{self.chat_user2.username}_{self.chat_user1.username}']
            self.chatroom = Chat.objects.filter(name__in=chat_names).distinct().first()
            self.chat_type = 'one_on_one'

            async_to_sync(self.channel_layer.group_add)(
                self.chatroom.name, self.channel_name
            )
            
            self.chat_user1.is_online = True
            self.chat_user1.save()
            self.online_check()

            self.accept()

        else:
            self.close() 
            return
        

        
    def disconnect(self, close_code):
        url_path = self.scope['path']
        if '/ws/chatroom/' in url_path:

            # Group chat
            async_to_sync(self.channel_layer.group_discard)(
                self.chatroom.name, self.channel_name
            )

            if self.user in self.chatroom.online_members.all():
                self.chatroom.online_members.remove(self.user)
                self.update_online_count()

        elif '/ws/chat/' in url_path:

            # One-on-one chat
            if self.chatroom:
                async_to_sync(self.channel_layer.group_discard)(
                    self.chatroom.name, self.channel_name
                )

                self.chat_user1.is_online = False
                self.chat_user1.save()
                self.online_check()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['text_content']

        if self.chat_type == 'group':

            message = GroupMessages(
                sender = self.user,
                group = self.chatroom,
                text_content = body
            )
            message.save()

            event = {
                'type': 'message_handler',
                'message_id': message.id
            }

            async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
            )

        elif self.chat_type == 'one_on_one':
            message = Messages(
                sender = self.user,
                chat = self.chatroom,
                text_content = body
            )
            message.save()

            event = {
                'type': 'message_handler',
                'message_id': message.id
            }

            async_to_sync(self.channel_layer.group_send)(
            self.chatroom.name, event
            )


    def message_handler(self, event):
        message_id = event['message_id']

        if self.chat_type == 'group':
            last_message = GroupMessages.objects.get(id=message_id)
            context = {
                'user': self.user,
                'last_message': last_message
            }
            html = render_to_string("onlymessages.html", {'last_message': context})
            self.send(text_data=html)

        elif self.chat_type == 'one_on_one':
            last_message = Messages.objects.get(id=message_id)

            context = {
                'user': self.user,
                'last_message': last_message
            }

            html = render_to_string("onlymessages.html", {'last_message': context})
            self.send(text_data=html)

    def online_check(self):
        is_freind_online = self.chat_user2.is_online
        online_check = 'online' if is_freind_online else 'offline'

        event = {
            'type': 'online_status_handler',
            'online_check': online_check
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom.name, event
        )


    def online_status_handler(self, event):
        online_status = event['online_check']
        html = render_to_string("online_check.html", {'online_check': online_status})
        self.send(text_data=html)



    def update_online_count(self):
        online_count = self.chatroom.online_members.count() - 1
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom.name, event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string("online_count.html", {'online_count': online_count})
        self.send(text_data=html)

        