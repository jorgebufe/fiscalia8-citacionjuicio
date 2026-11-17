"""Configuracion y arranque opcional de PocketBase."""
import os
import subprocess
import sys
import time
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def base_dir() -> str:
    """Carpeta del ejecutable (si esta empaquetado) o raiz del proyecto."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


load_dotenv(os.path.join(base_dir(), ".env"))
PB_URL = os.getenv("PB_URL", "http://127.0.0.1:8090").rstrip("/")


def pb_responde() -> bool:
    try:
        return requests.get(f"{PB_URL}/api/health", timeout=2).ok
    except requests.RequestException:
        return False


def iniciar_pocketbase():
    """Si PB_URL es local y no responde, lanza pocketbase.exe oculto.

    Devuelve el proceso lanzado (o None si no hizo falta / no se pudo).
    """
    if pb_responde():
        return None
    u = urlparse(PB_URL)
    if u.hostname not in ("127.0.0.1", "localhost"):
        return None
    carpeta = os.path.join(base_dir(), "pocketbase")
    exe = os.path.join(carpeta, "pocketbase.exe" if os.name == "nt" else "pocketbase")
    if not os.path.isfile(exe):
        return None
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    proc = subprocess.Popen(
        [exe, "serve", f"--http={u.hostname}:{u.port or 8090}"],
        cwd=carpeta, creationflags=flags,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        if pb_responde():
            break
        time.sleep(0.25)
    return proc
