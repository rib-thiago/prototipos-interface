# view.py

from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Select, Button, Header, Footer, LoadingIndicator
from textual.containers import ScrollableContainer, Container
import os

class ShowContentView(App):
    CSS_PATH = "hello.css"
    BINDINGS = [("q", "quit", "Sair")]
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container():
            self.label = Label(id="hello")
            yield self.label
            self.path = Input(placeholder="Path do Diretório", type="text")
            yield self.path
            self.select = Select(())
            yield self.select
            self.button = Button("Extrair Texto", variant="success")
            yield self.button
            self.content_label = Label(id="hello2")
            self.content = None
#             yield LoadingIndicator(id="indicator")
            with ScrollableContainer() as container: 
                yield self.content_label
            yield container
        yield Footer()

    def on_input_changed(self, event):
        self.label.update(f'[red bold]Diretório:[/] {event.input.value}')

    def on_input_submitted(self, event):
        files = os.listdir(event.input.value)
        file_tuples = [(file_name, file_name) for file_name in files]
        self.select.set_options(file_tuples)

    def on_select_changed(self, event):
        selected_file = event.value
        directory_path = self.path.value.strip()
        self.file_path = os.path.join(directory_path, selected_file)
        self.label.update(f'[green bold]Arquivo:[/] {self.file_path}')
        

    def on_button_pressed(self, event):
        if self.file_path.endswith('.jpg') or self.file_path.endswith('.png'):
            self.controller.show_image(self.file_path)
        self.content = self.controller.extract_text(self.file_path, language='rus')
        self.content_label.update(self.content)

    def action_remove_load(self):
        self.query_one("#indicator").remove()

