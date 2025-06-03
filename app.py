import tkinter as tk
from pages.home import HomePage
from pages.temas import TemasPage
from pages.desafio import DesafioPage


class MichiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Michi App")
        self.geometry("500x600")
        self.resizable(False, False)

        self.frames = {}

        for PageClass in (HomePage, TemasPage, DesafioPage):  # futuramente adicionamos outras aqui
            page_name = PageClass.__name__
            frame = PageClass(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MichiApp()
    app.mainloop()
