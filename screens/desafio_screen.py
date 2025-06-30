from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from logic.video_manager import load_progress
import os

class DesafioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tema_atual = None
        self.tema_info = None
    
    def configurar_tema(self, tema_nome, tema_info):
        self.tema_atual = tema_nome
        self.tema_info = tema_info
        self.ids.title_label.text = f"Desafios: {tema_nome}"
        self.gerar_botoes_desafios()
    
    def gerar_botoes_desafios(self):
        # Limpa botões existentes
        self.ids.desafios_container.clear_widgets()
        
        progress = load_progress()
        total_desafios = self.tema_info.get("total_videos", 3)
        
        for i in range(total_desafios):
            if i <= progress:
                # Desafio disponível
                btn = Button(
                    text=f"Desafio {i + 1} - Assistir 🎥",
                    size_hint_y=None,
                    height='48dp',
                    background_color=self.tema_info["cor"]
                )
                btn.bind(on_press=lambda x, idx=i: self.abrir_video(idx))
            else:
                # Desafio bloqueado
                btn = Button(
                    text=f"Desafio {i + 1} - Bloqueado 🔒",
                    size_hint_y=None,
                    height='48dp',
                    background_color=[0.5, 0.5, 0.5, 1],
                    disabled=True
                )
                btn.bind(on_press=lambda x: self.mostrar_bloqueado())
            
            self.ids.desafios_container.add_widget(btn)
    
    
    def mostrar_bloqueado(self):
        self.show_popup("Bloqueado", "Conclua os desafios anteriores para desbloquear! 🔐")
    
    def voltar_temas(self):
        self.manager.current = 'temas'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()