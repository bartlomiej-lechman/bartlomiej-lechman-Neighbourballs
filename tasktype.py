from kivy.clock import Clock
from kivy.uix.behaviors import focus
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


class TaskType:

    def __init__(self, content=None):
        self.grid = GridLayout(cols=2)
        self.grid.pos_hint = {"center_x": 0.4, "y": 0.25}
        self.grid.size_hint = (.55, .55)
        self.inputs = []
        self.content = content

    def create(self, typ=None):
        self.typ = typ
        task_type = 'type_' + str(typ)
        task_method = getattr(self, task_type)
        return task_method()

    def repeat(self):
        return self.create(self.typ)

    def update(self, content):
        self.content = content

    def check(self):
        check_type = 'check_' + str(self.typ)
        check_method = getattr(self, check_type)
        return check_method()

    def type_1(self):
        self.inputs = []
        self.clear_canvas()
        self.items = self.content.count()
        self.set_grid()
        return self

    def type_2(self):
        self.inputs = []
        # self.grid = GridLayout(cols=2)
        # self.grid.pos_hint = {"center_x": 0.4, "y": 0.25}
        # self.grid.size_hint = (.55, .55)
        self.clear_canvas()
        self.items = self.content.count() - 1
        self.grid.add_widget(Label(text=self.content['example']['string'], color=(1, 0, 1, 1)))
        self.grid.add_widget(
            TextInput(text=self.content['example']['klucz'], disabled=True, size_hint=(.5, None), height=50))
        self.set_grid()
        return self

    def type_3(self):
        self.inputs = []
        self.clear_canvas()
        self.items = self.content.count() - 2
        self.grid = StackLayout(orientation='lr-tb')
        self.grid.pos_hint = {"center_x": .52, "y": 0}
        self.grid.padding = 260

        # self.grid.cols = 3
        # self.grid.padding =100
        # self.grid.pos_hint = {"center_x": 0.5, "y": 0.25}
        self.grid.add_widget(Label(text="Example:", color=(0, 0, 0, 1), size_hint=(.15, 0.08), width=len('Example: ')))
        for k in range(1, 3):
            self.grid.add_widget(Label(text=self.content.get('example')['string' + str(k)], color=(0, 0, 0, 1),
                                       size_hint=(len(self.content.get('example')['string' + str(k)]) / 100, 0.08),
                                       width=len(self.content.get('example')['string' + str(k)])))
            self.grid.add_widget(TextInput(text=self.content.get('example')['mixed' + str(k)],
                                           size_hint=(len(self.content.get('example')['mixed' + str(k)]) / 100, 0.08),
                                           width=len(self.content.get('example')['mixed' + str(k)])))
        self.grid.add_widget(Label(text=self.content.get('example')['string3'], color=(0, 0, 0, 1),
                                   size_hint=(len(self.content.get('example')['string3']) / 100, 0.08),
                                   width=len(self.content.get('example')['string3'])))
        answer = "Answer: " + self.content.get('example')['string1'] + self.content.get('example')['klucz1'] + \
                 self.content.get('example')['string2'] + self.content.get('example')['klucz2'] + \
                 self.content.get('example')['string3']
        self.grid.add_widget(Label(text=answer, color=(0, 0, 0, 1), size_hint=(.6, 0.08), width=len(answer)))
        self.grid.add_widget(Label(text='', size_hint=(1, 0.08)))
        self.grid.add_widget(Label(text='', size_hint=(1, 0.08)))
        for i in range(1, self.items - 1):  # 1..8
            number = self.content.get(str(i))['quantity']
            inp = TextInput(text=self.content.get(str(i))['mixed1'],
                            size_hint=(len(self.content.get(str(i))['mixed1']) / 100, 0.08),
                            width=len(self.content.get(str(i))['mixed1']))
            for j in range(1, int(number) + 1):  # 1..2
                name = 'string' + str(j)
                label = Label(text=self.content.get(str(i))[name], color=(0, 0, 0, 1),
                              size_hint=(len(self.content.get(str(i))[name]) / 100, 0.1),
                              width=len(self.content.get(str(i))[name]))
                self.grid.add_widget(label)
                if j == 1:
                    self.grid.add_widget(inp)
                    self.inputs.append(inp)
        for k in range(self.items - 1, self.items + 1):
            inp2 = TextInput(text=self.content.get(str(k))['mixed1'],
                             size_hint=(len(self.content.get(str(k))['mixed1']) / 100, 0.08),
                             width=len(self.content.get(str(k))['mixed1']))
            self.grid.add_widget(inp2)
            self.grid.add_widget(Label(text=self.content.get(str(k))['string1'], color=(0, 0, 0, 1),
                                       size_hint=(len(self.content.get(str(k))['string1']) / 100, 0.1),
                                       width=len(self.content.get(str(k))['string1'])))
            self.inputs.append(inp2)

        self.layout = self.grid
        return self

    def check_3(self):
        j = 0
        for i in range(0, self.content.count() - 2):

            if self.inputs[i].text != self.content.get(str(i + 1))['klucz1']:
                self.inputs[i].background_color = (246 / 255, 120 / 255, 101 / 255, 1)
                j += 1
            else:
                self.inputs[i].background_color = (210 / 255, 246 / 255, 101 / 255, 1)

        print(j)
        self.grid.add_widget(
            Label(text="Wynik: " + str(self.items - j) + '/' + str(self.items), color=(1, 0, 1, 1),
                  valign='bottom', size_hint=(1, 0.25)))
        return j

    def check_2(self):
        self.items = self.content.count() - 2
        j = 0
        for i in range(0, self.content.count() - 2):
            if self.inputs[i].text != self.content.get(str(i + 1))['klucz']:
                self.inputs[i].background_color = (246 / 255, 120 / 255, 101 / 255, 1)

                print(self.inputs[i].text, self.content.get(str(i + 1))['klucz'])
                j += 1
            else:
                self.inputs[i].background_color = (210 / 255, 246 / 255, 101 / 255, 1)
        print(j)
        self.grid.add_widget(
            Label(text="Wynik: " + str(self.items - j) + '/' + str(self.items), color=(1, 0, 1, 1),
                  valign='bottom'))
        return j

    def change_input_color(self, i, color):
        self.inputs[i].background_color = color

    def check_1(self):
        print(len(self.inputs))
        j = 0
        for i in range(0, self.content.count() - 1):
            if self.inputs[i].text != self.content.get(str(i + 1))['klucz']:
                self.inputs[i].background_color = (246 / 255, 120 / 255, 101 / 255, 1)
                j += 1
            else:
                self.inputs[i].background_color = (210 / 255, 246 / 255, 101 / 255, 1)
            print(self.inputs[i].text, self.content.get(str(i + 1))['klucz'])
        self.grid.add_widget(
            Label(text="Wynik: " + str(10 - j) + '/' + str(self.content.count() - 1), color=(1, 0, 1, 1),
                  valign='bottom'))
        return j

    def type_4(self):
        self.inputs = []
        # self.grid = GridLayout(cols=3)

        # self.grid.pos_hint = {"center_x": 0.45, "y": 0.25}
        # self.grid.size_hint = (.5, .55)
        self.grid.cols = 3
        self.clear_canvas()
        self.items = self.content.count() - 3
        label_ex = Label()
        inp_ex = TextInput(text=self.content['example']['klucz'], disabled=True, size_hint=(.5, None), height=50)
        label_ex.text = self.content['example']['string']
        label_ex.color = (1, 0, 1, 1)
        self.grid.add_widget(label_ex)
        self.grid.add_widget(Image(size_hint=(.8, None), height=50, source=self.content.get('example')['source']))
        self.grid.add_widget(inp_ex)
        for i in range(1, self.items + 1):
            inp = TextInput(id='input' + str(i), size_hint=(.5, None), height=50)
            self.inputs.append(inp)
            label = Label()
            label.text = self.content.get(str(i))['string']
            label.color = (1, 0, 1, 1)
            self.grid.add_widget(
                label)
            self.grid.add_widget(
                Image(size_hint=(.5, None), height=50, source=self.content.get(str(i))['source']))
            self.grid.add_widget(inp)
        self.grid.add_widget(Label(text=self.content.get('curiosity')['string'], color=(1, 0, 1, 1)))
        self.layout = self.grid
        return self

    def check_4(self):
        j = 0
        for i in range(0, self.items):
            if self.inputs[i].text != self.content.get(str(i + 1))['klucz']:
                self.inputs[i].background_color = (246 / 255, 120 / 255, 101 / 255, 1)
                j += 1
            else:
                self.inputs[i].background_color = (210 / 255, 246 / 255, 101 / 255, 1)
            print(self.inputs[i].text, self.content.get(str(i + 1))['klucz'])
        self.grid.add_widget(
            Label(text="Wynik: " + str(self.items - j) + '/' + str(self.items), color=(1, 0, 1, 1),
                  valign='bottom'))
        return j

    def clear_canvas(self):
        for child in [child for child in self.grid.children]:
            self.grid.remove_widget(child)

    def set_grid(self):
        for i in range(1, self.items):
            inp = TextInput(id='input' + str(i), size_hint=(.5, None), height=40)
            self.inputs.append(inp)
            self.grid.add_widget(Label(text=self.content.get(str(i))['string'], color=(1, 0, 1, 1)))
            self.grid.add_widget(inp)

        self.layout = self.grid
