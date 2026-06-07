from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider


class LabelSlider(BoxLayout):
    def __init__(self, *args, min=0, max=100, value=0, step=1, orientation='horizontal', **kwargs):
        super().__init__(*args, orientation=orientation, **kwargs)

        self.slider = Slider(min=min, max=max, value=value, step=step, orientation=orientation)
        self.label = Label(size_hint_x=0.25)
        self.label.text = str(int(self.slider.value))
        self.slider.bind(value=lambda i, v: setattr(self.label, 'text', str(int(v))))
        self.add_widget(self.slider)
        self.add_widget(self.label)
