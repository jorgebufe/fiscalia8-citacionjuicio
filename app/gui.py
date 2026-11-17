"""Interfaz Tkinter de Fiscalia 8 citacion juicio."""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from .api import ESTADOS, ApiError, Cliente

TITULO = "Fiscalia 8 citacion juicio"
COLORES = {
    "sin_asignar": "#e5e5e5",
    "esperando": "#fff3c4",
    "en_redaccion": "#cfe4ff",
    "lista_para_visado": "#c9f2c7",
    "visada": "#b8b8f0",
}


def fecha(txt):
    return (txt or "")[:16].replace("T", " ")


def tabla(parent, columnas):
    """Crea un Treeview con scrollbar. columnas: [(id, titulo, ancho)]."""
    frame = ttk.Frame(parent)
    tv = ttk.Treeview(frame, columns=[c[0] for c in columnas], show="headings", height=14,
                      selectmode="browse")
    for cid, titulo, ancho in columnas:
        tv.heading(cid, text=titulo)
        tv.column(cid, width=ancho, anchor="w")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    for estado, color in COLORES.items():
        tv.tag_configure(estado, background=color)
    return frame, tv


class Login(ttk.Frame):
    def __init__(self, master, on_ok):
        super().__init__(master, padding=30)
        self.cliente, self.on_ok = Cliente(), on_ok
        ttk.Label(self, text=TITULO, font=("Segoe UI", 16, "bold")).grid(columnspan=2, pady=(0, 20))
        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", pady=4)
        self.u, self.p = tk.StringVar(), tk.StringVar()
        e1 = ttk.Entry(self, textvariable=self.u, width=28)
        e2 = ttk.Entry(self, textvariable=self.p, show="•", width=28)
        e1.grid(row=1, column=1, padx=8)
        e2.grid(row=2, column=1, padx=8)
        ttk.Button(self, text="Ingresar", command=self.entrar).grid(row=3, columnspan=2, pady=16)
        e1.focus()
        for e in (e1, e2):
            e.bind("<Return>", lambda _e: self.entrar())

    def entrar(self):
        try:
            self.cliente.login(self.u.get().strip(), self.p.get())
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
            return
        self.on_ok(self.cliente)


