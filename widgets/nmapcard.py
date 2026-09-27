from textual.widget import Widget
from textual.widgets import Static
from textual.app import RenderResult, ComposeResult


class NmapCard(Widget):


    DEFAULT_CSS = """
       NmapCard {
           width: 100%;
           height: 3;
           border: round $accent;
       } 
    """

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name


    @property
    def name(self,):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def compose(self) -> ComposeResult:
        yield Static(f'Nmap session: {self.name}')

