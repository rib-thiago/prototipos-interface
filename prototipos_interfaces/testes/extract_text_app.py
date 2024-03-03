from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Button


class ExtractTextApp(App): 
    
    BINDINGS = [("d", "toggle_dark", "Mudar Tema"), ("q", "quit", "Sair")]
                
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("Extrair Imagens de Arquivos")
        yield Button("Upload de Arquivo", variant="primary")
        yield Button("Caminho para Diretório", variant="error") 
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    app = ExtractTextApp()
    app.run()