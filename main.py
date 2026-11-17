

import logica
import menu

def main():
    usuarios = []
    equipos = []
    prestamos = []
    opcion = ""
    while opcion != "6":
        opcion = menu.mostrar_menu_principal()
        if opcion == "1":
            logica.registrar_usuario(usuarios)
        elif opcion == "2":
            logica.registrar_equipo(equipos)
        elif opcion == "3":
            logica.prestar_equipo(usuarios, equipos, prestamos)
        elif opcion == "4":
            logica.devolver_equipo(usuarios, equipos, prestamos)
        elif opcion == "5":
            menu.mostrar_resumen(equipos, prestamos)
        elif opcion == "6":
            print("¡Hasta luego!")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
