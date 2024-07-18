# A Classe App

O primeiro passo na construção de um aplicativo com Textual é importar a classe **App** e criar uma subclasse.

Vejamos o exemplo mais simples:

```python
from textual.app import App


class MyApp(App):
    pass
```

## O método run

Para rodar um aplicativo, criamos uma instância e chamamos `run()`

```python
# myapp.py

from textual.app import App


class MyApp(App):
    pass

if __name__ == "__main__":
    app = MyApp()
    app.run()
```
Os aplicativos não podem ser muito mais simples do que isso – não espere que este app faça muita coisa.

> A condição `__name__ = "__main__"` será verdadeira somente se executarmos o arquivo com o comando `python`.
> Isso nos permite importar o aplicativo sem executá-lo imediatamente. Também permite que comando `run` das `devtools`
> execute o aplicativo no modo de desenvolvimento.
> Consulte a documentação do Python para maiores informações.

Se executarmos esse aplicativ com o comando `python myapp.py` veremos um terminal vazio.

Quando chamamos `App.run()` o Textual coloca o terminal em um estado especial chamado *Application Mode*. Quando o terminal se encontra no *application mode* ele não imprime (`echo`) o que o usuário digita. Textual assumirá a resposta à entrada do usuário (teclado e mouse) e atualizará a parte visível do terminal (ou seja, a tela).

Se você pressionar `Ctrl+C` Textual sairá do modo de aplicativo e retornará ao prompt de comando. Qualquer conteúdo que você tinha no terminal antes do modo de aplicativo será restaurado.

## Eventos

Textual possui um sistema de eventos que você pode usar para responder a teclas pressionadas, ações do mouse e mudanças de estado internas. Manipuladores de eventos (*event handlers*) são métodos prefixados com `on_` seguido do nome do evento.

Um desses eventos é o evento `mount` que é enviado a um aplicativo após ele entrar em *application mode*. Você pode responder a este evento definindo um método chamado `on_mount`.

> Você deve ter notado que usamos os termos "enviar" e "enviado" em relação aos métodos manipuladores de eventos em preferência a "chamar". 
> Isso ocorre porque o Textual usa um sistema de passagem de mensagens onde os eventos são passados (ou enviados) entre os componentes. 

Outro evento deste tipo é o evento `key`, que é enviado quando o usuário pressiona uma tecla. O exemplo abaixo contém manipuladores para ambos os eventos:

```python
from textual.app import App
from textual import events


class EventApp(App):

    COLORS = [
        "white",
        "maroon",
        "red",
        "purple",
        "fuchsia",
        "olive",
        "yellow",
        "navy",
        "teal",
        "aqua",
    ]

    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"

    def on_key(self, event: events.Key) -> None:
        if event.key.isdecimal():
            self.screen.styles.background = self.COLORS[int(event.key)]


if __name__ == "__main__":
    app = EventApp()
    app.run()
```

O manipulador `on_mount` define o atributo `self.screen.styles.background` como *darkblue* que torna o fundo azul. Como o evento `mount` é enviado imediatamente após entrarmos no *application mode*, uma tela azul será exibida ao executar esse código.

O manipulador do evento `key` (`on_key`) possui um parâmetro de evento que recebrá uma instância de `key`. Cada evento possui um objeto de evento associado que será passado para o método manipulador se estiver presente na lista de parâmetros do método.

> É incomum (mas não inédito) que os parâmetros de um método afetem a forma como ele é chamado. 
> Textual faz isso inspecionando o método antes de chamá-lo.

Alguns eventos contêm informações adicionais que você pode inspecionar no manipulador. O evento `Key` possui um atributo `key` que é o nome da tecla que foi pressionada. O método `on_key` acima usa este atributo para alterar a cor de fundo se alguma das teclas de 0 a 9 for pressionada.

## Eventos Async

Textual é desenvolvido com a estrutura `asyncio` do Python, que usa as palavras-chave `async` e `await`.

Textual sabe que deve *aguardar (await)* seus manipuladores de eventos se eles forem corrotinas (ou seja, prefixados com a palavra-chave `async`). 

Funções regulares geralmente funcionam bem, a menos que você planeje integrar outras bibliotecas assíncronas (como `httpx` para leitura de dados da Internet).

> Para uma introdução amigável à programação assíncrona em Python, consulte o artigo sobre [*Concurrency and async - await*](https://fastapi.tiangolo.com/async/) do `FastAPI`.

## Widgets

Widgets são componentes independentes responsáveis por gerar a saída para uma parte da tela. Os widgets respondem aos eventos da mesma maneira que o aplicativo. A maioria dos aplicativos que fazem algo interessante conterá pelo menos um (e provavelmente muitos) widgets que juntos formam uma interface de usuário.

Os widgets podem ser tão simples quanto um pedaço de texto, um botão ou um componente completo, como um editor de texto ou navegador de arquivos (que pode conter seus próprios widgets).

### Composição

Para adicionar widgets ao seu aplicativo, implemente um método `compose()` que deve retornar um iterável de instâncias de Widget. Uma lista funcionaria, mas é conveniente gerar (`yield`) widgets, tornando o método um gerador.

O exemplo a seguir importa o widget builtin `Welcome` e o gera em `App.compose()`:

```python
from textual.app import App, ComposeResult
from textual.widgets import Welcome


class WelcomeApp(App):
    def compose(self) -> ComposeResult:
        yield Welcome()

    def on_button_pressed(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
```

Quando este código é executado, o Textual montará o widget `Welcome` que contém conteúdo em markdown e um botão.

Observe o método `on_button_pressed` que trata o evento `Button.Pressed` enviado por um botão contido no widget `Welcome`. O manipulador chama `App.exit()` para sair do aplicativo.

### Montagem

Embora a composição seja a forma preferida de adicionar widgets quando a aplicação é iniciada, às vezes é necessário adcionar novos widgets em resposta a eventos. Você pode fazer isso chamando `mount()` que irá adicionar um novo widget à *User Interface*.

Aqui está um aplicativo que adciona um widget `Welcome` em resposta a qualquer botão pressionado.

```python
from textual.app import App
from textual.widgets import Welcome


class WelcomeApp(App):
    def on_key(self) -> None:
        self.mount(Welcome())

    def on_button_pressed(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
```
Ao executar isso pela primeira vez, você verá uma tela em branco. Pressione qualquer tecla para adicionar o widget `Welcome`. 

Você pode até pressionar uma tecla várias vezes para adicionar vários widgets.