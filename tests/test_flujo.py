"""Prueba de integracion contra un PocketBase ya preparado (setup_pocketbase.py).

Uso: python -m tests.test_flujo
"""
import os

from app.api import ApiError, Cliente

PASS = os.getenv("DEFAULT_USER_PASSWORD", "12345678")


def debe_fallar(fn, *a):
    try:
        fn(*a)
    except ApiError:
        return
    raise AssertionError(f"Se esperaba un rechazo en {fn.__name__}{a}")


def main():
    fiscal = Cliente()
    fiscal.login("fiscal", PASS)
    assert fiscal.es_admin

    ana = Cliente()
    ana.login("bufejorge", PASS)
    assert not ana.es_admin
    otro = Cliente()
    otro.login("cangijuan", PASS)

    # Flujo normal
    causa = fiscal.crear_causa("TEST causa prueba")
    assert causa["estado"] == "sin_asignar"
    cuentas = {u["username"]: u for u in fiscal.listar_cuentas()}
    assert len(cuentas) >= 5
    c = fiscal.asignar(causa["id"], cuentas["bufejorge"]["id"])
    assert c["estado"] == "esperando"
    assert [x["id"] for x in ana.listar_causas()] == [causa["id"]]
    assert otro.listar_causas() == []
    ana.cambiar_estado(causa["id"], "en_redaccion")
    ana.cambiar_estado(causa["id"], "lista_para_visado")
    visto = next(x for x in fiscal.listar_causas() if x["id"] == causa["id"])
    assert visto["estado"] == "lista_para_visado" and visto["fecha_lista"]
    fiscal.cambiar_estado(causa["id"], "visada")

    # Reglas: usuario no puede administrar
    debe_fallar(ana.crear_causa, "x")
    debe_fallar(ana.asignar, causa["id"], cuentas["cangijuan"]["id"])
    debe_fallar(ana.cambiar_estado, causa["id"], "visada")
    debe_fallar(ana.eliminar_causa, causa["id"])
    debe_fallar(otro.cambiar_estado, causa["id"], "en_redaccion")
    visibles = ana.listar_cuentas()
    assert [u["username"] for u in visibles] == ["bufejorge"], visibles
    debe_fallar(ana.set_activo, cuentas["cangijuan"]["id"], False)
    debe_fallar(ana.resetear_password, cuentas["cangijuan"]["id"], "hackeado123")
    debe_fallar(ana.set_activo, ana.usuario["id"], True)  # tampoco la propia

    # Admin: desactivar y resetear
    fiscal.set_activo(cuentas["turcoalzabe"]["id"], False)
    debe_fallar(Cliente().login, "turcoalzabe", PASS)
    fiscal.set_activo(cuentas["turcoalzabe"]["id"], True)
    Cliente().login("turcoalzabe", PASS)
    fiscal.resetear_password(cuentas["turcoalzabe"]["id"], "NuevaClave99")
    debe_fallar(Cliente().login, "turcoalzabe", PASS)
    Cliente().login("turcoalzabe", "NuevaClave99")
    fiscal.resetear_password(cuentas["turcoalzabe"]["id"], PASS)
    Cliente().login("turcoalzabe", PASS)

    fiscal.eliminar_causa(causa["id"])
    print("OK: todas las pruebas pasaron.")


if __name__ == "__main__":
    main()
