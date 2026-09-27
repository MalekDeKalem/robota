from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Input
from textual.containers import CenterMiddle, Container
from widgets.nmapcard import NmapCard

class NmapCreateModal(ModalScreen):

    
    DEFAULT_CSS = """

        NmapCreateModal {
            align: center middle;
            border: round $accent;
        }

        NmapCreateModal > Input {
            width: 40%;
            height: 5;
            border: round $accent;
            background: $surface;
        }

    """


    def compose(self) -> ComposeResult:
        yield Input(placeholder="Insert Session name here") 

    def on_input_submitted(self, message: Input.Submitted):
        self.app.notify(f'Session: {message.value} added')
        newcard = NmapCard(message.value)
        self.dismiss(newcard)

        
