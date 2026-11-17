"""Vista en consola para mostrar el menú y los reportes del sistema."""


def mostrar_menu_principal():
    """Imprime las opciones del menú y retorna la selección del usuario."""
    print("\n=== PRÉSTAMO DE PORTÁTILES SENA ===")
    print("1. Registrar usuario")
    print("2. Registrar computador")
    print("3. Prestar computador")
    print("4. Devolver computador")
    print("5. Ver equipos y préstamos activos")
    print("6. Salir")
    return input("Elige una opción: ").strip()


def mostrar_resumen(equipos, prestamos):
    """Imprime en consola el estado de los equipos y los préstamos activos."""
    print("\n--- EQUIPOS REGISTRADOS ---")
    if not equipos:
        print("No hay equipos registrados.")
    else:
        for e in equipos:
            print(f"  {e['codigo']} | {e['marca']} | {e['estado']}")

    print("\n--- PRÉSTAMOS ACTIVOS ---")
    hay_activos = False
    for p in prestamos:
        if p["estado"] == "ACTIVO":
            hay_activos = True
            limite = p["fecha_limite"].strftime("%Y-%m-%d %H:%M")
            print(f"  Doc: {p['documento']} | Equipo: {p['codigo']} | Límite: {limite}")
    if not hay_activos:
        print("No hay préstamos activos.")