class PanelFiscal(ttk.Frame):
    """Causas: alta, asignacion y visado (rol admin)."""

    def __init__(self, master, cliente):
        super().__init__(master, padding=10)
        self.c = cliente
        self.causas, self.cuentas = [], []

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Label(barra, text="Nueva causa:").pack(side="left")
        self.nombre = tk.StringVar()
        e = ttk.Entry(barra, textvariable=self.nombre, width=40)
        e.pack(side="left", padx=6)
        e.bind("<Return>", lambda _e: self.crear())
        ttk.Button(barra, text="Agregar", command=self.crear).pack(side="left")
        ttk.Button(barra, text="Actualizar", command=self.refrescar).pack(side="right")

        asig = ttk.Frame(self)
        asig.pack(fill="x", pady=(0, 8))
        ttk.Label(asig, text="Asignar causa seleccionada a:").pack(side="left")
        self.destino = ttk.Combobox(asig, state="readonly", width=22)
        self.destino.pack(side="left", padx=6)
        ttk.Button(asig, text="Asignar", command=self.asignar).pack(side="left")
        ttk.Button(asig, text="Marcar visada", command=self.visar).pack(side="left", padx=(20, 0))
        ttk.Button(asig, text="Eliminar", command=self.eliminar).pack(side="right")

        frame, self.tv = tabla(self, [
            ("nombre", "Causa", 300), ("asignado", "Asignada a", 140),
            ("estado", "Estado", 130), ("fasig", "Asignada el", 120), ("flista", "Lista el", 120)])
        frame.pack(fill="both", expand=True)
        self.resumen = ttk.Label(self, text="")
        self.resumen.pack(anchor="w", pady=(6, 0))
        self.refrescar()

    def refrescar(self):
        try:
            self.causas = self.c.listar_causas()
            self.cuentas = [u for u in self.c.listar_cuentas()
                            if u.get("rol") == "usuario" and u.get("activo")]
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
            return
        self.destino["values"] = [u["username"] for u in self.cuentas]
        self.tv.delete(*self.tv.get_children())
        for ca in self.causas:
            quien = (ca.get("expand", {}).get("asignado_a") or {}).get("username", "—")
            self.tv.insert("", "end", iid=ca["id"], tags=(ca["estado"],), values=(
                ca["nombre"], quien, ESTADOS.get(ca["estado"], ca["estado"]),
                fecha(ca.get("fecha_asignacion")), fecha(ca.get("fecha_lista"))))
        listas = sum(1 for ca in self.causas if ca["estado"] == "lista_para_visado")
        self.resumen.config(text=f"{len(self.causas)} causas — {listas} lista(s) para visado")

    def _sel(self):
        s = self.tv.selection()
        if not s:
            messagebox.showinfo(TITULO, "Seleccioná una causa de la lista.")
            return None
        return next(c for c in self.causas if c["id"] == s[0])

    def _run(self, fn, *a):
        try:
            fn(*a)
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
        self.refrescar()

    def crear(self):
        n = self.nombre.get().strip()
        if not n:
            messagebox.showwarning(TITULO, "Ingresá el nombre de la causa.")
            return
        self.nombre.set("")
        self._run(self.c.crear_causa, n)

    def asignar(self):
        ca = self._sel()
        if not ca:
            return
        i = self.destino.current()
        if i < 0:
            messagebox.showwarning(TITULO, "Elegí a quién asignarla.")
            return
        self._run(self.c.asignar, ca["id"], self.cuentas[i]["id"])

    def visar(self):
        ca = self._sel()
        if not ca:
            return
        if ca["estado"] != "lista_para_visado":
            messagebox.showinfo(TITULO, "Solo se puede visar una causa que está 'Lista para visado'.")
            return
        self._run(self.c.cambiar_estado, ca["id"], "visada")

    def eliminar(self):
        ca = self._sel()
        if ca and messagebox.askyesno(TITULO, f"¿Eliminar la causa '{ca['nombre']}'?"):
            self._run(self.c.eliminar_causa, ca["id"])


class PanelUsuario(ttk.Frame):
    """Causas asignadas al usuario."""

    def __init__(self, master, cliente):
        super().__init__(master, padding=10)
        self.c, self.causas = cliente, []
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Button(barra, text="Confirmar recepción (empiezo la redacción)",
                   command=self.recibir).pack(side="left")
        ttk.Button(barra, text="Lista para visado del fiscal",
                   command=self.lista).pack(side="left", padx=8)
        ttk.Button(barra, text="Actualizar", command=self.refrescar).pack(side="right")
        frame, self.tv = tabla(self, [
            ("nombre", "Causa", 330), ("estado", "Estado", 150),
            ("fasig", "Asignada el", 130), ("flista", "Lista el", 130)])
        frame.pack(fill="both", expand=True)
        self.aviso = ttk.Label(self, text="")
        self.aviso.pack(anchor="w", pady=(6, 0))
        self.refrescar()

    def refrescar(self):
        try:
            self.causas = self.c.listar_causas()
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
            return
        self.tv.delete(*self.tv.get_children())
        for ca in self.causas:
            self.tv.insert("", "end", iid=ca["id"], tags=(ca["estado"],), values=(
                ca["nombre"], ESTADOS.get(ca["estado"], ca["estado"]),
                fecha(ca.get("fecha_asignacion")), fecha(ca.get("fecha_lista"))))
        nuevas = sum(1 for ca in self.causas if ca["estado"] == "esperando")
        self.aviso.config(text=f"Tenés {nuevas} causa(s) nueva(s) esperando tu confirmación."
                          if nuevas else "No tenés causas nuevas.")

    def _cambiar(self, desde, hasta, msg):
        s = self.tv.selection()
        if not s:
            messagebox.showinfo(TITULO, "Seleccioná una causa de la lista.")
            return
        ca = next(c for c in self.causas if c["id"] == s[0])
        if ca["estado"] != desde:
            messagebox.showinfo(TITULO, msg)
            return
        try:
            self.c.cambiar_estado(ca["id"], hasta)
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
        self.refrescar()

    def recibir(self):
        self._cambiar("esperando", "en_redaccion", "Solo podés confirmar causas en estado 'Esperando'.")

    def lista(self):
        self._cambiar("en_redaccion", "lista_para_visado",
                      "Primero confirmá la recepción (estado 'En redacción').")


