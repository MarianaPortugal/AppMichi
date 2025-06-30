import os
import shutil
from datetime import datetime
from kivy.utils import platform
from kivy.logger import Logger
from logic.video_manager import load_progress, save_progress

if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
    except ImportError:
        Logger.warning("UploadManager: Módulos Android não disponíveis")
elif platform == 'win':
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        Logger.warning("UploadManager: tkinter não disponível no Windows")
else:
    import subprocess

UPLOADS_PATH = "uploads"

SUPPORTED_FORMATS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
    'videos': ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v'],
    'others': ['.zip', '.rar', '.7z']
}


def get_all_supported_extensions():
    all_extensions = []
    for category in SUPPORTED_FORMATS.values():
        all_extensions.extend(category)
    return all_extensions


def upload_comprovacao():
    try:
        Logger.info("UploadManager: Iniciando processo de upload")

        if platform == 'android':
            return upload_android()
        elif platform == 'win':
            return upload_windows()
        else:
            return upload_linux_mac()

    except Exception as e:
        Logger.error(f"UploadManager: Erro no upload: {e}")
        return False


def upload_windows():
    try:
        Logger.info("UploadManager: Iniciando upload Windows")
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        filetypes = [
            ("Todos os arquivos suportados", " ".join([f"*{ext}" for ext in get_all_supported_extensions()])),
            ("Todos os arquivos", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo de comprovação",
            filetypes=filetypes,
            parent=root
        )

        root.destroy()

        if not file_path:
            Logger.info("UploadManager: Seleção de arquivo cancelada pelo utilizador")
            return False

        Logger.info(f"UploadManager: Arquivo selecionado: {file_path}")
        return process_file_selection(file_path)

    except Exception as e:
        Logger.error(f"UploadManager: Erro Windows: {e}")
        return False


def validate_file_type(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()
    supported_extensions = get_all_supported_extensions()

    is_supported = file_extension in supported_extensions

    if is_supported:
        Logger.info(f"UploadManager: Tipo de arquivo válido: {file_extension}")
    else:
        Logger.warning(f"UploadManager: Tipo de arquivo não suportado: {file_extension}")

    return is_supported


def process_file_selection(file_path):
    if not file_path or not os.path.exists(file_path):
        Logger.error(f"UploadManager: Arquivo inválido: {file_path}")
        return False

    try:
        if not validate_file_type(file_path):
            Logger.error(f"UploadManager: Tipo de arquivo não suportado: {file_path}")
            return False

        file_size = os.path.getsize(file_path)
        max_size = 50 * 1024 * 1024

        if file_size > max_size:
            Logger.error(f"UploadManager: Arquivo muito grande: {file_size/1024/1024:.1f}MB (máximo 50MB)")
            return False

        os.makedirs(UPLOADS_PATH, exist_ok=True)

        file_extension = os.path.splitext(file_path)[-1].lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 🔍 Detectar tema e vídeo a partir do nome do arquivo, ex: "cores_2.mp4"
        filename_original = os.path.basename(file_path)
        base_name, _ = os.path.splitext(filename_original)
        if "_" not in base_name:
            Logger.error("UploadManager: Nome de vídeo inválido. Esperado formato tema_indice (ex: cores_2)")
            return False

        theme, indice = base_name.split("_", 1)
        video_key = f"{theme}_{indice}"
        filename = f"comprovacao_{video_key}_{timestamp}{file_extension}"
        dest_path = os.path.join(UPLOADS_PATH, filename)

        shutil.copy2(file_path, dest_path)

        if not os.path.exists(dest_path):
            Logger.error("UploadManager: Falha na cópia do arquivo")
            return False

        # ✅ Atualiza progresso corretamente
        progress = load_progress()
        if theme not in progress:
            progress[theme] = {}
        if video_key not in progress[theme]:
            progress[theme][video_key] = {"watched": False, "submitted": False}
        progress[theme][video_key]["submitted"] = True
        save_progress(progress)

        Logger.info(f"UploadManager: Arquivo processado com sucesso: {dest_path}")
        Logger.info(f"UploadManager: Progresso atualizado: {theme} - {video_key}")

        return True

    except Exception as e:
        Logger.error(f"UploadManager: Erro ao processar arquivo: {e}")
        return False


def get_upload_stats():
    try:
        comprovacoes = os.listdir(UPLOADS_PATH) if os.path.exists(UPLOADS_PATH) else []

        arquivos = []
        for nome in comprovacoes:
            caminho = os.path.join(UPLOADS_PATH, nome)
            if os.path.isfile(caminho):
                tamanho = os.path.getsize(caminho)
                arquivos.append({
                    'nome': nome,
                    'tamanho_bytes': tamanho,
                    'tamanho_mb': round(tamanho / (1024 * 1024), 2),
                    'extensao': os.path.splitext(nome)[1].lower()
                })

        if not arquivos:
            return {
                'total_arquivos': 0,
                'tamanho_total_mb': 0,
                'tipos_arquivo': [],
                'categorias': {},
                'arquivo_maior': None,
                'arquivo_menor': None
            }

        total_arquivos = len(arquivos)
        tamanho_total = sum(a['tamanho_bytes'] for a in arquivos)
        tipos = list(set(a['extensao'] for a in arquivos))
        arquivo_maior = max(arquivos, key=lambda x: x['tamanho_bytes'])
        arquivo_menor = min(arquivos, key=lambda x: x['tamanho_bytes'])

        return {
            'total_arquivos': total_arquivos,
            'tamanho_total_mb': round(tamanho_total / (1024 * 1024), 2),
            'tipos_arquivo': tipos,
            'categorias': {},
            'arquivo_maior': arquivo_maior,
            'arquivo_menor': arquivo_menor
        }

    except Exception as e:
        Logger.error(f"UploadManager: Erro ao calcular estatísticas: {e}")
        return {
            'total_arquivos': 0,
            'tamanho_total_mb': 0,
            'tipos_arquivo': [],
            'categorias': {},
            'arquivo_maior': None,
            'arquivo_menor': None
        }
