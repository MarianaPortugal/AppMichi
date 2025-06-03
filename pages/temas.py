import tkinter as tk
from PIL import Image, ImageTk

class TemasPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        img_path = "assets/imagens/michi.png"
        michi_img = Image.open(img_path).resize((120, 120))
        self.michi_photo = ImageTk.PhotoImage(michi_img)
        img_label = tk.Label(self, image=self.michi_photo)
        img_label.pack(pady=10)

        title = tk.Label(self, text="O que vamos aprender hoje?", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        temas = ["Animais 🐶", "Cores 🌈", "Números 🔢"]
        for tema in temas:
            btn = tk.Button(self, text=tema, width=20, command=lambda t=tema: self.ir_para_desafios(t))
            btn.pack(pady=5)

        btn_voltar = tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("HomePage"))
        btn_voltar.pack(pady=20)

    def ir_para_desafios(self, tema_nome):
        desafio_page = self.controller.frames["DesafioPage"]
        desafio_page.tema = tema_nome
        desafio_page.title_label.config(text=f"Desafios: {tema_nome}")
        self.controller.show_frame("DesafioPage")
