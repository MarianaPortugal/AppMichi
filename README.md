# Michi App 🎥🐾

Michi App é uma aplicação educativa interativa construída com Python e Kivy, com o objetivo de estimular o aprendizado por meio de vídeos e recompensas visuais.

## 🚀 Funcionalidades

- Escolha de temas com vídeos educativos
- Acompanhamento de progresso por tema
- Envio de comprovação após assistir aos vídeos (por imagem)
- Desbloqueio gradual de novos conteúdos
- Interface amigável com mascote Michi

## 📂 Estrutura de Pastas

```
appmichi_final_corrigido/
├── assets/
│   ├── vídeos/               # Vídeos educativos
│   └── imagens/              # Imagens do app (michi, plano de fundo)
├── data/
│   └── progress.json         # Registro de progresso por usuário/tema
├── kv_files/                 # Telas definidas em arquivos .kv
├── logic/                    # Lógica do app (vídeos, uploads)
├── screens/                  # Telas gerenciadas no Kivy
├── uploads/                  # Imagens de comprovação enviadas
├── main.py                   # Ponto de entrada principal
└── README.md / README.txt    # Instruções e explicações do projeto
```

## 🧠 Explicação das Principais Classes

- `main.py` – ponto de entrada da aplicação, inicializa a navegação e carrega as telas.
- `home_screen.py` – lógica da tela inicial com o mascote Michi, botão de ajuda e envio de comprovação.
- `video_manager.py` – responsável por carregar e atualizar o progresso assistido de vídeos.
- `upload_manager.py` – permite o envio de imagens como comprovação e atualiza o progresso correspondente.
- `progresso_screen.py` – apresenta o progresso por tema e controla o acesso por senha.
- `temas_screen.py` – apresenta os temas disponíveis e vídeos relacionados.

## ✅ Como usar

1. Execute com: `python main.py`
2. Escolha seu perfil ou crie um novo.
3. Selecione um tema e assista ao vídeo disponível.
4. Envie uma imagem como comprovação (ex: print assistindo ao vídeo).
5. Desbloqueie o próximo vídeo e acompanhe seu progresso!

## 🔐 Observações

- A tela de progresso requer senha (padrão: `admin`).
- Os nomes dos arquivos de comprovação devem seguir o padrão: `tema_indice.png` (ex: `cores_1.png`).

## 🛠 Requisitos

- Python 3.8+
- Kivy 2.3+
