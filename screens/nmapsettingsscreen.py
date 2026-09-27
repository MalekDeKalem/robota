from textual.widgets import Input, Button, Footer, Label, Pretty, RadioButton, RadioSet, Checkbox, Switch
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, HorizontalGroup, VerticalGroup, Container
from textual.validation import Function, Number
from textual import on
from textual import work
from textual.reactive import reactive
from widgets.range import Range
import subprocess
import re

class NmapSettingsScreen(Screen):

    BINDINGS = [
        ("ctrl+b", "back_screen", "Go back"),
    ]

    CSS = """
        Input.-valid {
            border: tall $success 60%;
        }
        Input.-valid:focus {
            border: tall $success;
        }

        Horizontal {
            border: heavy $accent;
        }

        Screen {
            layout: vertical;
        }

        .great-box {
            height: 20;
            border: solid $panel;
        }

        .greater-box {
            height: 25;
            border: solid $panel;
        }

        .large-box {
            height: 25;
            border: solid $panel;
        }

        .small-box {
            height: 10;
            border: solid $panel;
        }

        .medium-box {
            height: 15;
            border: solid $panel;
        }

    """


    is_zombie_scan_set: reactive[bool] = reactive(False)
    is_ftp_bounce_scan_set: reactive[bool] = reactive(False)
    is_ip_proto_switch_set: reactive[bool] = reactive(False)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.query_one("#syn-scan").tooltip = """SYN scan is the default and most popular scan option for good reasons. It can be performed quickly, scanning thousands of ports per second on a fast network not hampered by restrictive firewalls. It is also relatively unobtrusive and stealthy since it never completes TCP connections. SYN scan works against any compliant TCP stack rather than depending on idiosyncrasies of specific platforms as Nmap's FIN/NULL/Xmas, Maimon and idle scans do. Italso allows clear, reliable differentiation between the open, closed, and filtered states."""
        self.query_one("#tcp-scan").tooltip = """TCP connect scan is the default TCP scan type when SYN scan is not an option. This is the case when a user does not have raw packet privileges. Instead of writing raw packets as most other scan types do, Nmap asks the underlying operating system to establish a connec‐ tion with the target machine and port by issuing the connect system call. This is the same high-level  system call that web browsers, P2P clients, and most other network-enabled applications use to establish a connection. It is part of a programming interface known as the Berkeley Sockets API. Rather than read raw packet responses off the wire, Nmap uses this API to obtain status information on each connection attempt."""
        self.query_one("#ack-scan").tooltip = """This scan is different than the others discussed so far in that it never determines open (or even open|filtered) ports. It is used to map out firewall rulesets, determining whether they are stateful or not and which ports are filtered."""
        self.query_one("#fin-scan").tooltip = """Sets just the TCP FIN bit."""
        self.query_one("#xmas-scan").tooltip = """Sets the FIN, PSH, and URG flags, lightning the packets up like a Christmas tree."""
        self.query_one("#null-scan").tooltip = """Does not set any bits (TCP flag header is 0)."""
        self.query_one("#zombie-scan").tooltip = """ This advanced scan method allows for a truly blind TCP port scan of the target (meaning no packets are sent to the target from your real IP address). Instead, a unique side-channel attack exploits predictable IP fragmentation ID sequence generation on the zombie host to glean information about the open ports on the target. IDS systems will display the scan as coming from the zombie machine you specify (which must be up and meet certain criteria).."""
        self.query_one("#ftp-bounce-scan").tooltip = """An interesting feature of the FTP protocol (RFC 959[8]) is support for so-called proxy FTP connections. This allows a user to connect to one FTP server, then ask that files be sent to a third-party server. Such a feature is ripe for abuse on many levels, so most servers have ceased supporting it. One of the abuses this feature allows is causing the FTP server to port scan other hosts. Simply ask the FTP server to send a file to each interesting port of a target host in turn.The error message  will describe whether the port is open or not. This is a good way to bypass firewalls because organizational FTP servers are often placed where they have more access to other internal hosts than any old Internet host would. Nmap supports FTP bounce scan with the -b option. It takes an argument of the form username:password@server:port. Server is the name or IP address of a vulnerable FTP server. As with a normal URL, you may omit username:password, in which case anonymous login credentials (user: anonymous password:-wwwuser@) are used. The port number (and preceding colon) may be omitted as well, in which case the default FTP port (21) on server is used."""
        self.query_one("#tcp-window-scan").tooltip = """Window scan is exactly the same as ACK scan except that it exploits an implementation detail of certain systems to differentiate open ports from closed ones, rather than always printing unfiltered when a RST is returned. It does this by examining the TCP Window field of the RST packets returned. On some systems, open ports use a positive window size (even for RST packets) while closed ones have a zero window. So instead of always listing a port as unfiltered when it receives a RST back, Window scan lists the port as open or closed if the TCP Window value in that reset is positive or zero, respectively. This scan relies on an implementation detail of a minority of systems out on the Internet, so you can't always trust it. Systems that don't support it will usually return all ports closed. Of course, it is possible that the machine really has no open ports. If most scanned ports are closed but a few common port numbers (such as 22, 25, 53) are filtered, the system is most likely susceptible. Occasionally, systems will even show the exact opposite behavior. If your scan shows 1,000 open ports and three closed or filtered ports, then those three may very well be the truly open ones."""
        self.query_one("#tcp-maimon-scan").tooltip = """The Maimon scan is named after its discoverer, Uriel Maimon. He described the technique in Phrack Magazine issue #49 (November 1996). Nmap, which included this technique, was released two issues later. This technique is exactly the same as NULL, FIN, and Xmas scans, except that the probe is FIN/ACK. According to RFC 793[7] (TCP), a RST packet should be generated in response to such a probe whether the port is open or closed. However, Uriel noticed that many BSD-derived systems simply drop the packet if the port is open."""
        self.query_one("#ip-proto-scan").tooltip = """IP protocol scan """


    def action_back_screen(self) -> None:
        self.app.pop_screen()

    def compose(self) -> ComposeResult:
        with Container(classes="medium-box"):
            yield Label("Target IP")
            yield Input(id="target-ip", placeholder="insert target ip", max_length=15, validators=[Function(is_ip, "Not a valid ip address")])
            yield Pretty("", id="target-ip-validation")
            yield Label("Verbosity Levels")
            yield Input(id="verbosity", placeholder="verbosity level in the range 0-3", type="integer", max_length=1, valid_empty=True, validators=[Number(minimum=0, maximum=3)])
            yield Pretty("", id="verbosity-level-validation")

        with Container(classes="greater-box"):
            yield Label("TCP Scan Techniques")
            with Vertical():
                yield Label("Switch on IP Proto Scan (Disables all other tcp scan techniques)")
                yield Switch(animate=True, id="ip-proto-scan") # -sO
                with Horizontal():
                    with RadioSet(id="tcp-scan-list"):
                        yield RadioButton("SYN scan", id="syn-scan")              # -sS
                        yield RadioButton("TCP scan", id="tcp-scan")              # -sT
                        yield RadioButton("ACK scan", id="ack-scan")              # -sA
                        yield RadioButton("FIN scan", id="fin-scan")              # -sF
                        yield RadioButton("XMAS scan", id="xmas-scan")            # -sX
                        yield RadioButton("NULL scan", id="null-scan")            # -sN
                        yield RadioButton("TCP window scan", id="tcp-window-scan")# -sW
                        yield RadioButton("TCP maimon scan", id="tcp-maimon-scan")# -sM
                        yield RadioButton("Zombie scan", id="zombie-scan")        # -sI
                        yield RadioButton("FTP bounce scan", id="ftp-bounce-scan") # -b
                yield Input(id="zombie-host", placeholder="Zombie host")
                yield Input(id="ftp-bounce-input", placeholder="username:password@server:port")


        with Container(classes="small-box"):
            yield Label("UDP Scan")
            with Vertical():
                yield Label("Enable UDP Scan")
                yield Switch(animate=True, id="udp-scan") # -sU
        
        with Container(classes="medium-box"):
            yield Label("Version Detection")
            with Vertical():
                with Horizontal():
                    with VerticalGroup():
                        yield Checkbox("Enable OS and version detection") # -A
                        yield Checkbox("Enable version detection") # -sV
                        yield Checkbox("Include all ports for version detection") # --allports

        with Container(classes="medium-box"):
            yield Label("Port specification and scan order")
            with Vertical():
                with Horizontal():
                    with RadioSet(id="port-scan-list"):
                        yield RadioButton("Scan all ports", id="all-port-scan")
                        yield RadioButton("Scan port range", id="scan-port-range")

                yield Range(id="port-range")

        with Container(classes="medium-box"):
            yield Label("Output")
            with Vertical():
                with Horizontal():
                    with RadioSet(id="output-list"):
                        yield RadioButton("Output in normal format")
                        yield RadioButton("Output in xml format")
                        yield RadioButton("Output in greppable format")
                        yield RadioButton("Output in all three formats")

        yield Button("Run nmap", id="run-button")
        yield Footer()


    @on(RadioSet.Changed, "#tcp-scan-list")
    def tcp_radioset(self, event: RadioSet.Changed) -> None:
        self.is_zombie_scan_set = (event.pressed.id == "zombie-scan")
        self.is_ftp_bounce_scan_set = (event.pressed.id == "ftp-bounce-scan")
    
    @on(Input.Changed, "#target-ip")
    def show_ip_validation(self, event: Input.Changed) -> None:
        if event:
            if not event.validation_result.is_valid:
                self.query_one("#target-ip-validation").update(event.validation_result.failure_descriptions)
            else:
                self.query_one("#target-ip-validation").update("")

    @on(Input.Changed, "#verbosity")
    def show_verbosity_validation(self, event: Input.Changed) -> None:
        if event.validation_result is not None:
            if not event.validation_result.is_valid:
                self.query_one("#verbosity-level-validation").update(event.validation_result.failure_descriptions)
            else:
                self.query_one("#verbosity-level-validation").update("")

    @on(Switch.Changed, "#ip-proto-scan")
    def ip_proto_scan(self, event: Switch.Changed) -> None:
        scanlist = self.query_one("#tcp-scan-list")
        scanlist.disabled = event.value

    def watch_is_zombie_scan_set(self, show: bool) -> None:
            self.query_one("#zombie-host").display = show

    def watch_is_ftp_bounce_scan_set(self, show: bool) -> None:
        self.query_one("#ftp-bounce-input").display = show


    # TODO
    # Implement run_command takes the states of all the widgets and
    # constructs a nmap command and runs it with subprocess and shows the progress of it 
    @work(exclusive=True)
    async def run_command(self):
        pass


def is_ip(value: str) -> bool:
    ipv4_pattern = "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ipv4_pattern, value)


