from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from .popup_standard_buttons import PopupStandardButtons

class PopupFileChooser(PopupStandardButtons):
    def __init__(self, *args, filters=[], path=None, **kwargs):
        super().__init__(
            *args, second_container=BoxLayout(orientation="vertical"), **kwargs
        )

        if path == None:
            path = ""
        self.path = path
        self.file_chooser_list_view = FileChooserListView( filters=filters, path=self.path )
        self.second_container.add_widget(self.file_chooser_list_view)
        self.bind(on_open=self._on_open)

    def set_permissions(self, on_granted=None):
        pass  # PC no necesita, Android sobreescribe

    def _on_open(self, *args):
        self.set_permissions(on_granted=self._refresh_files)

    def _refresh_files(self):
        self.file_chooser_list_view.path = self.path
        self.file_chooser_list_view._update_files()

    def get_selection(self):
        return self.file_chooser_list_view.selection
