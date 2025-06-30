
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from logic.video_manager import load_progress
from datetime import datetime

class ProgressoScreen(Screen):
    def on_pre_enter(self):
        self.ids.progresso_layout.clear_widgets()
        progresso = load_progress()

        for tema, videos in progresso.items():
            self.ids.progresso_layout.add_widget(Label(
                text=f"[b]{tema.upper()}[/b]", markup=True, font_size=18, size_hint_y=None, height=30
            ))
            for nome, status in videos.items():
                texto = f"{nome} - {'✅ Assistido' if status['watched'] else '❌ Não assistido'} / "
                texto += f"{'📤 Enviado' if status['submitted'] else '⏳ Pendente'}"
                self.ids.progresso_layout.add_widget(Label(
                    text=texto, font_size=16, size_hint_y=None, height=25
                ))

    def verificar_senha(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        input_box = TextInput(password=True, multiline=False)
        layout.add_widget(Label(text="Digite a senha de acesso:", font_size=16))
        layout.add_widget(input_box)

        def autenticar(instance):
            if input_box.text == "1234":
                self.manager.current = 'progresso'
                popup.dismiss()
            else:
                popup.content = Label(text="Senha incorreta!")

        btn = Button(text="Acessar", size_hint_y=None, height=40, on_press=autenticar)
        layout.add_widget(btn)

        popup = Popup(title="Área dos Pais", content=layout, size_hint=(None, None), size=(400, 250))
        popup.open()
