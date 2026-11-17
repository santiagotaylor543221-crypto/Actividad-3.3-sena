# Sistema de Préstamo de Portátiles — SENA

Aplicación de consola modular en Python para gestionar el registro de usuarios, el inventario de computadores portátiles, los préstamos por horas y las devoluciones con control de daños físicos y sanciones por entrega tardía.

---

## 1. Requisitos y ejecución

- **Lenguaje:** Python 3.x (únicamente librería estándar: `datetime` y `timedelta`).
- **Dependencias externas:** Ninguna.

Para iniciar el programa desde la carpeta del proyecto:

```bash
python3 main.py
```

---

## 2. Estructura del proyecto

```text
Actividad 3.3/
├── main.py           # Orquestador principal y ciclo del menú
├── menu.py           # Capa de vista en consola (menú y resúmenes)
├── logica.py         # Captura de entradas y ejecución de operaciones
├── validaciones.py   # Reglas puras de negocio y validación de datos
└── README.md         # Documentación del sistema
```

### Responsabilidad de cada módulo

| Archivo | Responsabilidad | Qué contiene | Qué **NO** hace |
| :--- | :--- | :--- | :--- |
| `main.py` | Orquestación | Inicializa `usuarios`, `equipos` y `prestamos`; ejecuta el ciclo `while opcion != "6"` y despacha cada opción. | No pide datos de negocio, no valida reglas ni formatea reportes. |
| `menu.py` | Vista en consola | `mostrar_menu_principal()` y `mostrar_resumen(equipos, prestamos)`. | No modifica listas ni aplica reglas de negocio. |
| `logica.py` | Lógica y flujo | `registrar_usuario`, `registrar_equipo`, `prestar_equipo`, `devolver_equipo`. Pide `input()`, maneja `ValueError` y actualiza estados con `datetime`. | No decide reglas de negocio complejas sin consultar a `validaciones.py`. |
| `validaciones.py` | Reglas de negocio | `validar_nuevo_usuario`, `validar_nuevo_equipo`, `validar_usuario_prestamo`, `validar_equipo_prestamo`. | No imprime en consola ni modifica las listas recibidas. |

---

## 3. Flujo completo de ejecución

### Flujo general del programa

```text
[Inicio]
   │
   ▼
main.py: crea usuarios = [], equipos = [], prestamos = []
   │
   ▼
menu.mostrar_menu_principal() ──► Muestra opciones 1..6 y retorna la elección
   │
   ├── "1" ─► logica.registrar_usuario(usuarios)
   │             └─► validaciones.validar_nuevo_usuario(...)
   │
   ├── "2" ─► logica.registrar_equipo(equipos)
   │             └─► validaciones.validar_nuevo_equipo(...)
   │
   ├── "3" ─► logica.prestar_equipo(usuarios, equipos, prestamos)
   │             ├─► validaciones.validar_usuario_prestamo(...)
   │             └─► validaciones.validar_equipo_prestamo(...)
   │
   ├── "4" ─► logica.devolver_equipo(usuarios, equipos, prestamos)
   │
   ├── "5" ─► menu.mostrar_resumen(equipos, prestamos)
   │
   └── "6" ─► Finaliza el ciclo y sale del programa
```

### Flujo detallado por operación

1. **Registrar usuario (`opción 1`)**:
   - `logica.registrar_usuario(usuarios)` solicita `documento` y `nombre`.
   - `validaciones.validar_nuevo_usuario` verifica que ningún campo esté vacío y recorre `usuarios` para impedir documentos duplicados.
   - Si es válido, agrega `{"documento": ..., "nombre": ..., "estado": "ACTIVO"}`.

2. **Registrar computador (`opción 2`)**:
   - `logica.registrar_equipo(equipos)` solicita `código` y `marca`.
   - `validaciones.validar_nuevo_equipo` normaliza el código con `.strip().upper()`, verifica campos obligatorios y evita códigos repetidos.
   - Si es válido, agrega `{"codigo": ..., "marca": ..., "estado": "DISPONIBLE"}`.

