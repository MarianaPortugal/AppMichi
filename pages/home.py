import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from logic.video_manager import get_next_video
from logic.upload_manager import upload_comprovacao
import os

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_img = None
        self.welcome = None
        self.setup_ui()

    def setup_ui(self):
        # Michi inicial
        img_path = "assets/imagens/michi.png"
        self.michi_photo = ImageTk.PhotoImage(Image.open(img_path).resize((150, 150)))
        self.label_img = tk.Label(self, image=self.michi_photo)
        self.label_img.image = self.michi_photo
        self.label_img.pack(pady=10)

        # Mensagem do Michi
        self.welcome = tk.Label(self, text="Olá! Eu sou o Michi! Vamos começar uma nova aventura?")
        self.welcome.pack()

        # Botão para escolher tema
        btn_temas = tk.Button(self, text="Escolher Tema", command=lambda: self.controller.show_frame("TemasPage"))
        btn_temas.pack(pady=5)


        # Botão de vídeo
        btn_video = tk.Button(self, text="Assistir vídeo", command=self.abrir_video)
        btn_video.pack(pady=10)

        # Botão de envio
        btn_upload = tk.Button(self, text="Enviar Comprovação", command=self.enviar_comprovante)
        btn_upload.pack(pady=5)

    def abrir_video(self):
        video_path = get_next_video()
        if video_path:
            os.startfile(video_path)  # funciona no Windows
        else:
            messagebox.showinfo("Parabéns!", "Você já concluiu todos os vídeos!")

    def enviar_comprovante(self):
        sucesso = upload_comprovacao()
        if sucesso:
            # troca imagem
            feliz_path = "assets/imagens/michi_feliz.png"
            self.michi_photo = ImageTk.PhotoImage(Image.open(feliz_path).resize((150, 150)))
            self.label_img.configure(image=self.michi_photo)
            self.label_img.image = self.michi_photo

            # muda mensagem
            self.welcome.config(text="Você arrasou! Missão cumprida! 🐾")

            messagebox.showinfo("Comprovante Enviado", "Comprovação enviada com sucesso! Próximo vídeo liberado.")
        else:
            messagebox.showwarning("Cancelado", "Envio cancelado.")
