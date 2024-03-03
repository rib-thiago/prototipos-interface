from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Select
import os

class ShowContentApp(App):
    def compose(self) -> ComposeResult:
        self.label = Label()
        yield self.label
        self.path = Input(placeholder="Path do Diretório", type="text")
        yield self.path
        self.select = Select(())
        yield self.select
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
            file_path = os.path.join(directory_path, selected_file)
            self.label.update(f'[red bold]Diretório:[/] {file_path}')
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
                    self.content_label.update(content)
            else:
                self.content_label.update("Arquivo não encontrado.")

if __name__ == "__main__":
    app = ShowContentApp()
    app.run()
