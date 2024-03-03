# app.py

from textual.app import App
from controller import ShowContentController
from view import ShowContentView

if __name__ == "__main__":
    controller = ShowContentController()
    view = ShowContentView(controller)
    view.run()
