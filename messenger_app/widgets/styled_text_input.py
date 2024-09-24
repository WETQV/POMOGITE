from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

class StyledTextInput(BoxLayout):
    def __init__(self, hint_text='', text='', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(5), dp(5)]
        self.size_hint_y = None
        self.height = dp(40)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Темно-серый фон
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.text_input = TextInput(
            text=text,
            hint_text=hint_text,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1),
            cursor_color=(1, 1, 1, 1),
            multiline=False,
            padding=[dp(10), dp(10), dp(10), dp(10)],
            font_size=dp(16)
        )
        self.add_widget(self.text_input)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    @property
    def text(self):
        return self.text_input.text

    @text.setter
    def text(self, value):
        self.text_input.text = value
