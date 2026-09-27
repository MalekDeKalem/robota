from textual.screen import Screen
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Static, ListItem, ListView, Footer
from modals.nmapcreatemodal import NmapCreateModal
from modals.nmapdeletemodal import NmapDeleteModal
from widgets.nmapcard import NmapCard
from screens.nmapsettingsscreen import NmapSettingsScreen


class NmapScreen(Screen):

    BINDINGS = [
        ("a", "add_nmap_card", "Add nmap instance"),
        ("d", "delete_nmap_card", "Delete nmap instance"),
        ("ctrl+b", "back_screen", "Go back"),
    ]

    cards = reactive[list[NmapCard]]([])

    def __init__(self, *args, **kwargs):
        self.screen_list = []
        super().__init__(*args, **kwargs)


    def compose(self) -> ComposeResult:
        yield ListView(id="nmap-list")
        yield Footer()
    

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        self.notify(f"length of cards: {len(self.cards)}")

    def watch_add_nmap_card(self) -> None:
        list_view = self.query_one("#nmap-list", ListView)
        list_view.remove_children()
        list_view.mount(*self.cards)

    def nmap_created(self, card: NmapCard | None) -> None:
        if card is not None:
            self.card = [*self.cards, card]

            list_view = self.query_one("#nmap-list", ListView)
            list_view.append(ListItem(card))

    def action_add_nmap_card(self) -> None:
        nmap_settings = NmapSettingsScreen()
        self.screen_list.append(nmap_settings)
        self.app.push_screen(NmapCreateModal(), self.nmap_created)

    def nmap_remove(self, pressed: bool):
        if pressed:
            list_view = self.query_one("#nmap-list", ListView)
            list_view.pop(list_view.index)
            self.app.uninstall_screen(self.screen_list[list_view.index])
            self.screen_list.pop(list_view.index)

    def action_delete_nmap_card(self) -> None:
        list_view = self.query_one("#nmap-list", ListView)
        list_item = list_view.highlighted_child
        selected_card = list_item.get_child_by_type(NmapCard)
        self.app.push_screen(NmapDeleteModal(session_name=selected_card.name), self.nmap_remove)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id != "nmap-list":
            return

        list_view = self.query_one("#nmap-list", ListView)
        list_item = list_view.highlighted_child
        selected_card = list_item.get_child_by_type(NmapCard)

        if self.app.is_screen_installed(selected_card.name):
            self.app.push_screen(self.screen_list[list_view.index])
        else:
            self.app.install_screen(self.screen_list[list_view.index], name=selected_card.name)
            self.app.push_screen(self.screen_list[list_view.index])



    def action_back_screen(self) -> None:
        self.app.pop_screen()
