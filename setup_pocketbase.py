"""Prepara PocketBase: campos de usuarios, coleccion de causas, reglas y cuentas iniciales.

Es idempotente: se puede ejecutar varias veces. Lee la configuracion del archivo .env.
"""
import os
import shutil
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

PB_URL = os.getenv("PB_URL", "").rstrip("/")
SU_EMAIL = os.getenv("PB_SUPERUSER_EMAIL", "")
SU_PASS = os.getenv("PB_SUPERUSER_PASSWORD", "")
DEFAULT_PASS = os.getenv("DEFAULT_USER_PASSWORD", "")

if not all([PB_URL, SU_EMAIL, SU_PASS, DEFAULT_PASS]):
    sys.exit("Faltan variables en .env (ver .env.example).")

CUENTAS = [
    ("fiscal", "admin"),
    ("Espostodario", "usuario"),
    ("bufejorge", "usuario"),
    ("cangijuan", "usuario"),
    ("turcoalzabe", "usuario"),
]

ES_ADMIN = '@request.auth.rol = "admin" && @request.auth.activo = true'

REGLAS_USERS = {
    "listRule": f'{ES_ADMIN} || id = @request.auth.id',
    "viewRule": f'{ES_ADMIN} || id = @request.auth.id',
    "createRule": None,   # solo superusuario
    "updateRule": ES_ADMIN,
    "deleteRule": None,   # solo superusuario
    "authRule": "activo = true",
}

REGLAS_CAUSAS = {
    "listRule": f'{ES_ADMIN} || (@request.auth.activo = true && asignado_a = @request.auth.id)',
    "viewRule": f'{ES_ADMIN} || (@request.auth.activo = true && asignado_a = @request.auth.id)',
    "createRule": ES_ADMIN,
    "updateRule": (
        f'{ES_ADMIN} || (@request.auth.activo = true && asignado_a = @request.auth.id'
        ' && @request.body.nombre:isset = false && @request.body.asignado_a:isset = false'
        ' && (@request.body.estado:isset = false || @request.body.estado = "en_redaccion"'
        ' || @request.body.estado = "lista_para_visado"))'
    ),
    "deleteRule": ES_ADMIN,
}


def api(method, path, token=None, **kw):
    headers = {"Authorization": token} if token else {}
    r = requests.request(method, f"{PB_URL}{path}", headers=headers, timeout=20, **kw)
    if not r.ok:
        sys.exit(f"Error {r.status_code} en {method} {path}: {r.text}")
    return r.json() if r.content else {}


def instalar_hooks():
    """Copia los hooks del servidor a pocketbase/pb_hooks (requiere reiniciar PocketBase)."""
    raiz = os.path.dirname(os.path.abspath(__file__))
    origen = os.path.join(raiz, "backend", "pb_hooks")
    destino = os.path.join(raiz, "pocketbase", "pb_hooks")
    if not os.path.isdir(os.path.join(raiz, "pocketbase")):
        return
    os.makedirs(destino, exist_ok=True)
    for nombre in os.listdir(origen):
        shutil.copy2(os.path.join(origen, nombre), os.path.join(destino, nombre))
    print("Hooks copiados a pocketbase/pb_hooks (reiniciá PocketBase si cambiaron).")


def main():
    instalar_hooks()
    token = api(
        "POST", "/api/collections/_superusers/auth-with-password",
        json={"identity": SU_EMAIL, "password": SU_PASS},
    )["token"]

    # --- Coleccion users: campos extra, reglas e identidad por username ---
    users = api("GET", "/api/collections/users", token)
    nombres = {f["name"] for f in users["fields"]}
    nuevos = []
    if "username" not in nombres:
        nuevos.append({"name": "username", "type": "text", "required": True})
    if "rol" not in nombres:
        nuevos.append({
            "name": "rol", "type": "select", "required": True,
            "maxSelect": 1, "values": ["admin", "usuario"],
        })
    if "activo" not in nombres:
        nuevos.append({"name": "activo", "type": "bool"})
    cambios = dict(REGLAS_USERS)
    cambios["fields"] = users["fields"] + nuevos
    indices = [i for i in users.get("indexes", []) if "idx_users_username" not in i]
    indices.append("CREATE UNIQUE INDEX idx_users_username ON users (username)")
    cambios["indexes"] = indices
    pa = users.get("passwordAuth", {})
    pa["enabled"] = True
    pa["identityFields"] = ["username", "email"]
    cambios["passwordAuth"] = pa
    api("PATCH", f"/api/collections/{users['id']}", token, json=cambios)
    print("Coleccion users configurada.")

    # --- Coleccion causas ---
    existentes = {c["name"]: c for c in api("GET", "/api/collections?perPage=200", token)["items"]}
    causas_def = {
        "name": "causas",
        "type": "base",
        "fields": [
            {"name": "nombre", "type": "text", "required": True},
            {"name": "asignado_a", "type": "relation", "collectionId": users["id"],
             "maxSelect": 1, "cascadeDelete": False},
            {"name": "estado", "type": "select", "required": True, "maxSelect": 1,
             "values": ["sin_asignar", "esperando", "en_redaccion",
                        "lista_para_visado", "visada"]},
            {"name": "fecha_asignacion", "type": "date"},
            {"name": "fecha_lista", "type": "date"},
            {"name": "creada", "type": "autodate", "onCreate": True},
            {"name": "actualizada", "type": "autodate", "onCreate": True, "onUpdate": True},
        ],
        **REGLAS_CAUSAS,
    }
    if "causas" in existentes:
        api("PATCH", f"/api/collections/{existentes['causas']['id']}", token, json=causas_def)
    else:
        api("POST", "/api/collections", token, json=causas_def)
    print("Coleccion causas configurada.")

    # --- Cuentas iniciales ---
    for username, rol in CUENTAS:
        res = api("GET", "/api/collections/users/records", token,
                  params={"filter": f'username = "{username}"'})
        datos = {"username": username, "rol": rol, "activo": True, "verified": True,
                 "email": f"{username.lower()}@fiscalia8.local", "emailVisibility": True}
        if res["items"]:
            print(f"Cuenta {username}: ya existe.")
            continue
        datos.update({"password": DEFAULT_PASS, "passwordConfirm": DEFAULT_PASS})
        api("POST", "/api/collections/users/records", token, json=datos)
        print(f"Cuenta {username} ({rol}): creada.")


if __name__ == "__main__":
    main()
