# -*- coding: utf-8 -*-
import colorsys
from threading import Thread
from PIL import Image as Im
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from datetime import datetime
from popuptype import PopupType
from tasktype import *
from flashcards import *
from mandelbrot import *
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from specialbuttons import HoverButton, ImageButton
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from multiprocessing.pool import ThreadPool

Window.fullscreen = 'auto'


class CustomBoxLayout(BoxLayout):
    pass


class PopupLayout(BoxLayout):
    pass


class ChooseLevelScreen2(Screen):
    pass


class SettingsScreen(Screen):
    pass


class ChooseTaskScreen(Screen):
    pass


class FractalScreen(Screen):
    time = datetime.now()

    frameTime = 1

    def __init__(self, w=1080, h=800, **kw):
        super(FractalScreen, self).__init__(**kw)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.w = w
        self.h = h
        self.max_iterations = 100
        self.a = complex(-2.0, -1.0)
        self.b = complex(1.0, 1.0)
        self.zoom = 0.5
        Clock.schedule_interval(self.update_pic, .5)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'r':
            self.reset()
        if keycode[1] == 'e':
            App.get_running_app().change_screen('achievement_screen')

    def on_touch_down(self, touch):
        self.zoom_in(touch)

    def zoom_in(self, touch):
        x1 = touch.pos[0] - 450
        y1 = touch.pos[1] + 160
        x2 = x1 + 1080 * self.zoom
        y2 = y1 - 785 * self.zoom
        ax = ((self.b.real - self.a.real) / self.w) * x1 + self.a.real
        ay = ((self.b.imag - self.a.imag) / self.h) * y1 + self.a.imag
        bx = ((self.b.real - self.a.real) / self.w) * x2 + self.a.real
        by = ((self.b.imag - self.a.imag) / self.h) * y2 + self.a.imag
        self.a, self.b = complex(ax, ay), complex(bx, by)
        self.draw_fractal()
        self.zoom /= pow(1.001, 1.01)

    def reset(self):
        self.zoom = 0.5
        self.a = complex(-2.0, -1.0)
        self.b = complex(1.0, 1.0)
        self.draw_fractal()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update_pic(self, dt):
        self.fractal.reload()

    def on_pre_enter(self, *args):
        self.zoom = 0.5
        self.a = complex(-2.0, -1.0)
        self.b = complex(1.0, 1.0)
        self.draw_fractal()

    def draw_fractal(self):
        result = np.zeros((self.h, self.w, 3))

        pool = ThreadPool(processes=4)
        iy = np.arange(self.h)

        test = pool.map_async(get_col, zip(iy, repeat(self.w), repeat(self.h), repeat(self.a), repeat(self.b),
                                        repeat(self.max_iterations))).get()
        for i in np.arange(self.h):
            result[i, :] = test[i]

        mandelbrot = result
        mandelbrot = Im.fromarray(mandelbrot.astype(np.uint8))

        mandelbrot.save(f'fractal.png')
        self.fractal.source = 'fractal.png'


class Achievement(ImageButton):
    def __init__(self, title=None, source=None, **kwargs):
        super(Achievement, self).__init__(**kwargs)
        self.title = title
        self.source = source

    def on_press(self):
        App.get_running_app().change_screen(self.title + '_screen')


class AchievementScreen(Screen):
    def on_pre_enter(self, *args):
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.set_achievements()

    def set_achievements(self):
        store = JsonStore('json/a1/achievements.json')
        for i in store.keys():
            if store[i]['open']:
                self.grid.add_widget(Achievement(title=i, source=store[i]['img']))


class Vocabulary(BoxLayout):
    def set_content(self, content):
        text = ''
        f = open(content, "r", encoding="utf-8")
        for x in f:
            text += x

        self.text.text = text


