from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Select, Button, Header, Footer
from textual.containers import ScrollableContainer, Container
import os
import cv2
import pytesseract

class ShowContentApp(App):
    # Defina o caminho para o arquivo CSS
    CSS_PATH = "hello.css"
    BINDINGS = [("q", "quit", "Sair")]
    
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
            # Crie um ScrollableContainer
            with ScrollableContainer() as container:            
                yield self.content_label
            # Retorne o container
            yield container
        yield Footer()



    def on_input_changed(self, event):
        self.label.update(f'[red bold]Diretório:[/] {event.input.value}')


    def on_input_submitted(self, event):
        # Obtém a lista de arquivos no diretório
        files = os.listdir(event.input.value)
        # Itera sobre os arquivos e gera as tuplas
        file_tuples = [(file_name, file_name) for file_name in files]
        self.select.set_options(file_tuples)

    def on_select_changed(self, event):
            selected_file = event.value
            directory_path = self.path.value.strip()
            self.file_path = os.path.join(directory_path, selected_file)
            self.label.update(f'[green bold]Arquivo:[/] {self.file_path}')

    def on_button_pressed(self, event):
        self.content = extract_text(self.file_path, language='eng')
        self.content_label.update(self.content)


def extract_text(filename, language='eng'):
    
    # Carrega a imagem
    img = cv2.imread(filename)

    # Extrai texto da imagem
    resultado = pytesseract.image_to_string(img, lang=language)

    return resultado


if __name__ == "__main__":
    app = ShowContentApp()
    app.run()
