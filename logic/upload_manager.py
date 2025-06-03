import os
import shutil
from tkinter import filedialog
from logic.video_manager import load_progress, save_progress


UPLOADS_PATH = "uploads"

def upload_comprovacao():
    # Abre janela para escolher o arquivo
    file_path = filedialog.askopenfilename(title="Selecione o arquivo de comprovação")

    if not file_path:
        return False  # Cancelado

    # Garante que a pasta de uploads exista
    os.makedirs(UPLOADS_PATH, exist_ok=True)

    # Gera nome do arquivo baseado no índice do vídeo atual
    index = load_progress()
    filename = f"comprovacao_video{index + 1}" + os.path.splitext(file_path)[-1]
    dest_path = os.path.join(UPLOADS_PATH, filename)

    # Copia o arquivo
    shutil.copy(file_path, dest_path)

    # Atualiza progresso para liberar próximo vídeo
    save_progress(index + 1)
    return True
