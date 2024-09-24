from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from utils.user_data import user_data
from datetime import datetime, timedelta
from widgets.rounded_button import RoundedButton

class MessageBubble(FloatLayout):
    def __init__(self, message, last_message_time, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.padding = dp(10)
        self.spacing = dp(5)

        if isinstance(message, dict):
            avatar_source = message.get('avatar') or 'D:/photomode_30052024_162743.png'
            sender = message.get('sender', 'Unknown')
            text = message.get('text', '')
            timestamp = datetime.strptime(message.get('timestamp'), "%Y-%m-%d %H:%M:%S")
        else:
            avatar_source = 'D:/photomode_30052024_162743.png'
            sender = 'Unknown'
            text = str(message)
            timestamp = datetime.now()

        # Аватар
        avatar = AsyncImage(source=avatar_source, size_hint=(None, None), size=(dp(30), dp(30)))
        avatar.pos_hint = {'right': 1, 'top': 1}
        self.add_widget(avatar)

        # Имя отправителя
        sender_label = Label(text=sender, size_hint=(None, None), size=(dp(100), dp(20)))
        sender_label.pos_hint = {'right': 0.9, 'top': 1}
        self.add_widget(sender_label)

        # Сообщение
        message_background = FloatLayout(size_hint=(None, None))
        with message_background.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = RoundedRectangle(radius=[dp(15)])
        
        message_label = Label(text=text, size_hint=(None, None), padding=(dp(10), dp(5)))
        message_label.texture_update()
        message_label.size = (min(message_label.texture_size[0], Window.width * 0.7), message_label.texture_size[1])
        
        message_background.size = (message_label.width + dp(20), message_label.height + dp(10))
        message_background.pos_hint = {'right': 0.95, 'top': 0.9}
        
        message_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        message_background.add_widget(message_label)
        self.add_widget(message_background)

        # Временная метка
        if last_message_time is None or (timestamp - last_message_time) > timedelta(minutes=2):
            timestamp_label = Label(text=timestamp.strftime("%Y-%m-%d %H:%M"), size_hint=(None, None), 
                                    size=(dp(100), dp(20)), font_size='10sp', color=(0.5, 0.5, 0.5, 1))
            timestamp_label.pos_hint = {'right': 0.95, 'y': 0}
            self.add_widget(timestamp_label)
            self.height = avatar.height + message_background.height + timestamp_label.height + dp(15)
        else:
            self.height = avatar.height + message_background.height + dp(10)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class FavoritesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.layout.add_widget(Label(text="Избранное", font_size=dp(24), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1)))
        
        self.messages_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.8))
        self.scroll_view.add_widget(self.messages_layout)
        self.layout.add_widget(self.scroll_view)
        
        back_button = RoundedButton(text="Назад", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        back_button.bind(on_release=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.update_messages()

    def update_messages(self):
        self.messages_layout.clear_widgets()
        messages = user_data.get_favorite_messages()
        for message in messages:
            message_button = RoundedButton(
                text=f"{message['sender']}: {message['text']}",
                size_hint_y=None,
                height=dp(50),
                corner_radius=dp(25)
            )
            message_button.bind(on_press=lambda x, m=message: self.show_message_options(m))
            self.messages_layout.add_widget(message_button)

    def go_back(self, instance):
        self.manager.current = 'main'