from .popup_box_layout import PopupBoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

class PopupStandardButtons( PopupBoxLayout ):
    def __init__(self, *args, second_container, text_cancel="cancel", text_ok="ok", cancel_button=True, **kwargs):
        super().__init__( *args, orientation="vertical", **kwargs)

        self.second_container = second_container
        self.second_container.size_hint = (1, 0.9)
        self.content.add_widget( self.second_container )

        self.button_cancel = Button(text=text_cancel)
        self.button_cancel.bind(on_press=self.dismiss)

        box_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.1)
        )
        self.content.add_widget(box_layout)
        if cancel_button:
            box_layout.add_widget(self.button_cancel)

        self.button_ok = Button(text=text_ok)
        self.button_ok.bind( on_press=self.dismiss )
        box_layout.add_widget(self.button_ok)