3. **Prestar computador (`opción 3`)**:
   - `logica.prestar_equipo(usuarios, equipos, prestamos)` solicita documento, código y horas.
   - Convierte las horas a entero dentro de un bloque `try / except ValueError` para evitar cierres inesperados si el usuario digita texto.
   - Valida en dos pasos:
     1. `validar_usuario_prestamo`: el usuario debe existir, tener estado `"ACTIVO"` (no `"SANCIONADO"`) y no tener otro préstamo en estado `"ACTIVO"`.
     2. `validar_equipo_prestamo`: el equipo debe existir, estar `"DISPONIBLE"` y las horas deben estar entre `1` y `12`.
   - Calcula `hora_limite = datetime.now() + timedelta(hours=horas)`, cambia el equipo a `"PRESTADO"` y registra el préstamo como `"ACTIVO"`.

4. **Devolver computador (`opción 4`)**:
   - `logica.devolver_equipo(usuarios, equipos, prestamos)` busca en `prestamos` un registro `"ACTIVO"` que coincida con el código ingresado.
   - Pregunta si existe daño físico (`s/n`), cambia el préstamo a `"DEVUELTO"` y compara `datetime.now() > prestamo_encontrado["fecha_limite"]`:
     - Si la entrega es tardía, busca al usuario y cambia su estado a `"SANCIONADO"`.
   - Actualiza el estado del equipo a `"MANTENIMIENTO"` si hubo daño físico, o a `"DISPONIBLE"` si regresó en buen estado.

5. **Ver equipos y préstamos activos (`opción 5`)**:
   - `menu.mostrar_resumen(equipos, prestamos)` recorre ambas listas e imprime los equipos con su estado actual y los préstamos que permanecen en `"ACTIVO"` junto con su fecha y hora límite.

---

## 4. Justificación de decisiones de diseño

- **Separación en 4 módulos (`main`, `menu`, `logica`, `validaciones`):**
  Evita mezclar la interfaz de consola con las reglas de negocio. Si mañana cambia la forma de mostrar los datos (por ejemplo, pasar de consola a interfaz gráfica o web), `validaciones.py` puede reutilizarse sin modificaciones.
- **`main.py` como orquestador puro:**
  Mantener `main.py` libre de `input()` de negocio, `try/except` y formateo de tablas hace evidente el mapa completo de la aplicación en pocas líneas y facilita la lectura durante una sustentación.
- **Estructuras en memoria con `list` y `dict` simples:**
  Al no requerir persistencia en disco ni dependencias externas, trabajar directamente con diccionarios y listas nativas elimina código repetitivo de serialización y mantiene el foco en el flujo lógico y las estructuras de control (`for`, `if`, `elif`, `else`).
- **Retorno de tuplas `(exito, mensaje)` en `validaciones.py`:**
  En lugar de definir excepciones personalizadas, cada validador retorna `(True, "")` o `(False, "Mensaje de error")`. Esto hace explícito el control de errores con un simple `if not ok:` y permite probar o explicar cada regla de forma aislada.
- **Normalización de entradas (`.strip()` y `.upper()`):**
  Evita rechazos falsos por espacios accidentales al inicio o final y garantiza que códigos como `port-001` y `PORT-001` se reconozcan como el mismo equipo.
- **Control explícito de `ValueError` al leer horas:**
  Convertir la entrada de horas dentro de `try / except ValueError` protege el programa frente a errores de tipeo del operador sin interrumpir la sesión activa en memoria.
- **Sanción automática y paso a mantenimiento en devoluciones:**
  Automatizar el cambio a `"SANCIONADO"` por mora y a `"MANTENIMIENTO"` por daño físico evita depender de pasos manuales adicionales y garantiza que `validar_usuario_prestamo` y `validar_equipo_prestamo` bloqueen futuros préstamos de inmediato.

---

Author: Santiago Taylor
