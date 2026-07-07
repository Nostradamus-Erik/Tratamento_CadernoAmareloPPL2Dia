@echo off
echo. && ^
echo Oi, aqui fala o professor Alexandre pelo Windows && ^
echo Nao se sinta sozinho(a), eu estou no computador com voce && ^
echo. && ^
echo. && ^
echo vou CRIAR o ambiente virtual na pasta de nivel anterior && ^
python -m venv ..\venv && ^
echo PRONTO! && ^
echo. && ^
echo. && ^
echo agora vou ATIVAR o ambiente virtual && ^
call ..\venv\Scripts\activate.bat && ^
echo PRONTO! && ^
echo. && ^
echo. && ^
echo vou conferir se o pip3 esta atualizado, um passo importante no Windows && ^
python -m pip install --upgrade pip && ^
echo PRONTO! && ^
echo. && ^
echo. && ^
echo finalmente, eu vou INSTALAR a biblioteca pdf2image && ^
echo. && ^
pip3 install pdf2image && ^
echo. && ^
echo PRONTO! && ^
echo. && ^
echo. && ^
echo vou dar um git config --list para vc conferir: && ^
echo - seu user.email && ^
echo - seu user.name && ^
echo - se está no SEU repositórios mesmo conferindo a variável remote.origin.url && ^
echo. && ^
git config --list && ^
echo. && ^
echo. && ^
echo ==> CONFIRA <== se está tudo certo no seu user.email, user.name, remote.origin.url && ^
echo se estiver tudo certo, pode codar. Boa sorte! && ^
echo. && ^
echo. && ^
echo se precisar arrumar o user.email, use o comando: && ^  
echo git config --global user.email "seu.email@exemplo.com" && ^
echo. && ^
echo. && ^
echo se precisar arrumar o user.name, use o comando: && ^
echo git config --global user.name "Seu Nome" && ^
echo. && ^
echo. && ^
echo confira se o remote.origin.url está mostrando o link do SEU repositório: && ^
echo. && ^
echo. && ^
echo lembre-se de conferir as credenciais no Gerenciados de Credenciais && ^
echo.