class Task(ImageButton):
    def __init__(self, status=None, typ=None, category=None, number=None, level=None, task_panel=None,
                 task_content=None,
                 **kwargs):
        super(Task, self).__init__(**kwargs)

        self.typ = typ
        self.task_content = task_content
        self.level = level
        self.status = status
        self.category = category
        self.number = number
        self.task_type = TaskType(
            JsonStore('json/' + App.get_running_app().lang + '/' + self.level + '/' + self.category + '_' + str(
                self.number) + '.json'))
        self.source = 'images/' + 'zad_' + self.category + '/' + 'zad_' + self.category + '_' + self.status + str(
            self.number) + '.png'
        self.task_panel = task_panel

    def on_press(self):
        self.task_type = TaskType(
            JsonStore('json/' + App.get_running_app().lang + '/' + self.level + '/' + self.category + '_' + str(
                self.number) + '.json'))
        App.get_running_app().add_task(task=self, typ=self.task_type.create(self.typ))

    def change_task_status(self, status):
        self.lang = App.get_running_app().lang
        store = JsonStore('json/' + self.lang + '/' + self.level + '.json')
        achiev_store = JsonStore('json/' + self.level + '/achievements.json')
        time = datetime.now()
        if status == -1:
            store[self.task_panel.topic][self.category][str(self.number)]['treal'] = -1
            store[self.task_panel.topic] = store[self.task_panel.topic]
            App.get_running_app().update_cards(level=self.level, number=str(self.number), topic=self.task_panel.topic)
            if store[self.task_panel.topic][self.category][str(self.number)]['achiev']:
                title = store[self.task_panel.topic][self.category][str(self.number)]['achiev']
                achiev_store[title]['open'] = 1
                achiev_store[title] = achiev_store[title]
            self.disabled = True
        elif status == 1:
            treal = store[self.task_panel.topic][self.category][str(self.number)]['treal']
            if treal == 2:
                App.get_running_app().block_tasks[self.level] = {"topic": self.task_panel.topic,
                                                                 self.category: {str(self.number): {
                                                                     "time": {"year": time.year, "month": time.month,
                                                                              "day": time.day, "hour": time.hour,
                                                                              "min": time.minute}}}}
            store[self.task_panel.topic][self.category][str(self.number)]['treal'] = treal + 1
            store[self.task_panel.topic] = store[self.task_panel.topic]
        else:
            store[self.task_panel.topic][self.category][str(self.number)]['treal'] = 0
            store[self.task_panel.topic] = store[self.task_panel.topic]



class TaskScreen(Screen):
    def __init__(self, typ=None, task=None, name=None, **kw):
        super().__init__(**kw)
        self.task = task
        self.store = App.get_running_app().STORE
        self.typ = typ
        self.content = self.typ.content
        self.name = name
        Clock.schedule_interval(self.update, .5)

    def update(self, *args):
        self.task_l.text = App.get_running_app().STORE.get('taskscreen')['task'] + " " + str(self.task.number)

        self.content = JsonStore(
            'json/' + App.get_running_app().lang + '/' + self.task.level + '/' + self.task.category + '_' + str(
                self.task.number) + '.json')
        self.typ.update(self.content)

    def on_enter(self, *args):

        self.typ.repeat()
        for child in [child for child in self.layout.children]:
            if isinstance(child, GridLayout):
                self.layout.remove_widget(child)
        self.title.text = self.content.get('title')['name']
        self.grid = self.typ.layout
        self.layout.add_widget(self.grid)

    def check_answers(self):
        self.store = App.get_running_app().STORE
        bad = self.typ.check()
        self.task.change_task_status(status=1) if bad else self.task.change_task_status(status=-1)
        self.popup = Popup(title='', size_hint=(None, None),
                           size=(600, 600))
        store = JsonStore(
            'json/' + App.get_running_app().lang + '/' + self.task.level + '.json')
        print(store)
        # print(store['gram'][str(self.task.number)]['treal'])
        treal = store['P']['gram'][str(self.task.number)]['treal']

        if bad:
            self.popup.content = PopupType().create(popup=self.popup, msg='incorrect', content=self.store,
                                                    treal=str(treal) + '/3')
        else:
            self.popup.content = PopupType().create(msg='correct', popup=self.popup, content=self.store)

        Clock.schedule_once(self.popup.open, 1.5)