class PanelCuentas(ttk.Frame):
    """Administracion de cuentas (solo admin)."""

    def __init__(self, master, cliente):
        super().__init__(master, padding=10)
        self.c, self.cuentas = cliente, []
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Button(barra, text="Activar / Desactivar", command=self.alternar).pack(side="left")
        ttk.Button(barra, text="Resetear contraseña", command=self.resetear).pack(side="left", padx=8)
        ttk.Button(barra, text="Actualizar", command=self.refrescar).pack(side="right")
        frame, self.tv = tabla(self, [
            ("username", "Usuario", 200), ("rol", "Rol", 120), ("estado", "Estado", 120)])
        frame.pack(fill="both", expand=True)
        self.refrescar()

    def refrescar(self):
        try:
            self.cuentas = self.c.listar_cuentas()
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
            return
        self.tv.delete(*self.tv.get_children())
        for u in self.cuentas:
            self.tv.insert("", "end", iid=u["id"], values=(
                u["username"], u["rol"], "Activa" if u.get("activo") else "Desactivada"))

    def _sel(self):
        s = self.tv.selection()
        if not s:
            messagebox.showinfo(TITULO, "Seleccioná una cuenta.")
            return None
        return next(u for u in self.cuentas if u["id"] == s[0])

    def alternar(self):
        u = self._sel()
        if not u:
            return
        if u["id"] == self.c.usuario["id"]:
            messagebox.showwarning(TITULO, "No podés desactivar tu propia cuenta.")
            return
        try:
            self.c.set_activo(u["id"], not u.get("activo"))
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))
        self.refrescar()

    def resetear(self):
        u = self._sel()
        if not u:
            return
        nueva = simpledialog.askstring(
            TITULO, f"Nueva contraseña para '{u['username']}' (mínimo 8 caracteres):",
            show="•", parent=self)
        if not nueva:
            return
        if len(nueva) < 8:
            messagebox.showwarning(TITULO, "La contraseña debe tener al menos 8 caracteres.")
            return
        try:
            self.c.resetear_password(u["id"], nueva)
            messagebox.showinfo(TITULO, f"Contraseña de '{u['username']}' actualizada.")
        except ApiError as e:
            messagebox.showerror(TITULO, str(e))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITULO)
        self.geometry("460x300")
        self.minsize(460, 300)
        self.actual = None
        self.mostrar_login()

    def _cambiar(self, frame):
        if self.actual:
            self.actual.destroy()
        self.actual = frame
        frame.pack(fill="both", expand=True)

    def mostrar_login(self):
        self.geometry("460x300")
        self._cambiar(Login(self, self.mostrar_principal))

    def mostrar_principal(self, cliente):
        self.geometry("900x520")
        marco = ttk.Frame(self)
        top = ttk.Frame(marco, padding=(10, 6))
        top.pack(fill="x")
        rol = "Admin" if cliente.es_admin else "Usuario"
        ttk.Label(top, text=f"{TITULO}  —  {cliente.usuario['username']} ({rol})",
                  font=("Segoe UI", 11, "bold")).pack(side="left")
        ttk.Button(top, text="Cerrar sesión", command=self.mostrar_login).pack(side="right")
        nb = ttk.Notebook(marco)
        nb.pack(fill="both", expand=True)
        if cliente.es_admin:
            nb.add(PanelFiscal(nb, cliente), text="Causas")
            nb.add(PanelCuentas(nb, cliente), text="Cuentas")
        else:
            nb.add(PanelUsuario(nb, cliente), text="Mis causas")
        self._cambiar(marco)
