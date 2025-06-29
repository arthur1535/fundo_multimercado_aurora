# Script PowerShell para upload do Projeto Aurora
Write-Host "===========================================" -ForegroundColor Green
Write-Host "CONFIGURANDO PROJETO FUNDO AURORA" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Navegar para o diretório
Set-Location "d:\onedrive\OneDrive - Universidade Federal de Uberlândia\codar\curso\testecdi"

# Abortar merge se existir
Write-Host "Abortando merge pendente..." -ForegroundColor Yellow
git merge --abort 2>$null

# Verificar status
Write-Host "Status atual do repositório:" -ForegroundColor Cyan
git status

# Remover remote antigo e adicionar novo
Write-Host "Configurando novo repositório remoto..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/arthur1535/fundo_multimercado_aurora.git

# Verificar remotes
Write-Host "Remotes configurados:" -ForegroundColor Cyan
git remote -v

# Fazer push forçado
Write-Host "Enviando projeto para GitHub..." -ForegroundColor Yellow
git push -u origin main --force

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "PROJETO FUNDO AURORA ENVIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Acesse: https://github.com/arthur1535/fundo_multimercado_aurora" -ForegroundColor Cyan
Write-Host ""