class TasksPanelScreen(Screen):

    def __init__(self, store_name=None, topic=None, **kw):
        super(TasksPanelScreen, self).__init__(**kw)
        self.lang = App.get_running_app().lang
        self.store_name = store_name
        self.store = JsonStore('json/' + self.lang + '/' + self.store_name + '.json')
        self.topic = topic
        Clock.schedule_interval(self.update, .5)

    def on_pre_enter(self, *args):
        self.lang = App.get_running_app().lang
        self.store = JsonStore('json/' + self.lang + '/' + self.store_name + '.json')
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.set_tasks('gram')
        self.set_tasks('czyt')
        self.set_tasks('sluch')

    def show_info(self):
        lang = App.get_running_app().lang
        self.info = Popup(title='', content=InfoPopup(img='images/' + lang + '_taskspanel_popup.png'),
                          size_hint=(None, None), size=(Window.width - 600, Window.height - 150))
        self.info.open()

    def update(self, *args):
        self.lang = App.get_running_app().lang

        self.store = JsonStore('json/' + self.lang + '/' + self.store_name + '.json')
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.set_tasks('gram')
        self.set_tasks('czyt')
        self.set_tasks('sluch')
        self.flag.source = App.get_running_app().STORE.get('flag')['source']

    def show_book(self):
        book_content = 'json/' + self.store_name + '/' + self.topic + '.txt'
        layout_popup = Vocabulary(orientation='vertical', size_hint_y=None)
        layout_popup.bind(minimum_height=layout_popup.setter('height'))
        layout_popup.set_content(book_content)

        root = ScrollView(size_hint=(1, None), size=(Window.width - 100, Window.height - 100))
        root.add_widget(layout_popup)
        popup = Popup(title='', content=root, size_hint=(None, 1), size=(Window.width - 500, Window.height - 100))
        popup.open()

    def set_tasks(self, category):

        disabled_bool = False
        for i in range(1, 6):
            task = self.store.get(self.topic)[category][str(i)]
            if 3 > task['treal'] >= 0:
                status = 'new'
                disabled_bool = False
            elif task['treal'] == 3:
                status = 'block'
                disabled_bool = True

            elif task['treal'] < 0:
                status = 'done'
                disabled_bool = True
            else:
                status = 'block'
            self.grid.add_widget(
                Task(task_panel=self, status=status, category=category, number=i, level=self.store_name,
                     task_content=task['source'], typ=task['type'], disabled=disabled_bool, name=category + str(i),
                     id=category + str(i)))


class FactButton(HoverButton):
    def __init__(self, description=None, label=None, fact_content=None, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        self.description = description
        self.description.color = (0.97, 0.6, 0.25, 1)
        self.description.italic = True
        self.label = label
        self.background_color = (0.25, 0.5, 0.5, 1)
        self.background_normal = '1,1,1,1'
        self.fact_content = JsonStore(fact_content)
        self.popup = Popup(title='', size_hint=(1, 1))

    def on_press(self):
        self.background_normal = '0.5,1,1,1'

    def on_release(self):
        self.background_normal = '1,1,1,1'
        layout_popup = FactLayout(fact=self, padding=(100, 5), spacing=70, size_hint_y=None, content=self.fact_content)
        layout_popup.bind(minimum_height=layout_popup.setter('height'))
        layout_popup.set_content()
        root = ScrollView(size_hint=(1, None), size=(Window.width - 10, Window.height - 50))
        root.add_widget(layout_popup)
        self.popup.content = root
        self.popup.open()

    def on_enter(self, *args):
        Window.set_system_cursor('hand')
        self.description.text = self.label

    def on_leave(self, *args):
        Window.set_system_cursor('arrow')
        self.description.text = ''


class FactsScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.update, .5)
        Clock.schedule_interval(self.on_enter, .5)

    def on_enter(self, *args):
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)
        self.articles = JsonStore('json/' + App.get_running_app().lang + '/facts.json')
        items = self.articles.count()
        for i in range(1, items + 1):
            article = self.articles[str(i)]
            self.grid.add_widget(
                Label(text=article['level'], height=50, size_hint_y=None, size_hint_x=.3, font_size='23sp', bold=True,
                      color=(0.2, 0.3, 0.43, 1)))
            self.grid.add_widget(
                FactButton(text=article['head'], label=article['description'], description=self.description_l,
                           height=50, size_hint_y=None, fact_content=article['source']))
        for j in range(3, 15):
            self.grid.add_widget(
                Label(text='level', height=50, size_hint_y=None, font_size='23sp', bold=True, color=(0.2, 0.3, 0.43, 1),
                      size_hint_x=.3))
            self.grid.add_widget(Button(text='Article ' + str(j) + '(to do)', height=50, size_hint_y=None))

    def on_pre_enter(self, *args):
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)

    def update(self, *args):
        self.articles = JsonStore('json/' + App.get_running_app().lang + '/facts.json')
        self.store = App.get_running_app().STORE
        self.flag.source = self.store.get('flag')['source']


