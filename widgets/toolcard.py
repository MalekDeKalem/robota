from textual.app import ComposeResult, RenderResult
from textual.widget import Widget 
from textual.widgets import Static
from textual.containers import Grid
from textual.reactive import reactive

class ToolCard(Widget):

    icon = reactive("")
    description = reactive("")

    def __init__(self, icon: str = "", description: str = "", **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.description = description

    def compose(self):
        yield Grid(
            Static(self.icon, classes="box"),
            Static(self.description, classes="desc-box")
        )

