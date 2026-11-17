"""Validaciones para usuarios, equipos y préstamos."""


def validar_nuevo_usuario(documento, nombre, usuarios):
    """Verifica datos no vacíos y que el documento no esté duplicado."""
    doc = documento.strip()
    if not doc or not nombre.strip():
        return False, "El documento y el nombre son obligatorios."
    for u in usuarios:
        if u["documento"] == doc:
            return False, f"Ya existe un usuario con documento {doc}."
    return True, ""


def validar_nuevo_equipo(codigo, marca, equipos):
    """Verifica datos no vacíos y que el código no esté duplicado."""
    cod = codigo.strip().upper()
    if not cod or not marca.strip():
        return False, "El código y la marca son obligatorios."
    for e in equipos:
        if e["codigo"] == cod:
            return False, f"Ya existe un equipo con código {cod}."
    return True, ""


def validar_usuario_prestamo(documento, usuarios, prestamos):
    """Verifica que el usuario exista, esté ACTIVO y sin préstamo activo."""
    doc = documento.strip()
    usuario = None
    for u in usuarios:
        if u["documento"] == doc:
            usuario = u
            break
    if usuario is None:
        return False, "El usuario no está registrado."
    if usuario["estado"] != "ACTIVO":
        return False, f"Usuario bloqueado (estado: {usuario['estado']})."
    for p in prestamos:
        if p["documento"] == doc and p["estado"] == "ACTIVO":
            return False, "El usuario ya tiene un préstamo activo."
    return True, ""


def validar_equipo_prestamo(codigo, equipos, horas):
    """Verifica que el equipo exista, esté DISPONIBLE y horas entre 1 y 12."""
    cod = codigo.strip().upper()
    equipo = None
    for e in equipos:
        if e["codigo"] == cod:
            equipo = e
            break
    if equipo is None:
        return False, "El equipo no está registrado."
    if equipo["estado"] != "DISPONIBLE":
        return False, f"Equipo no disponible (estado: {equipo['estado']})."
    if horas < 1 or horas > 12:
        return False, "Las horas deben estar entre 1 y 12."
    return True, ""