class FactLayout(StackLayout):

    def __init__(self, content=None, fact=None, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.fact = fact

    def set_content(self):
        self.add_widget(
            Label(text=self.content['main_header']['text'], size_hint_x=0.95, size_hint_y=None, font_size='30sp',
                  bold=True, color=(0.99, 0.98, 0.7, 1)))
        btn_exit = ImageButton(size_hint_y=None, size_hint_x=0.05, source='images/exit_btn.png')
        btn_exit.bind(on_press=self.fact.popup.dismiss)
        self.add_widget(btn_exit)
        if self.content.exists('images'):

            self.add_widget(Image(size_hint_y=.18, size_hint_x=0.35, source=self.content['images']['img_1']))
            self.add_widget(Label(text=self.content['p']['p_1'], size_hint_x=0.65, size_hint_y=.2, font_size='18sp',
                                  color=(0.1, 0.1, 0.1, 1)))
            self.add_widget(
                Label(text=self.content['p']['p_2'], size_hint_x=1, text_size=(1200, None), size_hint_y=None,
                      font_size='18sp',
                      color=(0.1, 0.1, 0.1, 1)))
            self.add_widget(
                Label(text=self.content['p']['p_3'], text_size=(600, None), size_hint_x=.6, size_hint_y=.25,
                      font_size='18sp',
                      color=(0.1, 0.1, 0.1, 1)))
            self.add_widget(Image(size_hint_y=.3, size_hint_x=.4, source=self.content['images']['img_2']))

            self.add_widget(Image(size_hint_y=.2, size_hint_x=.5, source=self.content['images']['img_3']))
            self.add_widget(
                Label(text=self.content['p']['p_4'], size_hint_x=.5, size_hint_y=.2, font_size='18sp',
                      text_size=(600, None),
                      color=(0.1, 0.1, 0.1, 1)))
        else:
            self.spacing = 100
            p = self.content['p']
            i = 1
            for item in p:
                self.add_widget(
                    Label(text=p['p_' + str(i)], text_size=(600, None), size_hint_x=1, size_hint_y=None,
                          font_size='18sp',
                          color=(0.1, 0.1, 0.1, 1)))
                i += 1


class HomeScreen(Screen):

    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        self.store = JsonStore('json/pl.json')
        self.study_l = self.store.get('homescreen')['study']
        self.exit_l = self.store.get('homescreen')['exit']
        self.settings_l = self.store.get('homescreen')['parameters']
        self.credits_l = 'Credits'
        Clock.schedule_interval(self.update, .5)

    def update(self, *args):
        self.store = App.get_running_app().STORE
        self.nauka.text = self.store.get('homescreen')['study']
        self.wyjscie.text = self.store.get('homescreen')['exit']
        self.ustawienia.text = self.store.get('homescreen')['parameters']
        self.flag.source = self.store.get('flag')['source']


class ChooseLevelScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.update, .5)

    def update(self, *args):
        self.flag.source = App.get_running_app().STORE.get('flag')['source']


class InfoPopup(FloatLayout):
    image = StringProperty('')

    def __init__(self, img, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.image = img

    def set_img(self, dt):
        self.ids.info.source = self.img


class FlashcardStartScreen(Screen):
    number_of_words = JsonStore('json/pl/cards.json').count()

    def __init__(self, **kw):
        super(FlashcardStartScreen, self).__init__(**kw)
        Clock.schedule_interval(self.update, .5)

    def popupcontent(self):
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Button())

        return self.layout

    def update(self, *args):
        self.flag.source = App.get_running_app().STORE.get('flag')['source']
        self.app = App.get_running_app()
        self.number_of_words = self.app.cards.count()

    def show_info(self):
        lang = App.get_running_app().lang
        self.info = Popup(title='', content=InfoPopup(img='images/' + lang + '_odpytywanie_popup.png'),
                          size_hint=(None, None), size=(Window.width - 600, Window.height - 150))
        self.info.open()

    def start(self):

        layout = CustomBoxLayout()
        layout.baza_slow.text = str(self.number_of_words) + '/50'
        layout.label_1.text = 'ZBYT MAŁA IŁOŚĆ SŁÓWEK!'
        layout.label_1.font_size = '30sp'
        layout.label_1.bold = True
        layout.label_1.color = (1, 0.7, 0.2, 1)
        layout.label_2.text = 'WYKONAJ JESZCZE KILKA ZADAŃ ABY ODBLOKOWAĆ TĄ AKTYWNOŚĆ'
        if self.number_of_words < 17:
            self.popup = Popup(title='', content=layout, size_hint=(None, None), size=(600, 300))
            self.popup.open()
        else:
            self.app.change_screen('flashcard_screen')


