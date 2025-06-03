import tkinter as tk
from tkinter import messagebox
from logic.video_manager import get_next_video, load_progress
import os

class DesafioPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tema = "Animais"  # valor temporário
        self.setup_ui()

    def setup_ui(self):
        self.title_label = tk.Label(self, text="Desafios: Animais 🐾", font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        self.gerar_botoes_atividade()

        btn_voltar = tk.Button(self, text="Voltar", command=lambda: self.controller.show_frame("TemasPage"))
        btn_voltar.pack(pady=20)

    def gerar_botoes_atividade(self):
        progress = load_progress()

        for i in range(3):  # Suponhamos 3 vídeos por tema
            if i <= progress:
                text = f"Desafio {i + 1} - Assistir 🎥"
                command = lambda i=i: self.abrir_video(i)
            else:
                text = f"Desafio {i + 1} - Bloqueado 🔒"
                command = lambda: messagebox.showinfo("Bloqueado", "Conclua os desafios anteriores.")

            btn = tk.Button(self.buttons_frame, text=text, width=25, command=command)
            btn.pack(pady=5)

    def abrir_video(self, index):
        video_path = get_next_video()
        if video_path:
            os.startfile(video_path)
        else:
            messagebox.showinfo("Concluído", "Todos os vídeos foram assistidos.")
