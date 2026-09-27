from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Button
from textual.containers import HorizontalGroup, Container, Horizontal




class NmapDeleteModal(ModalScreen[bool]):

    BINDINGS = [
        ("y", "delete_card", "Y"),
        ("n", "cancel_card", "N"),
    ]

    DEFAULT_CSS = """
        NmapDeleteModal {
            align: center middle;
            border: round $accent;
            width: 100%;
        }

        NmapDeleteModal > Container {
            width: auto;
            height: auto;
            border: thick $background 80%;
            background: $surface;
        }

        NmapDeleteModal > Container > Label {
            width: 100%;
            content-align-horizontal: center;
            margin-top: 1;
        }

        NmapDeleteModal > Container > Horizontal {
            width: auto;
            height: auto;
        }

        NmapDeleteModal > Container > Horizontal > Button {
            margin: 2 4;
        }
        
    """

    def __init__(self, session_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_name = session_name

    def compose(self) -> ComposeResult:
        with Container(): 
            yield Label(f'Are you sure you want to delete Session {self.session_name}')
            with Horizontal():
                yield Button(label="Yes", id="yes-btn")
                yield Button(label="No", id="no-btn")

    def action_delete_card(self):
        self.dismiss(True)

    def action_cancel_card(self):
        self.dismiss(False)

    def on_button_pressed(self, event: Button.Pressed):
        button_id = self.query_one("#yes-btn", Button)
        if button_id:
            self.dismiss(True)
        else:
            self.dismiss(False)
