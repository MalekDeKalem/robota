from textual.widget import Widget
from textual.widgets import Label, Input
from textual.app import ComposeResult
from textual.containers import Horizontal



class Range(Widget):

    DEFAULT_CSS = """
        Input {
            width: 10;
        }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("from")
            yield Input(type="integer")
            yield Label("to")
            yield Input(type="integer")
