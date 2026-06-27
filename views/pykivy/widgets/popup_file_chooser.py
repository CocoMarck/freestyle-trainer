from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from .popup_standard_buttons import PopupStandardButtons

class PopupFileChooser(PopupStandardButtons):
    def __init__(self, *args, filters=[], **kwargs):
        super().__init__(
            *args, second_container=BoxLayout(orientation="vertical"), path:str=None  **kwargs
        )

        self.file_chooser_list_view = FileChooserListView( filters=filters, path=path )
        self.second_container.add_widget(self.file_chooser_list_view)
        self.bind(on_open=self._on_open)

    def _on_open(self, *args):
        self.set_permissions()

    def set_permissions(self):
        pass  # PC no necesita, Android sobreescribe

    def get_selection(self):
        return self.file_chooser_list_view.selection
