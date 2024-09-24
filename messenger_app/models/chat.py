from datetime import datetime
import uuid

class Message:
    def __init__(self, sender_id, text, timestamp=None, is_read=False):
        self.sender_id = sender_id
        self.text = text
        self.timestamp = timestamp or datetime.now()
        self.is_read = is_read

    def to_dict(self):
        return {
            'sender_id': self.sender_id,
            'text': self.text,
            'timestamp': self.timestamp.isoformat(),
            'is_read': self.is_read
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sender_id=data['sender_id'],
            text=data['text'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            is_read=data['is_read']
        )

    def mark_as_read(self):
        self.is_read = True

class Chat:
    def __init__(self, chat_id, participants):
        self.chat_id = chat_id
        self.participants = participants
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_last_message(self):
        return self.messages[-1] if self.messages else None

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'participants': self.participants,
            'messages': [message.to_dict() for message in self.messages]
        }

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, list):
            # Если data - список, предполагаем, что это список участников
            return cls(str(uuid.uuid4()), data)
        elif isinstance(data, dict):
            chat_id = data.get('chat_id', str(uuid.uuid4()))
            participants = data.get('participants', [])
            chat = cls(chat_id, participants)
            chat.messages = [Message.from_dict(msg_data) for msg_data in data.get('messages', [])]
            return chat
        else:
            # Если data не список и не словарь, создаем пустой чат
            return cls(str(uuid.uuid4()), [])
