from .perfil_screen import PerfilScreen
from .home_screen import HomeScreen
from .temas_screen import TemasScreen
from .desafio_screen import DesafioScreen
from .progresso_screen import ProgressoScreen

AVAILABLE_SCREENS = [
    ('perfil', PerfilScreen),
    ('home', HomeScreen),
    ('temas', TemasScreen),
    ('desafio', DesafioScreen),
    ('progresso', ProgressoScreen),
]

SCREEN_TRANSITIONS = {
    'home': {
        'temas': 'slide_left',
        'progresso': 'slide_up'
    },
    'temas': {
        'home': 'slide_right',
        'desafio': 'slide_left'
    }
}

