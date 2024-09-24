from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from utils.user_data import user_data
from widgets.rounded_button import RoundedButton
from kivy.uix.textinput import TextInput

class ChatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(text="Чат", font_size=dp(24), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1))
        self.layout.add_widget(title)
        
        self.chat_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        self.layout.add_widget(self.chat_layout)
        
        self.message_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[10, 10, 10, 10]
        )
        self.layout.add_widget(self.message_input)
        
        send_button = RoundedButton(text="Отправить", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        send_button.bind(on_press=self.send_message)
        self.layout.add_widget(send_button)
        
        back_button = RoundedButton(text="Назад", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)
        
        self.chat_id = None

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id
        self.load_chat_messages()

    def load_chat_messages(self):
        self.chat_layout.clear_widgets()
        if self.chat_id:
            chat_data = user_data.get_chat(self.chat_id)
            if chat_data:
                for message in chat_data.get('messages', []):
                    self.add_message_to_chat(message)

    def add_message_to_chat(self, message):
        sender = message.get('sender', 'Unknown')
        text = message.get('text', '')
        message_label = Label(
            text=f"{sender}: {text}",
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1)
        )
        self.chat_layout.add_widget(message_label)

    def send_message(self, instance):
        if self.chat_id and self.message_input.text:
            message = {
                'sender': user_data.get_nickname(),
                'text': self.message_input.text
            }
            user_data.add_message_to_chat(self.chat_id, message)
            self.add_message_to_chat(message)
            self.message_input.text = ''

    def go_back(self, instance):
        self.manager.current = 'chats_list'

    def on_pre_enter(self):
        self.load_chat_messages()