from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.animation import Animation

Builder.load_string('''
<RoundedButton>:
    background_color: 0, 0, 0, 0  # Прозрачный фон
    color: 1, 1, 1, 1  # Белый текст
    canvas.before:
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.corner_radius]
''')

class RoundedButton(Button):
    bg_color = ListProperty([0.2, 0.2, 0.2, 1])  # Темно-серый цвет по умолчанию
    corner_radius = NumericProperty(10)

    def on_press(self):
        self.bg_color = [0.3, 0.3, 0.3, 1]  # Немного светлее при нажатии

    def on_release(self):
        self.bg_color = [0.2, 0.2, 0.2, 1]  # Возвращаемся к исходному цвету

    def on_hover(self, window, pos):
        if self.collide_point(*self.to_widget(*pos)):
            Animation(bg_color=[0.25, 0.25, 0.25, 1], duration=0.1).start(self)
        else:
            Animation(bg_color=[0.2, 0.2, 0.2, 1], duration=0.1).start(self)
