import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from screens.welcome_screen import WelcomeScreen
from screens.main_screen import MainScreen
from screens.profile_screen import ProfileScreen
from screens.chats_list_screen import ChatsListScreen
from screens.search_screen import SearchScreen
from screens.favorites_screen import FavoritesScreen
from screens.chats_screen import ChatsScreen
from kivy.config import Config
from kivy.animation import Animation
from screens.welcome_animation_screen import WelcomeAnimationScreen

# Включаем мультитач для эмуляции наведения мыши
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MessengerApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)  # Полностью черный цвет
        Window.bind(mouse_pos=self.on_mouse_pos)

        self.sm = ScreenManager(transition=FadeTransition(duration=0.15))
        screens = [
            WelcomeAnimationScreen(name='welcome_animation'),
            WelcomeScreen(name='welcome'),
            MainScreen(name='main'),
            ProfileScreen(name='profile'),
            ChatsListScreen(name='chats_list'),  # Убедитесь, что имя 'chats_list'
            SearchScreen(name='search'),
            FavoritesScreen(name='favorites'),
            ChatsScreen(name='chat')
        ]
        for screen in screens:
            self.sm.add_widget(screen)
        self.sm.current = 'welcome_animation'
        return self.sm

    def on_mouse_pos(self, window, pos):
        for widget in window.children[0].walk():
            if hasattr(widget, 'on_hover'):
                widget.on_hover(window, pos)

    def animated_exit(self):
        def fade_out_complete(animation, widget):
            App.get_running_app().stop()
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=fade_out_complete)
        anim.start(self.sm.current_screen)

if __name__ == '__main__':
    MessengerApp().run()