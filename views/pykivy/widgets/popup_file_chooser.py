from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from .popup_standard_buttons import PopupStandardButtons

class PopupFileChooser(PopupStandardButtons):
    def __init__(self, *args, filters=[], path="./", **kwargs):
        super().__init__(*args, second_container=BoxLayout(orientation="vertical"), **kwargs)

        self.file_chooser_list_view = FileChooserListView( filters=filters, path=path )
        self.second_container.add_widget(self.file_chooser_list_view)

    def get_selection(self):
        return self.file_chooser_list_view.selection
