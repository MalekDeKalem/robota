from textual.app import App, ComposeResult

from textual.widgets import Footer, Header, ListView, ListItem
from widgets.toolcard import ToolCard
from modals.thememodal import ThemeModal
from screens.nmapscreen import NmapScreen
from textual import on


class Robota(App):
    CSS_PATH = "./styles/toolcard.tcss"
    BINDINGS = [
        ("ctrl+t", "set_theme", "Select Theme"),
    ]


    def __init__(self):
        super().__init__()
        self.tools = [
            {
                    "icon": r"""                 ⢀⠀⠄⠄⠢⠠⠐⠄⠂⠢⠠⠂⠄⡠⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢄⠢⠑⠈⠀⠈⠀⡀⠄⠀⠄⠂⠀⠄⠀⠄⠀⡈⠐⠈⠔⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⠐⡁⠠⠀⠄⠠⡨⠠⡡⢂⠪⡘⡐⢅⠣⢒⢐⠔⢄⠄⡀⢂⠀⠂⠩⠨⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠠⡐⠑⠐⠀⠂⢐⢀⠢⠡⡑⠌⡂⡂⢅⠪⡐⠜⢄⠌⡀⠢⡈⡢⢘⠨⠐⠨⠠⠂⡐⠀⠌⠘⠄⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡀⠄⠪⠈⠄⠐⡀⠡⠊⠐⢀⠂⡐⠄⠅⠢⠨⡂⡱⡼⡝⢵⣣⢪⠨⢂⠔⠠⠡⡁⠌⠠⠁⢂⠢⡀⠂⡐⠁⠃⠄⡀⠀⠀⠀⠀
⠀⠀⢀⠄⢁⠐⠀⢁⠄⡑⠈⠀⡁⠈⢀⠀⡂⠅⠨⢈⢂⠢⣫⡺⡊⢓⣕⡳⢁⠅⠂⠅⠡⢀⠂⠐⠈⠀⡀⠄⠑⡠⠈⡠⠁⡘⠠⡀⠀⠀
⠀⠠⠂⡂⡠⠡⠊⠄⠄⠀⠀⠁⠀⠠⠀⠀⢐⠐⠈⡀⢂⠅⢣⡳⡭⣣⡺⠜⡐⡈⠄⠡⠈⠄⠀⠐⠀⠁⠀⠀⡀⠠⢑⠠⢂⠄⡈⠌⡂⠀
⠀⠡⡑⢄⢊⢢⠡⠑⢄⠌⡀⡈⠀⠄⠀⢁⠀⠌⡐⠀⡂⠌⡐⠨⡘⠡⠡⡁⢂⠐⡀⠅⠌⠀⠐⠀⠐⠀⣀⢁⠄⠌⠔⠨⡐⡈⡄⡢⠁⠀
⠀⠀⠀⠀⠁⠁⠁⠃⠆⠥⡨⢐⢁⠆⢌⢀⠀⠄⠂⡡⢀⠂⠌⠂⠄⠅⠡⠐⡀⠂⠔⠐⢀⢈⠠⡈⠢⠑⢄⠅⠜⠌⠊⠊⠈⠈⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠒⢰⢐⠨⡈⠂⠆⢄⠢⢨⠠⠡⡈⢄⢑⢐⠄⢅⠅⠢⠑⠔⠡⡈⠆⠍⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⢂⠅⡅⡂⠌⠄⠡⢁⢊⠐⠄⠡⠨⠠⢨⠠⡑⠜⠑⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢎⠙⣎⢉⡎⠱⡰⠁⡯⡨⡙⡜⢎⠍⣅⢓⠜⠨⠊⡮⢊⢍⡚⣎⢩⣁⢲⡐⣊⠭⡘⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢸⡌⡢⡇⣣⣑⡇⡷⢡⣃⠵⣸⢨⡸⠔⢁⣀⠀⢇⢇⣀⠇⣟⢬⣌⢪⡇⢗⣌⠝⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠑⠋⠒⠓⠒⠑⠒⠚⠒⠑⠚⠒⠒⠚⠀⠘⠒⠁⠈⠒⠒⠉⠓⠒⠃⠓⠊⠚⠐⠓""",

                "description":"""Nmap is a free an open-source network mapper used for network discovery,\nsecurity auditing and port scanning. It can be utilized as a method for reconnaissance to gather information about a target such as what services run on which ports.""",
                "name":"nmap",
            }, 
            {
                "icon": r"""⠄⠄⣴⣶⣤⡤⠦⣤⣀⣤⠆⠄⠄⠄⠄⠄⣈⣭⣭⣿⣶⣿⣦⣼⣆⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠉⠻⢿⣿⠿⣿⣿⣶⣦⠤⠄⡠⢾⣿⣿⡿⠋⠉⠉⠻⣿⣿⡛⣦⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠈⠄⠄⠄⠈⢿⣿⣟⠦⠄⣾⣿⣿⣷⠄⠄⠄⠄⠻⠿⢿⣿⣧⣄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣸⣿⣿⢧⠄⢻⠻⣿⣿⣷⣄⣀⠄⠢⣀⡀⠈⠙⠿⠄⠄⠄⠄
⠄⠄⢀⠄⠄⠄⠄⠄⠄⢠⣿⣿⣿⠈⠄⠄⠡⠌⣻⣿⣿⣿⣿⣿⣿⣿⣛⣳⣤⣀⣀⠄⠄
⠄⠄⢠⣧⣶⣥⡤⢄⠄⣸⣿⣿⠘⠄⠄⢀⣴⣿⣿⡿⠛⣿⣿⣧⠈⢿⠿⠟⠛⠻⠿⠄⠄
⠄⣰⣿⣿⠛⠻⣿⣿⡦⢹⣿⣷⠄⠄⠄⢊⣿⣿⡏⠄⠄⢸⣿⣿⡇⠄⢀⣠⣄⣾⠄⠄⠄
⣠⣿⠿⠛⠄⢀⣿⣿⣷⠘⢿⣿⣦⡀⠄⢸⢿⣿⣿⣄⠄⣸⣿⣿⡇⣪⣿⡿⠿⣿⣷⡄⠄
⠙⠃⠄⠄⠄⣼⣿⡟⠌⠄⠈⠻⣿⣿⣦⣌⡇⠻⣿⣿⣷⣿⣿⣿⠐⣿⣿⡇⠄⠛⠻⢷⣄
⠄⠄⠄⠄⠄⢻⣿⣿⣄⠄⠄⠄⠈⠻⣿⣿⣿⣷⣿⣿⣿⣿⣿⡟⠄⠫⢿⣿⡆⠄⠄⠄⠁
⠄⠄⠄⠄⠄⠄⠻⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣀⣤⣾⡿⠃⠄⠄⠄⠄
⠄⠄⠄⠄⢰⣶⠄⠄⣶⠄⢶⣆⢀⣶⠂⣶⡶⠶⣦⡄⢰⣶⠶⢶⣦⠄⠄⣴⣶⠄⠄⠄⠄
⠄⠄⠄⠄⢸⣿⠶⠶⣿⠄⠈⢻⣿⠁⠄⣿⡇⠄⢸⣿⢸⣿⢶⣾⠏⠄⣸⣟⣹⣧⠄⠄⠄
⠄⠄⠄⠄⠸⠿⠄⠄⠿⠄⠄⠸⠿⠄⠄⠿⠷⠶⠿⠃⠸⠿⠄⠙⠷⠤⠿⠉⠉⠿⠆⠄⠄""",

                "description":"""Hydra is a powerful open-source tool. It can be used to do various things like performing dictionary attacks on different services (SSH, FTP, HTTP, Telnet). It also is a tool ideal for cracking hashes.""",
                "name": "hydra",
            },
        ]

        self.tool_index = 0
        self.screen_list = [0,0]

    def on_mount(self) -> None:
        self.theme = "tokyo-night"
    
    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        self.notify(f"Selected item: {event.list_view.index}")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id != "tool-list":
            return
        
        self.notify(f"Select Tool: {self.tools[event.list_view.index]}")
        if self.tools[event.list_view.index]["name"] == "nmap":
            if self.is_screen_installed("NmapScreen"):
                self.push_screen(self.screen_list[event.list_view.index])
            else:
                screen = NmapScreen()
                self.screen_list[event.list_view.index] = screen
                self.install_screen(screen, name="NmapScreen")
                self.push_screen(screen)
        elif self.tools[event.list_view_index]["name"] == "hydra":
            pass

    def action_set_theme(self) -> None: 
            self.push_screen(ThemeModal())

    def compose(self) -> ComposeResult:
        yield Header()
        items = [ListItem(ToolCard(icon=tool["icon"], description=tool["description"])) for tool in self.tools]
        yield ListView(*items, id="tool-list")
        yield Footer()






if __name__ == "__main__":
    app = Robota()
    app.run()
