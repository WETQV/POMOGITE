from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior

class ClickableFloatLayout(ButtonBehavior, FloatLayout):
    pass

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = ClickableFloatLayout()
        self.layout.bind(on_press=self.skip_animation)

        self.welcome_label = Label(
            text="Добро пожаловать в Messenger",
            font_size=dp(24),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 0)
        )
        self.layout.add_widget(self.welcome_label)

        self.add_widget(self.layout)

    def on_enter(self):
        self.start_animation()

    def start_animation(self):
        anim = Animation(color=(1, 1, 1, 1), duration=2) + Animation(color=(1, 1, 1, 1), duration=1)
        anim.bind(on_complete=self.finish_animation)
        anim.start(self.welcome_label)

    def finish_animation(self, *args):
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 0.5)

    def skip_animation(self, instance):
        Animation.cancel_all(self.welcome_label)
        self.manager.current = 'main'

    def animate_in(self):
        pass

    def animate_out(self):
        pass