# Genera los dos paquetes de distribucion:
#   dist\Cliente   -> Fiscalia8.exe (+ .env) para cada PC
#   dist\Servidor  -> PocketBase limpio (colecciones, reglas y cuentas) para la PC del fiscal
# Requisitos: pip install -r requirements.txt, carpeta pocketbase/ (solo el .exe se usa) y .env.
Set-Location $PSScriptRoot

# --- Variables del .env ---
$cfg = @{}
Get-Content ".env" | ForEach-Object {
    if ($_ -match '^\s*([A-Z_]+)\s*=\s*(.*)$') { $cfg[$Matches[1]] = $Matches[2].Trim() }
}
foreach ($k in 'PB_SUPERUSER_EMAIL', 'PB_SUPERUSER_PASSWORD', 'DEFAULT_USER_PASSWORD') {
    if (-not $cfg[$k]) { throw "Falta $k en .env" }
}

Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue

# --- Cliente ---
python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name "Fiscalia8" --distpath "dist\Cliente" main.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller fallo" }
Set-Content "dist\Cliente\.env" "PB_URL=http://127.0.0.1:8090" -Encoding ascii
Copy-Item "distribucion\cliente\*" "dist\Cliente\"

# --- Servidor: PocketBase limpio preparado en una carpeta temporal ---
$tmp = Join-Path $env:TEMP "fiscalia8_build_pb"
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
New-Item -ItemType Directory $tmp | Out-Null
Copy-Item "pocketbase\pocketbase.exe" $tmp
Copy-Item -Recurse "backend\pb_hooks" (Join-Path $tmp "pb_hooks")
$pb = Join-Path $tmp "pocketbase.exe"
$datos = Join-Path $tmp "pb_data"
& $pb superuser upsert $cfg['PB_SUPERUSER_EMAIL'] $cfg['PB_SUPERUSER_PASSWORD'] --dir $datos | Out-Null

$proc = Start-Process $pb -ArgumentList 'serve', '--http=127.0.0.1:8091', "--dir=$datos" `
    -WorkingDirectory $tmp -WindowStyle Hidden -PassThru
try {
    $ok = $false
    for ($i = 0; $i -lt 40 -and -not $ok; $i++) {
        Start-Sleep -Milliseconds 500
        try { $ok = (Invoke-WebRequest "http://127.0.0.1:8091/api/health" -UseBasicParsing).StatusCode -eq 200 } catch {}
    }
    if (-not $ok) { throw "PocketBase temporal no inicio" }
    $env:PB_URL = "http://127.0.0.1:8091"
    python setup_pocketbase.py
    if ($LASTEXITCODE -ne 0) { throw "setup_pocketbase.py fallo" }
} finally {
    Remove-Item Env:PB_URL -ErrorAction SilentlyContinue
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

New-Item -ItemType Directory "dist\Servidor" | Out-Null
Copy-Item $pb "dist\Servidor\"
Copy-Item -Recurse (Join-Path $tmp "pb_data") "dist\Servidor\pb_data"
Copy-Item -Recurse (Join-Path $tmp "pb_hooks") "dist\Servidor\pb_hooks"
Copy-Item "distribucion\servidor\*" "dist\Servidor\"
Remove-Item -Recurse -Force $tmp

# --- ZIP listos para llevar en un pendrive + guia ---
Copy-Item "distribucion\GUIA_INSTALACION.txt" "dist\GUIA_INSTALACION.txt"
Compress-Archive -Path "dist\Servidor\*" -DestinationPath "dist\Fiscalia8_Servidor.zip" -Force
Compress-Archive -Path "dist\Cliente\*" -DestinationPath "dist\Fiscalia8_Cliente.zip" -Force

Write-Host "Listo: dist\Fiscalia8_Servidor.zip, dist\Fiscalia8_Cliente.zip y dist\GUIA_INSTALACION.txt"
