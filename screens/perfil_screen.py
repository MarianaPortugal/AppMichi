from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App

class PerfilScreen(Screen):
    nome = StringProperty("")

    def on_enter(self):
        pass  # Pode remover se não for usar

    def salvar_nome(self):
        nome = self.ids.nome_input.text.strip()
        if nome:
            app = App.get_running_app()
            app.nome_crianca = nome
            self.manager.current = 'home'
