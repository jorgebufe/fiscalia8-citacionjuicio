# Genera dist\Fiscalia8\Fiscalia8.exe y copia PocketBase junto al ejecutable.
# Requisitos: pip install -r requirements.txt, carpeta pocketbase/ y .env preparados.
Set-Location $PSScriptRoot

python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name "Fiscalia8" --distpath "dist\Fiscalia8" main.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller fallo" }

# Junto al .exe: PocketBase (con datos y hooks) y un .env que solo contiene la URL.
Copy-Item -Recurse -Force "pocketbase" "dist\Fiscalia8\pocketbase"
$url = (Select-String -Path ".env" -Pattern '^PB_URL=').Line
Set-Content -Path "dist\Fiscalia8\.env" -Value $url -Encoding utf8
Write-Host "Listo: dist\Fiscalia8\Fiscalia8.exe"
