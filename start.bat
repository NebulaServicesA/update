@echo off
title Auto GitHub Full Reset Push
color 0a

cd /d "%~dp0"

set repo=https://github.com/NebulaServicesA/update.git

if exist ".git" (
    rmdir /s /q ".git"
)

git init

git branch -M main

git remote add origin %repo%

git add .

git commit -m "auto update"

git push -u origin main --force

echo.
echo Done.
pause