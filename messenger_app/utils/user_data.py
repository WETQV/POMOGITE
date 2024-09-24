import json
import os
import string
import random
from kivy.utils import platform
from PIL import Image as PILImage
from datetime import datetime
import uuid
from models.chat import Chat, Message

class UserData:
    def __init__(self):
        self.data = {
            'user_id': '',
            'nickname': '',
            'avatar': '',
            'contacts': {},
            'chats': {},
            'favorite_messages': []
        }
        self.data_file = 'user_data.json'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                loaded_data = json.load(file)
                # Обновляем данные, сохраняя структуру по умолчанию
                self.data.update(loaded_data)
        else:
            self.save_data()

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def get_user_id(self):
        return self.data.get('user_id', '')

    def set_user_id(self, user_id):
        self.data['user_id'] = user_id
        self.save_data()

    def get_nickname(self):
        return self.data.get('nickname', '')

    def set_nickname(self, nickname):
        self.data['nickname'] = nickname
        self.save_data()

    def get_avatar(self):
        return self.data.get('avatar', '')

    def set_avatar(self, avatar_path):
        self.data['avatar'] = avatar_path
        self.save_data()

    def get_contacts(self):
        return self.data.get('contacts', {})

    def add_contact(self, user_id, nickname=''):
        if 'contacts' not in self.data:
            self.data['contacts'] = {}
        self.data['contacts'][user_id] = {'nickname': nickname}
        self.save_data()

    def remove_contact(self, user_id):
        if 'contacts' in self.data and user_id in self.data['contacts']:
            del self.data['contacts'][user_id]
            self.save_data()

    def get_chats(self):
        return self.data.get('chats', {})

    def get_all_chats(self):
        return list(self.data.get('chats', {}).items())

    def add_chat(self, chat_id, chat_data):
        self.data['chats'][chat_id] = chat_data
        self.save_data()

    def remove_chat(self, chat_id):
        if chat_id in self.data['chats']:
            del self.data['chats'][chat_id]
            self.save_data()
            return True
        return False

    def search_user(self, user_id):
        return self.data.get('contacts', {}).get(user_id, None)

    def create_or_get_chat(self, user_id):
        for chat_id, chat in self.chats.items():
            if user_id in chat.participants:
                return chat_id
        
        new_chat_id = str(uuid.uuid4())
        self.chats[new_chat_id] = Chat(new_chat_id, [self.user_id, user_id])
        self.save_data()
        return new_chat_id

    def add_message_to_favorites(self, message, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.favorite_messages.append({
            'text': message,
            'timestamp': timestamp,
            'sender': self.get_nickname(),
            'avatar': self.get_avatar()
        })
        self.save_data()

    def get_favorite_messages(self):
        return self.data.get('favorite_messages', [])

    def add_favorite_message(self, message):
        if 'favorite_messages' not in self.data:
            self.data['favorite_messages'] = []
        self.data['favorite_messages'].append(message)
        self.save_data()

    def remove_favorite_message(self, message):
        if 'favorite_messages' in self.data:
            self.data['favorite_messages'].remove(message)
            self.save_data()

    def get_chat(self, chat_id):
        return self.data['chats'].get(chat_id, None)

    def add_message_to_chat(self, chat_id, message):
        if chat_id not in self.data['chats']:
            self.data['chats'][chat_id] = {'messages': []}
        self.data['chats'][chat_id]['messages'].append(message)
        self.save_data()

    def delete_chat(self, chat_id):
        if chat_id in self.data['chats']:
            del self.data['chats'][chat_id]
            self.save_data()
            return True
        return False

user_data = UserData()