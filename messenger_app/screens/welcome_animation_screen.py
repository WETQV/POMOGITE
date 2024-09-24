from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.graphics import Color, Rectangle
from random import random, choice, uniform
import string

class AnimatedLabel(Label):
    velocity = ListProperty([0, 0])
    rotation = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = self.get_muted_color()

    def get_muted_color(self):
        return [uniform(0.2, 0.6), uniform(0.2, 0.6), uniform(0.2, 0.6), 1]

class Word(Label):
    target_text = StringProperty('')
    shake_amount = NumericProperty(0)
    animation_progress = NumericProperty(0)
    is_forming = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = self.get_muted_color()
        self.original_pos = self.pos
        self.bind(shake_amount=self.update_shake)
        self.bind(animation_progress=self.update_text)

    def get_muted_color(self):
        return [uniform(0.4, 0.8), uniform(0.4, 0.8), uniform(0.4, 0.8), 1]

    def update_shake(self, instance, value):
        shake_x = (random() - 0.5) * 2 * value
        shake_y = (random() - 0.5) * 2 * value
        self.pos = (self.original_pos[0] + shake_x, self.original_pos[1] + shake_y)

    def update_text(self, instance, value):
        if self.is_forming:
            self.text = self.target_text[:int(len(self.target_text) * value)]
        else:
            visible_chars = int(len(self.text) * (1 - value))
            self.text = self.text[:visible_chars]

class WelcomeAnimationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = FloatLayout()
        self.add_widget(self.background)
        
        self.foreground = RelativeLayout()
        self.add_widget(self.foreground)
        
        self.letters = []
        self.words = []
        self.animation_stage = 0
        self.wakoo_letters = []
        self.word_list = ["BRAIN", "HEART", "LUNGS", "LIVER", "KIDNEY", "SPLEEN", "THYMUS", "MARROW", "CORTEX", "NEURON"]
        self.overlay = None
        Clock.schedule_once(self.start_animation, 0.5)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.skip_animation()
            return True
        return super().on_touch_down(touch)

    def skip_animation(self):
        # Остановить все текущие анимации
        Clock.unschedule(self.add_letter)
        Clock.unschedule(self.start_forming_words)
        Clock.unschedule(self.start_shaking_words)
        Clock.unschedule(self.fade_to_black)
        Clock.unschedule(self.show_wakoo)
        Clock.unschedule(self.fade_out)

        # Очистить все элементы
        self.background.clear_widgets()
        self.foreground.clear_widgets()
        self.letters.clear()
        self.words.clear()
        self.wakoo_letters.clear()

        # Сразу перейти к главному меню
        self.manager.current = 'main'

    def start_animation(self, dt):
        Clock.schedule_interval(self.add_letter, 0.02)
        Clock.schedule_once(self.start_forming_words, 3)
        Clock.schedule_once(self.start_shaking_words, 7)

    def add_letter(self, dt):
        letter = choice(string.ascii_uppercase)
        label = AnimatedLabel(text=letter, font_size='20sp', size_hint=(None, None))
        label.pos = (random() * self.width, random() * self.height)
        label.velocity = [uniform(-4, 8), uniform(-4, 8)]
        self.background.add_widget(label)
        self.letters.append(label)
        Animation(opacity=1, duration=0.1).start(label)
        Animation(rotation=720, duration=0.5).repeat = True
        Animation(rotation=360, duration=1).start(label)

    def update_letter_position(self, dt):
        for letter in self.letters:
            letter.pos[0] += letter.velocity[0]
            letter.pos[1] += letter.velocity[1]
            if letter.right > self.width or letter.x < 0:
                letter.velocity[0] *= -1
            if letter.top > self.height or letter.y < 0:
                letter.velocity[1] *= -1

    def start_forming_words(self, dt):
        self.animation_stage = 1
        Clock.schedule_interval(self.form_word, 0.5)

    def form_word(self, dt):
        if not self.word_list:
            return False
        word_text = self.word_list.pop(0)
        word = Word(text='', target_text=word_text, font_size='30sp', size_hint=(None, None))
        word.pos = (random() * (self.width - word.width), random() * (self.height - word.height))
        self.background.add_widget(word)
        self.words.append(word)
        word.is_forming = True
        Animation(animation_progress=1, duration=0.3).start(word)
        return True

    def start_shaking_words(self, dt):
        self.animation_stage = 3
        for word in self.words:
            Animation(shake_amount=15, duration=0.3).start(word)
        Clock.schedule_once(self.fade_to_black, 1)

    def fade_to_black(self, dt):
        self.overlay = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            self.overlay_color = Color(0, 0, 0, 0)
            self.overlay = Rectangle(size=self.size, pos=self.pos)
        anim = Animation(a=1, duration=0.5)
        anim.bind(on_complete=self.transform_to_wakoo)
        anim.start(self.overlay_color)

    def transform_to_wakoo(self, *args):
        self.animation_stage = 4
        target_text = "WAKOO"
        for i, letter in enumerate(target_text):
            label = Label(text=letter, font_size='100sp', color=[1, 1, 1, 0], size_hint=(None, None), bold=True)
            label.pos_hint = {'center_x': 0.5 + (i - 2) * 0.1, 'center_y': 0.5}
            self.foreground.add_widget(label)
            self.wakoo_letters.append(label)
        for word in self.words:
            self.background.remove_widget(word)
        self.words.clear()
        for letter in self.letters:
            self.background.remove_widget(letter)
        self.letters.clear()
        Clock.schedule_once(self.show_wakoo, 0.3)

    def show_wakoo(self, dt):
        Animation(a=0, duration=0.5).start(self.overlay_color)
        for letter in self.wakoo_letters:
            Animation(color=[1, 1, 1, 1], duration=1).start(letter)
        Clock.schedule_once(self.fade_out, 3)

    def fade_out(self, dt):
        for letter in self.wakoo_letters:
            Animation(color=[1, 1, 1, 0], duration=1).start(letter)
        anim = Animation(a=1, duration=1)
        anim.bind(on_complete=self.switch_to_main_menu)
        anim.start(self.overlay_color)

    def switch_to_main_menu(self, *args):
        self.manager.current = 'main'

    def on_enter(self):
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Черный фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        Clock.schedule_interval(self.update_letter_position, 1/60)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        if self.overlay:
            self.overlay.pos = instance.pos
            self.overlay.size = instance.size
