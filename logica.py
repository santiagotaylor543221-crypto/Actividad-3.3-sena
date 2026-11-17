from datetime import datetime, timedelta
import validaciones
def registrar_usuario(usuarios):
    doc = input("Documento: ")
    nombre = input("Nombre: ")
    ok, msg = validaciones.validar_nuevo_usuario(doc, nombre, usuarios)
    if not ok:
        print(f"Error: {msg}")
        return
    usuarios.append({"documento": doc.strip(), "nombre": nombre.strip(), "estado": "ACTIVO"})
    print("Usuario registrado correctamente.")

def registrar_equipo(equipos):
    cod = input("Código (ej. PORT-001): ")
    marca = input("Marca: ")
    ok, msg = validaciones.validar_nuevo_equipo(cod, marca, equipos)
    if not ok:
        print(f"Error: {msg}")
        return
    equipos.append({"codigo": cod.strip().upper(), "marca": marca.strip(), "estado": "DISPONIBLE"})
    print(f"Equipo {cod.strip().upper()} registrado correctamente.")

def prestar_equipo(usuarios, equipos, prestamos):
    doc = input("Documento del usuario: ")
    cod = input("Código del equipo: ")
    try:
        horas = int(input("Horas de préstamo (1 a 12): "))
    except ValueError:
        print("Error: las horas deben ser un número entero.")
        return
    ok, msg = validaciones.validar_usuario_prestamo(doc, usuarios, prestamos)
    if not ok:
        print(f"Error: {msg}")
        return
    ok, msg = validaciones.validar_equipo_prestamo(cod, equipos, horas)
    if not ok:
        print(f"Error: {msg}")
        return
    codigo = cod.strip().upper()
    hora_limite = datetime.now() + timedelta(hours=horas)
    for e in equipos:
        if e["codigo"] == codigo:
            e["estado"] = "PRESTADO"
    prestamos.append({"documento": doc.strip(), "codigo": codigo, "fecha_limite": hora_limite, "estado": "ACTIVO"})
    print(f"Préstamo registrado. Límite: {hora_limite.strftime('%Y-%m-%d %H:%M')}")

def devolver_equipo(usuarios, equipos, prestamos):
    codigo = input("Código del equipo a devolver: ").strip().upper()
    prestamo_encontrado = None
    for p in prestamos:
        if p["codigo"] == codigo and p["estado"] == "ACTIVO":
            prestamo_encontrado = p
    if prestamo_encontrado is None:
        print("Error: no hay préstamo activo para ese equipo.")
        return
    dano = input("¿Tiene daño físico? (s/n): ").strip().lower()
    prestamo_encontrado["estado"] = "DEVUELTO"
    mensaje = "Devolución registrada."
    if datetime.now() > prestamo_encontrado["fecha_limite"]:
        mensaje = "Devolución registrada. (Entrega tardía: usuario SANCIONADO)"
        for u in usuarios:
            if u["documento"] == prestamo_encontrado["documento"]:
                u["estado"] = "SANCIONADO"
    for e in equipos:
        if e["codigo"] == codigo:
            if dano == "s":
                e["estado"] = "MANTENIMIENTO"
            else:
                e["estado"] = "DISPONIBLE"
    print(mensaje)
