from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from utils.user_data import user_data
from widgets.rounded_button import RoundedButton
from kivy.animation import Animation
from kivy.clock import Clock

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        title = Label(text="Поиск собеседника", font_size=dp(24), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1))
        layout.add_widget(title)
        
        self.id_input = TextInput(
            hint_text="Введите ID пользователя",
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[10, 10, 10, 10]
        )
        layout.add_widget(self.id_input)
        
        search_button = RoundedButton(text="Поиск", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        search_button.bind(on_press=self.search_user)
        layout.add_widget(search_button)
        
        self.result_label = Label(text="", color=(1, 1, 1, 1), font_size=dp(36), opacity=0)
        layout.add_widget(self.result_label)
        
        self.add_contact_button = RoundedButton(text="Добавить контакт", size_hint_y=None, height=dp(50), corner_radius=dp(25), opacity=0)
        self.add_contact_button.bind(on_press=self.add_contact)
        layout.add_widget(self.add_contact_button)
        
        back_button = RoundedButton(text="Назад", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def search_user(self, instance):
        user_id = self.id_input.text.strip()
        if user_id:
            if user_id == user_data.get_user_id():
                self.show_nyashka_animation()
            else:
                user = user_data.search_user(user_id)
                if user:
                    self.show_result_animation(f"Найден пользователь: {user['nickname']}")
                    self.show_add_contact_button()
                else:
                    self.show_result_animation("Пользователь не найден", fade_out=True)
                    self.hide_add_contact_button()
        else:
            self.show_result_animation("Введите ID пользователя", fade_out=True)
            self.hide_add_contact_button()

    def show_nyashka_animation(self):
        self.result_label.text = "Ты Няшка!"
        anim = Animation(opacity=1, duration=0.5) + Animation(opacity=1, duration=1) + Animation(opacity=0, duration=0.5)
        anim.start(self.result_label)
        self.hide_add_contact_button()

    def show_result_animation(self, text, fade_out=False):
        self.result_label.text = text
        anim = Animation(opacity=1, duration=0.5)
        if fade_out:
            anim += Animation(opacity=1, duration=2) + Animation(opacity=0, duration=0.5)
        anim.start(self.result_label)

    def show_add_contact_button(self):
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.add_contact_button)

    def hide_add_contact_button(self):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.add_contact_button)

    def add_contact(self, instance):
        user_id = self.id_input.text.strip()
        if user_data.add_contact(user_id):
            self.show_result_animation("Контакт успешно добавлен", fade_out=True)
            self.hide_add_contact_button()
        else:
            self.show_result_animation("Не удалось добавить контакт", fade_out=True)

    def go_back(self, instance):
        self.manager.current = 'main'

    def on_enter(self):
        # Сбрасываем состояние экрана при входе на него
        self.id_input.text = ""
        self.result_label.opacity = 0
        self.add_contact_button.opacity = 0

    def on_leave(self):
        # Сбрасываем состояние экрана при уходе с него
        self.id_input.text = ""
        self.result_label.opacity = 0
        self.add_contact_button.opacity = 0