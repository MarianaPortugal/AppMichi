from .video_manager import *
from .upload_manager import *

def check_system_requirements():
    # Verificação básica (placeholder)
    return {
        'kivy_available': True,
        'pillow_available': True,
        'platform_supported': True,
        'video_directory_exists': True,
        'writable_data_directory': True
    }

def get_app_info():
    return {
        'name': 'Michi App',
        'version': '2.0',
        'author': 'Grupo 7'
    }
