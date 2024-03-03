# hello_textual3.py

from textual.app import App, ComposeResult
from textual.widgets import Button, Label


class HelloWorld(App):

    def compose(self) -> ComposeResult:
        self.close_button = Button("Close", id="close")
        yield Label("Hello Textual")
        yield self.close_button

    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"
        self.close_button.styles.background = "red"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)

if __name__ == "__main__":
    app = HelloWorld()
    app.run()
