from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.clock import Clock
from utils.user_data import user_data
from widgets.rounded_button import RoundedButton
from kivy.uix.textinput import TextInput

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Заголовок
        self.layout.add_widget(Label(text="Профиль", font_size=dp(24), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1)))
        
        # ID пользователя
        id_layout = BoxLayout(size_hint_y=None, height=dp(40))
        self.id_label = Label(text=f"ID: {user_data.get_user_id()}", size_hint_x=0.7, color=(1, 1, 1, 1))
        copy_button = RoundedButton(text="Копировать", size_hint_x=0.3, corner_radius=dp(20))
        copy_button.bind(on_press=self.copy_user_id)
        id_layout.add_widget(self.id_label)
        id_layout.add_widget(copy_button)
        self.layout.add_widget(id_layout)
        
        # Индикатор копирования
        self.copy_indicator = Label(text="Скопировано", opacity=0, size_hint_y=None, height=dp(30), color=(0, 1, 0, 1))
        self.layout.add_widget(self.copy_indicator)
        
        # Никнейм
        nickname_layout = BoxLayout(size_hint_y=None, height=dp(40))
        nickname_layout.add_widget(Label(text="Никнейм:", size_hint_x=0.3, color=(1, 1, 1, 1)))
        self.nickname_input = TextInput(
            text=user_data.get_nickname() or "",
            hint_text="Введите никнейм",
            multiline=False,
            size_hint_x=0.7,
            height=dp(40),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[10, 10, 10, 10]
        )
        nickname_layout.add_widget(self.nickname_input)
        self.layout.add_widget(nickname_layout)
        
        # Аватар
        avatar_layout = FloatLayout(size_hint_y=None, height=dp(150))
        self.avatar_image = AsyncImage(source=user_data.get_avatar() or 'path/to/default/avatar.png', 
                                       size_hint=(None, None), size=(dp(120), dp(120)))
        self.avatar_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        avatar_layout.add_widget(self.avatar_image)
        self.layout.add_widget(avatar_layout)
        
        # Кнопка для загрузки аватара
        avatar_button = RoundedButton(text="Загрузить аватар", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        avatar_button.bind(on_press=self.show_file_chooser)
        self.layout.add_widget(avatar_button)
        
        # Индикатор сохранения
        self.save_indicator = Label(text="Сохранено", opacity=0, size_hint_y=None, height=dp(30), color=(0, 1, 0, 1))
        self.layout.add_widget(self.save_indicator)
        
        # Кнопка сохранения
        self.save_button = RoundedButton(text="Сохранить", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        self.save_button.bind(on_press=self.save_profile)
        self.layout.add_widget(self.save_button)
        
        # Кнопка возврата на главный экран
        back_button = RoundedButton(text="Назад", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

        self.original_nickname = ""
        self.original_avatar = ""

    def show_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        content.add_widget(file_chooser)
        
        select_button = RoundedButton(text="Выбрать", size_hint_y=None, height=dp(50), corner_radius=dp(25))
        select_button.bind(on_press=lambda x: self.load_avatar(file_chooser.selection))
        content.add_widget(select_button)
        
        popup = Popup(title="Выберите изображение", content=content, size_hint=(0.9, 0.9))
        select_button.bind(on_press=popup.dismiss)
        popup.open()

    def load_avatar(self, selection):
        if selection:
            avatar_path = selection[0]
            user_data.set_avatar(avatar_path)
            self.avatar_image.source = user_data.get_avatar()
            self.avatar_image.reload()

    def save_profile(self, instance):
        new_nickname = self.nickname_input.text.strip()
        new_avatar = self.avatar_image.source

        changes_made = False

        if new_nickname != self.original_nickname:
            user_data.set_nickname(new_nickname)
            self.original_nickname = new_nickname
            changes_made = True

        if new_avatar != self.original_avatar:
            user_data.set_avatar(new_avatar)
            self.original_avatar = new_avatar
            changes_made = True

        if changes_made:
            self.show_save_indicator()
            print(f"Профиль сохранен: Никнейм - {user_data.get_nickname()}")
        else:
            print("Профиль не изменился, сохранение не требуется")

    def show_save_indicator(self):
        self.save_indicator.opacity = 1
        Animation(opacity=0, duration=1.5).start(self.save_indicator)

    def go_back(self, instance):
        self.manager.current = 'main'

    def copy_user_id(self, instance):
        Clipboard.copy(user_data.get_user_id())
        self.copy_indicator.opacity = 1
        anim = Animation(opacity=0, duration=1)
        anim.start(self.copy_indicator)

    def on_pre_enter(self):
        self.id_label.text = f"ID: {user_data.get_user_id()}"
        self.original_nickname = user_data.get_nickname()
        self.nickname_input.text = self.original_nickname
        self.original_avatar = user_data.get_avatar()
        self.avatar_image.source = self.original_avatar or 'path/to/default/avatar.png'
        self.avatar_image.reload()