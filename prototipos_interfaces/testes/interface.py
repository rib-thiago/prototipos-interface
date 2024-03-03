from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Select, Button, LoadingIndicator
import os
import cv2
import pytesseract

class ShowContentApp(App):
    def compose(self) -> ComposeResult:
        self.label = Label()
        yield self.label
        self.path = Input(placeholder="Path do Diretório", type="text")
        yield self.path
        self.select = Select(())
        yield self.select
        self.button = Button("Extrair Texto", variant="success")
        yield self.button
        self.loading_indicator = LoadingIndicator(disabled=False)  # Adicione o indicador de carregamento
        yield self.loading_indicator
        self.content_label = Label()
        yield self.content_label


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
            self.label.update(f'[red bold]Diretório:[/] {self.file_path}')

    def on_button_pressed(self, event):  # Torne o método assíncrono
        content = extract_text(self.file_path, language='eng')  # Espere a extração do texto
        self.content_label.update(content)



def extract_text(filename, language='eng'):
    
    # Carrega a imagem
    img = cv2.imread(filename)

    # Extrai texto da imagem
    resultado = pytesseract.image_to_string(img, lang=language)

    return resultado


if __name__ == "__main__":
    app = ShowContentApp()
    app.run()
