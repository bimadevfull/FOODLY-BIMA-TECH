@echo off
title FOODLY - App de Delivery

echo ========================================
echo     FOODLY - APP DE DELIVERY
echo ========================================
echo. 

echo [1/2] Instalando dependencias...
python -m pip install -q -r requirements.txt

echo. 
echo [2/2] Iniciando aplicativo...
echo.
echo O app abrira automaticamente no navegador! 
echo Pressione Ctrl+C para encerrar.
echo. 

streamlit run app.py

pause