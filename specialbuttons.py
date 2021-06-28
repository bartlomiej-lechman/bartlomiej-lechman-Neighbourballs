from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from hoverable import *
from kivy.uix.button import Button
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    toggled = False

    def on_enter(self, *args):

        Window.set_system_cursor('hand')

    def on_leave(self, *args):
        Window.set_system_cursor('arrow')

    def on_release(self):
        Window.set_system_cursor('arrow')

    def toggle_image(self, source):
        self.source = source
        if self.toggled:
            self.toggled = False
        else:
            self.toggled = True


class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_enter(self, *args):
        self.color = (1, 0.7, 0.2, 1)
        Window.set_system_cursor('hand')

    def on_leave(self, *args):
        self.color = (1, 1, 1, 1)
        Window.set_system_cursor('arrow')
        self.sound = SoundLoader.load('sound/effects/button.mp3')

        if self.sound:
            self.sound.play()

    def on_release(self):
        Window.set_system_cursor('arrow')


class RoundedButton(Button, HoverBehavior):
    # btn_color = (0.25, 0.5, 0.5, 1)

    def __init__(self, color_btn=(0.25, 0.5, 0.5, 1), img_source=None, **kwargs):
        super().__init__(**kwargs)
        self.color_btn = color_btn
        with self.canvas:
            Color(rgb=self.color_btn)  # set the colour

            self.rect = RoundedRectangle(source=img_source,
                                         pos=self.pos, size=self.size, radius=[30])

            # Update the canvas as the screen size change
            # if not use this next 5 line the
            # code will run but not cover the full screen
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

            # update function which makes the canvas adjustable.

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, *args):
        Window.set_system_cursor('hand')

    def on_leave(self, *args):
        self.color = (1, 1, 1, 1)
        Window.set_system_cursor('arrow')

    def on_release(self):
        Window.set_system_cursor('arrow')
        # App.get_running_app().change_screen('a1')
