from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from utils.user_data import user_data
from widgets.rounded_button import RoundedButton  # Добавьте этот импорт
from kivy.uix.popup import Popup

class ChatsListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(text="Чаты", font_size=dp(24), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1))
        self.layout.add_widget(title)
        
        self.chats_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        self.layout.add_widget(self.chats_layout)
        
        back_button = RoundedButton(text="Назад", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.update_chats_list()

    def update_chats_list(self):
        self.chats_layout.clear_widgets()
        chats = user_data.get_all_chats()
        for chat_id, chat_data in chats:
            chat_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
            
            chat_button = RoundedButton(
                text=f"Чат с {chat_data.get('nickname', 'Неизвестный')}",
                size_hint_x=0.9,
                corner_radius=dp(25)
            )
            chat_button.bind(on_press=lambda x, cid=chat_id: self.open_chat(cid))
            chat_layout.add_widget(chat_button)
            
            delete_button = RoundedButton(
                text="X",
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                corner_radius=dp(15),
                background_color=(1, 0, 0, 1)
            )
            delete_button.bind(on_press=lambda x, cid=chat_id: self.confirm_delete_chat(cid))
            chat_layout.add_widget(delete_button)
            
            self.chats_layout.add_widget(chat_layout)

    def open_chat(self, chat_id):
        chat_screen = self.manager.get_screen('chat')
        chat_screen.set_chat_id(chat_id)
        self.manager.current = 'chat'

    def confirm_delete_chat(self, chat_id):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text="Вы уверены, что хотите удалить этот чат?"))
        
        buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        yes_button = Button(text="Да")
        no_button = Button(text="Нет")
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(buttons)
        
        popup = Popup(title="Подтверждение", content=content, size_hint=(0.8, 0.4))
        
        yes_button.bind(on_press=lambda x: self.delete_chat(chat_id, popup))
        no_button.bind(on_press=popup.dismiss)
        
        popup.open()

    def delete_chat(self, chat_id, popup):
        if user_data.delete_chat(chat_id):
            popup.dismiss()
            self.update_chats_list()

    def go_back(self, instance):
        self.manager.current = 'main'