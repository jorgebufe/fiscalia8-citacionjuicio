"""Cliente REST de PocketBase para la aplicacion."""
from datetime import datetime, timezone

import requests

from .config import PB_URL

ESTADOS = {
    "sin_asignar": "Sin asignar",
    "esperando": "Esperando",
    "en_redaccion": "En redacción",
    "lista_para_visado": "Lista para visado",
    "visada": "Visada",
}


class ApiError(Exception):
    pass


def _ahora() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.000Z")


class Cliente:
    def __init__(self):
        self.token = None
        self.usuario = None

    # ---- base ----
    def _req(self, metodo, ruta, **kw):
        headers = {"Authorization": self.token} if self.token else {}
        try:
            r = requests.request(metodo, f"{PB_URL}{ruta}", headers=headers, timeout=15, **kw)
        except requests.RequestException as e:
            raise ApiError(f"No se pudo conectar con el servidor: {e}") from e
        if not r.ok:
            try:
                data = r.json()
                msg = data.get("message", r.text)
                detalle = data.get("data") or {}
                extra = "; ".join(f"{k}: {v.get('message')}" for k, v in detalle.items())
                msg = f"{msg} {extra}".strip()
            except ValueError:
                msg = r.text
            raise ApiError(msg)
        return r.json() if r.content else {}

    # ---- sesion ----
    def login(self, username, password):
        try:
            data = self._req("POST", "/api/collections/users/auth-with-password",
                             json={"identity": username, "password": password})
        except ApiError as e:
            raise ApiError("Usuario o contraseña incorrectos, o cuenta desactivada.") from e
        self.token = data["token"]
        self.usuario = data["record"]
        return self.usuario

    @property
    def es_admin(self):
        return bool(self.usuario) and self.usuario.get("rol") == "admin"

    # ---- causas ----
    def listar_causas(self):
        r = self._req("GET", "/api/collections/causas/records",
                      params={"perPage": 500, "expand": "asignado_a", "sort": "-creada"})
        return r["items"]

    def crear_causa(self, nombre):
        return self._req("POST", "/api/collections/causas/records",
                         json={"nombre": nombre, "estado": "sin_asignar"})

    def asignar(self, causa_id, usuario_id):
        return self._req("PATCH", f"/api/collections/causas/records/{causa_id}",
                         json={"asignado_a": usuario_id, "estado": "esperando",
                               "fecha_asignacion": _ahora(), "fecha_lista": None})

    def cambiar_estado(self, causa_id, estado):
        datos = {"estado": estado}
        if estado == "lista_para_visado":
            datos["fecha_lista"] = _ahora()
        return self._req("PATCH", f"/api/collections/causas/records/{causa_id}", json=datos)

    def eliminar_causa(self, causa_id):
        self._req("DELETE", f"/api/collections/causas/records/{causa_id}")

    # ---- cuentas (admin) ----
    def listar_cuentas(self):
        r = self._req("GET", "/api/collections/users/records",
                      params={"perPage": 200, "sort": "username"})
        return r["items"]

    def set_activo(self, usuario_id, activo):
        return self._req("PATCH", f"/api/collections/users/records/{usuario_id}",
                         json={"activo": bool(activo)})

    def resetear_password(self, usuario_id, nueva):
        return self._req("POST", "/api/fiscalia/reset-password",
                         json={"usuario": usuario_id, "password": nueva})
