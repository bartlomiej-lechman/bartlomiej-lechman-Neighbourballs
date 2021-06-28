from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from specialbuttons import RoundedButton


class CanvasBoxLayout(BoxLayout):
    pass


class PopGridLayout(GridLayout):
    pass


class PopupType:

    def __init__(self):
        self.layout = CanvasBoxLayout(orientation='vertical')

    def create(self, msg=None, popup=None, content=None, treal=''):
        self.content = content
        self.msg = msg
        self.popup = popup
        self.treal =treal
        popup_type = 'type_' + msg
        popup_method = getattr(self, popup_type)
        return popup_method()

    def type_correct(self):
        image = 'images/correct.png'
        self.set_content(image=image, label=self.content['popup']['correct']['label'],
                         btn_next=self.content['popup']['correct']['btn_next'], btn_return=self.content['popup']['correct']['btn_return'])

        return self.layout

    def set_content(self, image, label, btn_next,
                    btn_return):
        grid = PopGridLayout(cols=2, size_hint=(.7, .7), pos_hint={'center_x': 0.5, 'center_y': 0})
        grid.spacing = 20
        grid.padding = 40
        btn_return = RoundedButton(color_btn=(1, 1, 1, 1), img_source=btn_return, on_press=lambda a:App.get_running_app().change_screen('a1'), on_release=self.popup.dismiss)
        btn_next = RoundedButton(color_btn=(1, 1, 1, 1), img_source=btn_next)
        grid.add_widget(btn_return)
        grid.add_widget(btn_next)

        self.layout.add_widget(
            Label(text=label, size_hint=(.5, .5), pos_hint={'center_x': 0.5, 'center_y': 1}))
        self.layout.add_widget(Image(source=image))
        self.layout.add_widget(grid)

    def type_incorrect(self):
        image = 'images/incorrect.png'
        self.set_content(image=image, label=self.content['popup']['incorrect']['label']+'\n         ('+self.treal+')',
                         btn_next=self.content['popup']['incorrect']['btn_next'],
                         btn_return=self.content['popup']['incorrect']['btn_return'])
        return self.layout