/// <reference path="../pb_data/types.d.ts" />

// Reseteo de contraseña de una cuenta, permitido solo a un admin activo.
// PocketBase exige la contraseña anterior a cualquier cuenta que no sea superusuario,
// por eso el admin usa esta ruta en lugar de editar el registro directamente.
routerAdd("POST", "/api/fiscalia/reset-password", (e) => {
  const auth = e.auth;
  if (!auth || auth.collection().name !== "users" ||
      auth.getString("rol") !== "admin" || !auth.getBool("activo")) {
    throw new ForbiddenError("Solo un admin puede resetear contraseñas.");
  }

  const data = new DynamicModel({ usuario: "", password: "" });
  e.bindBody(data);

  if (!data.usuario) {
    throw new BadRequestError("Falta el usuario.");
  }
  if (data.password.length < 8) {
    throw new BadRequestError("La contraseña debe tener al menos 8 caracteres.");
  }

  const registro = e.app.findRecordById("users", data.usuario);
  registro.setPassword(data.password);
  e.app.save(registro);

  return e.json(200, { ok: true });
}, $apis.requireAuth("users"));
