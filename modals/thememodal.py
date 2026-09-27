from textual.app import ComposeResult
from textual.widgets import ListItem, Label, ListView
from textual.screen import ModalScreen
from textual import on


class ThemeModal(ModalScreen):

    DEFAULT_CSS = """

        ThemeModal {
            align: center middle;
        }

        ListView {
            width: 40;
            height: 12;
            border: round $accent;
            background: $surface;
        }

    """
    
    BINDINGS = [
        ("up", "cursor_up", "Up"),
        ("down", "cursor_down", "Down"),
    ]

    def compose(self) -> ComposeResult:
        items = [ListItem(Label(theme)) for theme in self.app.available_themes.keys()]
        yield ListView(*items, id="theme-list")

    def action_cursor_up(self):
        list_view = self.query_one(ListView)
        list_view.action_cursor_up()

    def action_cursor_down(self):
        list_view = self.query_one(ListView)
        list_view.action_cursor_down()
    
    @on(ListView.Selected, "#theme-list")
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.app.theme = list(self.app.available_themes.keys())[event.list_view.index]
        self.app.pop_screen()

