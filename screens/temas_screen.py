
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from logic.video_manager import get_videos_for_theme, mark_watched, mark_submitted
import os

class TemasScreen(Screen):
    tema_atual = None

    def on_enter(self):
        self.ids.tema_layout.clear_widgets()

    def carregar_videos(self, tema):
        self.tema_atual = tema
        layout = self.ids.tema_layout
        layout.clear_widgets()
        videos = get_videos_for_theme(tema)

        for video in videos:
            btn = Button(
                text=f"{video['name']} {'✅' if video['submitted'] else ''}",
                size_hint_y=None,
                height=60,
                font_size=18,
                background_color=(0.3, 0.6, 0.9, 1) if video['unlocked'] else (0.6, 0.6, 0.6, 1),
                disabled=not video['unlocked'],
                on_press=lambda instance, v=video: self.assistir_video(tema, v)
            )
            layout.add_widget(btn)

    def assistir_video(self, tema, video):
        os.system(f'start "" "{video["file"]}"' if os.name == 'nt' else f'xdg-open "{video["file"]}"')
        mark_watched(tema, video["name"])

    def submeter_atividade(self):
        if not self.tema_atual:
            return

        layout = self.ids.tema_layout
        botoes = layout.children
        if not botoes:
            return

        for btn in reversed(botoes):
            if "✅" not in btn.text and not btn.disabled:
                video_name = btn.text.strip()
                mark_submitted(self.tema_atual, video_name)
                self.show_congratulations()
                self.carregar_videos(self.tema_atual)
                break

    def show_congratulations(self):
        popup = Popup(
            title="Parabéns!",
            content=Label(text="Você concluiu a atividade! 🎉", font_size=20),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
