# view.py

from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Select, Button, Header, Footer, LoadingIndicator
from textual.containers import ScrollableContainer, Container, Center, Horizontal, Vertical
from textual import on
import os

Languages = ('eng', 'por', 'rus')


class ShowContentView(App):
    CSS_PATH = "style.css"
    BINDINGS = [("q", "quit", "Sair")]

    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="cont01"):
            self.label = Label(id="label_dir")
            yield self.label
            # Label para mostrar o idioma selecionado
            self.language_label = Label(id="label_lang")
            yield self.language_label
        self.path = Input(placeholder="Path do Diretório", type="text", id="input")
        yield self.path
        with Container(id="cont02"):
            self.select = Select((), id="select_file")
            yield self.select
            # Select para idiomas
            self.language = Select(((lang, lang) for lang in Languages), id="select_lang")
            yield self.language
        with Horizontal(id="cont03"):
            self.button_extrair = Button("Extrair Texto", variant="success", id="b_extrair")
            yield self.button_extrair
            self.button_exibir = Button("Exibir Imagem", variant="warning", id="b_exibir")
            yield self.button_exibir
        self.content_label = Label(id="label_content")
        self.content = None
        with ScrollableContainer(): 
            yield self.content_label
        yield Footer()

    def on_input_changed(self, event):
        self.label.update(f'[red bold]Diretório:[/] {event.input.value}')

    def on_input_submitted(self, event):
        files = os.listdir(event.input.value)
        file_tuples = [(file_name, file_name) for file_name in files]
        self.select.set_options(file_tuples)


    @on(Select.Changed, "#select_file")
    def print_something(self, event):
        selected_file = event.value
        directory_path = self.path.value.strip()
        self.file_path = os.path.join(directory_path, selected_file)
        self.label.update(f'[green bold]Arquivo:[/] {self.file_path}')

    @on(Select.Changed, "#select_lang")
    def print_label(self, event):
        self.language_label.update(f'[blue bold]Idioma:[/] {event.value}')

    @on(Button.Pressed, "#b_extrair")    
    def on_button_pressed(self, event):
        self.content = self.controller.extract_text(self.file_path, self.language.value)
        self.content_label.update(self.content)

    @on(Button.Pressed, "#b_exibir")
    def act_something(self, event): 
        if self.file_path.endswith('.jpg') or self.file_path.endswith('.png'):
            self.controller.show_image(self.file_path)
