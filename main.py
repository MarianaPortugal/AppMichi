from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from screens import AVAILABLE_SCREENS, SCREEN_TRANSITIONS
from screens.perfil_screen import PerfilScreen
from logic import check_system_requirements, get_app_info

class MichiApp(App):
    def build(self):
        # Verifica requisitos do sistema
        self.check_requirements()
        
        # Carrega os arquivos KV
        self.load_kv_files()
        
        # Cria o gerenciador de telas
        sm = ScreenManager()
        
        # Adiciona as telas registradas
        for screen_name, screen_class in AVAILABLE_SCREENS:
            sm.add_widget(screen_class(name=screen_name))
        
        # Define a tela inicial
        sm.current = 'perfil'

        Logger.info("MichiApp: Aplicação iniciada com sucesso")
        return sm
    
    def load_kv_files(self):
        """Carrega todos os arquivos .kv necessários"""
        kv_files = [
            'kv_files/perfil.kv',     # <-- ADICIONADO AQUI
            'kv_files/home.kv',
            'kv_files/temas.kv',
            'kv_files/desafio.kv',
            'kv_files/progresso.kv'
        ]
        
        for kv_file in kv_files:
            try:
                Builder.load_file(kv_file)
                Logger.info(f"MichiApp: Arquivo KV carregado: {kv_file}")
            except Exception as e:
                Logger.error(f"MichiApp: Erro ao carregar {kv_file}: {e}")
    
    def check_requirements(self):
        """Verifica se todos os requisitos estão atendidos"""
        requirements = check_system_requirements()
        issues = []
        
        if not requirements['kivy_available']:
            issues.append("Kivy não está instalado")
        if not requirements['pillow_available']:
            issues.append("Pillow não está instalado")
        if not requirements['platform_supported']:
            issues.append("Plataforma não suportada")
        if not requirements['video_directory_exists']:
            issues.append("Diretório de vídeos não encontrado")
        if not requirements['writable_data_directory']:
            issues.append("Não foi possível criar diretório de dados")
        
        if issues:
            Logger.warning(f"MichiApp: Problemas encontrados: {issues}")
            # self.show_requirements_popup(issues)  # opcional
    
    def show_requirements_popup(self, issues):
        """Exibe um popup com problemas de requisitos"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(
            text="Problemas encontrados:",
            size_hint_y=None,
            height='30dp'
        ))
        
        for issue in issues:
            content.add_widget(Label(
                text=f"• {issue}",
                size_hint_y=None,
                height='25dp',
                halign='left'
            ))
        
        btn_ok = Button(
            text='Continuar mesmo assim',
            size_hint_y=None,
            height='40dp'
        )
        
        popup = Popup(
            title='Verificação do Sistema',
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.open()
    
    def on_start(self):
        app_info = get_app_info()
        Logger.info(f"MichiApp: {app_info['name']} v{app_info['version']} iniciado")
    
    def on_stop(self):
        Logger.info("MichiApp: Aplicação finalizada")

if __name__ == '__main__':
    MichiApp().run()
