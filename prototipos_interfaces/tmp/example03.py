from textual.app import App
from textual.widgets import LoadingIndicator, Button
from textual.containers import Container
from textual import on

class WelcomeApp(App):

    def compose(self):
        self.button_load = Button("Exibir Load", variant="success", id="b_extrair")
        yield self.button_load
        self.button_unload = Button("Remover Load", variant="warning", id="b_exibir")
        yield self.button_unload


    @on(Button.Pressed, "#b_extrair")
    def something(self) -> None:
        self.mount(LoadingIndicator(id="amor"))

    @on(Button.Pressed, "#b_exibir")
    def pressed(self) -> None:
        self.query_one("#amor").remove()


if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
