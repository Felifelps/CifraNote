@echo off
cd %__CD__% 
git init
git add .
set /p commit=Enter Commit: 
git commit -m "%commit%"
git config --global user.name Felifelps
git config --global user.email felipefelipe23456@gmail.com
git push https://github.com/Felifelps/CifraNote 
echo Salvo
pause