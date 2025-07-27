@echo off
echo ========================================
echo Configurando API CRUD de Vagas - FastAPI
echo ========================================

echo.
echo 1. Criando ambiente virtual...
python -m venv venv

echo.
echo 2. Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 3. Instalando dependencias...
pip install -r requirements.txt

echo.
echo 4. Configuracao concluida!
echo.
echo Para ativar o ambiente virtual manualmente:
echo venv\Scripts\activate.bat
echo.
echo Para executar a aplicacao:
echo uvicorn main:app --reload
echo.
echo Para executar os testes:
echo pytest
echo.
pause 