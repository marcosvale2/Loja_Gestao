# GestaoLoja - Fonte para gerar .exe (Windows 11 x64)

## O que tem neste zip
- Código-fonte do MVP (Python + PyQt5)
- Instruções para gerar o executável (.exe) no Windows 11 64-bit
- Pasta `static/` com subpastas para fotos/etiquetas/receipts

## Como gerar o .exe no Windows (passo-a-passo resumido)
1. Instale Python 3.10+ (64-bit) e marque "Add Python to PATH".
2. Abra PowerShell/CMD na pasta do projeto.
3. (opcional) Crie e ative um venv:
   python -m venv venv
   venv\Scripts\activate
4. Instale dependências:
   pip install -r requirements.txt
5. Instale PyInstaller:
   pip install pyinstaller
6. Gere o executável (nome: gestaoLoja.exe):
   pyinstaller --noconfirm --onefile --add-data "static;static" --name gestaoLoja app.py
7. Ao final você encontrará o executável em `dist\gestaoLoja.exe`.

Observações importantes:
- Para gerar um executável Windows, é necessário rodar PyInstaller **no Windows**.
- O comando `--add-data` usa separador `;` no Windows. Se usar no Linux, troque por `:`.
- Se quiser ícone, adicione `--icon=meu_icone.ico`.
- PyInstaller já embute o interpretador Python no .exe; o usuário final não precisa ter Python instalado.
# Loja_Gestao
