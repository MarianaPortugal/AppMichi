from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from logic.video_manager import load_progress
from logic.upload_manager import upload_comprovacao, get_upload_stats
from widgets.scalable_image import ScalableImage  # IMPORTAÇÃO ADICIONADA
import os

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.michi_feliz = False
        
    def on_enter(self):
        if self.michi_feliz:
            self.reset_michi()
        self.atualizar_progresso_rapido()
    
    def atualizar_progresso_rapido(self):
        try:
            progress = load_progress()
            videos_path = "assets/vídeos"
            total_videos = 0
            if os.path.exists(videos_path):
                total_videos = len([f for f in os.listdir(videos_path) 
                                 if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))])
            self.ids.progresso_rapido.text = f"Progresso: {progress}/{total_videos} vídeos"
        except:
            self.ids.progresso_rapido.text = "Progresso: --/-- vídeos"
    
    def mostrar_ajuda(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        ajuda_texto = """🎯 Como usar o Michi App:

1. Clique em "Escolher Tema" para ver os temas disponíveis
2. Assista aos vídeos em ordem
3. Envie uma comprovação após assistir
4. Desbloqueie novos conteúdos!

💡 Dicas:
• Vídeos são desbloqueados gradualmente
• Suas comprovações ficam salvas
• Acompanhe seu progresso na tela de estatísticas"""
        
        content.add_widget(Label(
            text=ajuda_texto,
            text_size=(None, None),
            halign='left',
            valign='top'
        ))
        
        btn_fechar = Button(
            text='Entendi!',
            size_hint_y=None,
            height='40dp'
        )
        
        popup = Popup(
            title='Como usar o Michi App',
            content=content,
            size_hint=(0.8, 0.7)
        )
        
        btn_fechar.bind(on_press=popup.dismiss)
        content.add_widget(btn_fechar)
        popup.open()
    
    def ir_para_temas(self):
        self.manager.current = 'temas'
    
    def enviar_comprovante(self):
        sucesso = upload_comprovacao()
        if sucesso:
            self.celebrar_sucesso()
            self.show_popup("Comprovante Enviado", 
                          "Comprovação enviada com sucesso!\nPróximo vídeo liberado! 🎥")
        else:
            self.show_popup("Cancelado", "Envio cancelado.")
    
    def celebrar_sucesso(self):
        self.ids.michi_image.source = "assets/imagens/michi_feliz.png"
        self.ids.welcome_label.text = "Você arrasou! Missão cumprida! 🐾"
        self.michi_feliz = True

        # Animação em sequência usando a propriedade scale
        anim1 = Animation(scale=1.3, duration=0.2)
        anim2 = Animation(scale=0.9, duration=0.2) 
        anim3 = Animation(scale=1.1, duration=0.2)
        anim4 = Animation(scale=1.0, duration=0.2)
        anim_sequence = anim1 + anim2 + anim3 + anim4
        anim_sequence.start(self.ids.michi_image)
        
        Clock.schedule_once(lambda dt: self.atualizar_progresso_rapido(), 0.5)
    
    def reset_michi(self):
        self.ids.michi_image.source = "assets/imagens/michi.png"
        self.ids.welcome_label.text = "Olá! Eu sou o Michi! Vamos começar uma nova aventura?"
        self.michi_feliz = False
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

