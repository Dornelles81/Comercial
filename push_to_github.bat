@echo off
echo ========================================
echo ENVIAR PROJETO PARA O GITHUB
echo ========================================
echo.

REM Definir o nome do repositorio
set REPO_NAME=dashboard-comercial

echo 1. Criando repositorio no GitHub...
echo    Acesse: https://github.com/new
echo    Nome sugerido: %REPO_NAME%
echo.
echo 2. Aguardando voce criar o repositorio...
echo    Pressione qualquer tecla apos criar o repositorio no GitHub
pause > nul

echo.
set /p GITHUB_USER="Digite seu usuario do GitHub: "

echo.
echo 3. Configurando remote...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo 4. Enviando para o GitHub...
git push -u origin master

echo.
echo ========================================
echo CONCLUIDO!
echo ========================================
echo.
echo Seu projeto esta em:
echo https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
pause
