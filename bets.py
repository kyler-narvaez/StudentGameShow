from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import VerticalScroll
from textual.screen import Screen

class BettingButton(Button):
    def __init__(self, name: str):
        super().__init__(f"{name}: Incorrect", id=name)
        self.has_bet = False
        self.can_focus = False
        self.contestant_name = name
        self.add_class("no-bet")

    def toggle(self):
        self.has_bet = not self.has_bet
        self.label = f"{self.contestant_name}: {'Correct' if self.has_bet else 'Incorrect'}"
        self.remove_class("placed-bet" if not self.has_bet else "no-bet")
        self.add_class("placed-bet" if self.has_bet else "no-bet")

class BettingScreen(Screen):
    def __init__(self, contestants):
        super().__init__()
        self.contestants = contestants
        self.buttons = {}

    def compose(self) -> ComposeResult:
        yield Static("🎲 Place your bets!", classes="title")

        with VerticalScroll():
            for name in self.contestants:
                btn = BettingButton(name)
                self.buttons[name] = btn
                yield btn

        yield Button("✅ Confirm Bets", id="confirm", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            results = {name: btn.has_bet for name, btn in self.buttons.items()}
            self.app.exit(results)
        else:
            self.buttons[event.button.id].toggle()

def place_bets(contestants):
    class BettingApp(App):
        CSS = """
        Screen {
            align: center middle;
        }

        Button {
            width: 40;
            margin: 1;
            content-align: center middle;
        }

        .title {
            height: 2;
            content-align: center middle;
        }

        .placed-bet {
            background: green;
            color: black;
        }

        .no-bet {
            background: grey;
            color: white;
        }
        """

        def on_mount(self):
            self.push_screen(BettingScreen(contestants))

    app = BettingApp()
    return app.run()
