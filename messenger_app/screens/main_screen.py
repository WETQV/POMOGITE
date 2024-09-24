from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.app import App
from widgets.rounded_button import RoundedButton

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(text="Главное меню", font_size=dp(24), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1))
        self.layout.add_widget(title)
        
        scroll_view = ScrollView(size_hint=(1, 1))
        buttons_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        buttons = [
            ("Профиль", 'profile'),
            ("Чаты", 'chats'),
            ("Поиск", 'search'),
            ("Избранное", 'favorites'),
            ("Выход", 'exit')
        ]
        
        for button_text, screen_name in buttons:
            button = RoundedButton(
                text=button_text, 
                size_hint_y=None, 
                height=dp(50),
                corner_radius=dp(25)
            )
            button.bind(on_release=lambda btn, s=screen_name: self.change_screen(s))
            buttons_layout.add_widget(button)
        
        scroll_view.add_widget(buttons_layout)
        self.layout.add_widget(scroll_view)
        
        self.add_widget(self.layout)

    def change_screen(self, screen):
        if screen == 'chats':
            self.manager.current = 'chats_list'
        elif screen == 'exit':
            App.get_running_app().stop()
        else:
            self.manager.current = screen

    def on_enter(self):
        self.opacity = 0
        self.layout.opacity = 1
        self.opacity = 1