class FlashcardScreen(Screen):
    curr_card = None

    def __init__(self, **kw):
        super(FlashcardScreen, self).__init__(**kw)
        self.baza = JsonStore('json/pl/cards.json')

    def updatecard(self, *args):
        self.baza = App.get_running_app().cards
        self.answer.text = 'Sprawdż słówko'
        self.curr_card = getrandomcard(self.baza)
        self.question.text = getquestion(self.curr_card)

    def on_pre_enter(self, *args):
        self.updatecard()

    def updateAnsLabel(self, *args):
        self.answer.text = getanswer(self.curr_card)

    def dismiss_popup(self): pass

    def show_info(self):
        lang = App.get_running_app().lang
        self.info = Popup(title='', content=InfoPopup(img='images/' + lang + '_odpytywanie_popup.png'),
                          size_hint=(None, None), size=(Window.width - 600, Window.height - 150))
        self.info.open()


class StudyScreen(Screen):

    def __init__(self, **kw):
        super(StudyScreen, self).__init__(**kw)
        self.store = JsonStore('json/pl.json')
        self.tasks_l = self.store.get('studyscreen')['tasks']
        self.flashcards_l = self.store.get('studyscreen')['flashcards']
        self.interesting_l = self.store.get('studyscreen')['interesting']
        self.achievements_l = self.store.get('studyscreen')['achievements']
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.store = App.get_running_app().STORE
        self.tasks.text = self.store.get('studyscreen')['tasks']
        self.flashcards.text = self.store.get('studyscreen')['flashcards']
        self.interesting.text = self.store.get('studyscreen')['interesting']
        self.achievements.text = self.store.get('studyscreen')['achievements']
        self.flag.source = self.store.get('flag')['source']


with open('kivy/main.kv', encoding='utf8') as f:
    GUI = Builder.load_string(f.read())





class MainApp(App):
    pl = BooleanProperty(True)
    STORE = JsonStore('json/pl.json')
    cards = JsonStore('json/pl/cards.json')
    sound = SoundLoader.load('sound/music/arthur-vyncke_until-we-meet-again.mp3')
    sound.loop = True
    if sound:
        sound.play()

    def __init__(self, **kwargs):
        super(MainApp, self).__init__()
        self.flag = 'images/Group 34.png'
        self.lang = 'pl'

    def on_start(self):
        pass

    def build(self):
        Clock.schedule_interval(self.update_block, 1)

        return GUI

    def get_flag(self):
        return self.flag

    def change_screen(self, screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name

    def add_task(self, task, typ):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.add_widget(TaskScreen(task=task, typ=typ, name='zadanie' + str(task.number)))
        screen_manager.current = 'zadanie' + str(task.number)

    def set_store(self, boolean):

        self.pl = boolean
        if self.pl:
            self.STORE = JsonStore('json/pl.json')
            self.lang = 'pl'
            self.cards = JsonStore('json/pl/cards.json')
            self.flag = 'images/Group 34.png'

        else:
            self.STORE = JsonStore('json/ukr.json')
            self.cards = JsonStore('json/ukr/cards.json')
            self.lang = 'ukr'
            self.flag = 'images/pl_flag.png'

    def update_block(self, *args):
        block_tasks = JsonStore('json/' + self.lang + '/block_tasks.json')
        topics = ['P']
        category = ['gram', 'czyt', 'sluch']
        now = datetime.now()
        keys = block_tasks.keys()
        for i in keys:
            task = block_tasks[i]
            for topic in topics:
                if task['topic'] == topic:
                    for categ in category:
                        if categ in task:
                            keys2 = task[categ].keys()
                            for j in keys2:
                                year = task[categ][j]['time']['year']
                                month = task[categ][j]['time']['month']
                                day = task[categ][j]['time']['day']
                                hour = task[categ][j]['time']['hour']
                                min = task[categ][j]['time']['min']
                                time2 = datetime(year=year, day=day, month=month, hour=hour, minute=min)
                                if (now - time2).total_seconds() >= 3600:
                                    store = JsonStore('json/' + self.lang + '/' + i + '.json')
                                    store[topic][categ][j]['treal'] = 0
                                    store[topic] = store[topic]
                                    block_tasks.delete(i)

    def update_cards(self, level=None, topic=None, number=None):
        words = JsonStore('json/' + self.lang + '/' + level + '/' + topic + number + '.json')
        self.cards = JsonStore('json/' + self.lang + '/cards.json')
        quantity = self.cards.count()
        j = 1
        for i in range(quantity, quantity + words.count() - 1):
            word = words[str(number) + '_' + str(j)]
            addCard(self.cards, question=word['question'], answer=word['answer'], category=words['category'], number=i)
            j += 1

    def set_level(self):
        screen_manager = self.root.ids["screen_manager"]
        level_a1 = TasksPanelScreen(name='a1', id='a1', store_name='a1', topic='P')
        screen_manager.add_widget(level_a1)


MainApp().run()
