# Restaurante App - Semana 16

Proyecto de **Programación Orientada a Objetos** que evoluciona directamente desde la versión de la Semana 15. Se conserva el inicio de sesión, la navegación, la gestión de productos, las ventas, la persistencia JSON y la arquitectura modular; la evolución de esta semana se concentra en el **manejo de eventos aplicado a la gestión de usuarios**.

## Propósito

La gestión de usuarios demuestra el flujo solicitado:

```text
interacción del usuario
→ evento
→ bind()
→ callback(event)
→ RestauranteServicio
→ persistencia en usuarios.json
→ actualización del Treeview
→ respuesta visual
```

La interfaz captura eventos y actualiza la vista. Las validaciones, reglas de negocio y persistencia no se realizan directamente desde la interfaz, sino mediante `RestauranteServicio` y `ArchivoServicio`.

## Estructura

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo_restaurante.png
│   ├── icono_producto.png
│   ├── icono_usuario.png
│   └── icono_venta.png
├── main.py
└── README.md
```

## Evolución realizada en Semana 16

- Se añadió el atributo `rol` al modelo `Usuario`.
- Se persiste el rol en `datos/usuarios.json`.
- Se manejan los roles `Administrador`, `Empleado` y `Cliente`.
- Solo el usuario con rol **Administrador** visualiza la opción administrativa **Usuarios**.
- El Administrador puede registrar, consultar, actualizar y eliminar usuarios de tipo **Empleado** y **Cliente**.
- La cuenta Administrador está protegida contra actualización/eliminación accidental desde la gestión.
- La tabla `Treeview` muestra identificación, nombre, usuario y rol; no muestra la contraseña.
- Se reutiliza `RestauranteServicio` para consultar el objeto completo a partir del identificador seleccionado.
- Se conserva la funcionalidad anterior de Productos y Ventas.
- Se integran el logotipo y los íconos de Productos, Usuarios y Ventas desde `assets/`.

## Eventos implementados

### `<<TreeviewSelect>>`

Se asocia mediante:

```python
self.tabla_usuarios.bind(
    "<<TreeviewSelect>>",
    self._al_seleccionar_usuario
)
```

Al seleccionar una fila, el callback obtiene la identificación, consulta el usuario mediante `RestauranteServicio` y carga sus datos en el formulario.

### `<Return>`

```python
control.bind("<Return>", self._evento_registrar_usuario)
```

El callback **reutiliza** `registrar_usuario()`, el mismo método que usa el botón Registrar. Así se evita duplicar la lógica.

### `<Escape>`

```python
control.bind("<Escape>", self._evento_limpiar_usuario)
```

Limpia el formulario, cancela la selección y devuelve la interfaz a un estado inicial.

### `<<ComboboxSelected>>`

```python
self.usuario_rol_combo.bind(
    "<<ComboboxSelected>>",
    self._al_cambiar_rol_usuario
)
```

Permite responder al cambio de rol seleccionado.

### `command=`

Los botones principales continúan utilizando `command=`:

- Registrar
- Actualizar
- Eliminar
- Limpiar

Esto permite diferenciar el callback directo de los botones y los callbacks asociados mediante `bind()`.

## Gestión de usuarios y persistencia

`RestauranteServicio` concentra:

- validación de campos;
- unicidad de identificación;
- unicidad del nombre de usuario;
- registro;
- consulta;
- actualización;
- eliminación;
- protección de la cuenta Administrador;
- protección de la cuenta actualmente autenticada;
- persistencia mediante `usuarios.json`.

`ArchivoServicio` continúa siendo el único responsable de leer y escribir archivos JSON.

## Roles

- **Administrador:** puede acceder a la gestión administrativa de usuarios.
- **Empleado:** inicia sesión y utiliza las funcionalidades generales, pero no dispone del mantenimiento administrativo de usuarios.
- **Cliente:** inicia sesión y utiliza las funcionalidades generales, pero no dispone del mantenimiento administrativo de usuarios.

La pantalla administrativa permite al Administrador gestionar usuarios de tipo **Empleado** y **Cliente**, tal como solicita la actividad.

## Credenciales de prueba

### Administrador
- Usuario: `admin`
- Contraseña: `admin123`

### Cliente
- Usuario: `carolina`
- Contraseña: `1234`

### Empleado
- Usuario: `mesero`
- Contraseña: `mesero123`

## Ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

## Comprobación mínima sugerida

1. Ejecutar `main.py`.
2. Iniciar sesión con `admin / admin123`.
3. Confirmar que Productos y Ventas continúan funcionando.
4. Abrir **Usuarios**.
5. Registrar un usuario Cliente o Empleado.
6. Confirmar que aparece inmediatamente en el `Treeview`.
7. Seleccionar una fila y comprobar que `<<TreeviewSelect>>` carga los datos.
8. Modificar un dato y presionar **Actualizar**.
9. Seleccionar un usuario y utilizar **Eliminar**; debe solicitar confirmación.
10. Comprobar que la cuenta Administrador no puede eliminarse desde esta pantalla.
11. Completar el formulario y presionar **Enter** para registrar mediante `<Return>`.
12. Presionar **Escape** para limpiar formulario y selección.
13. Cambiar el rol y comprobar la respuesta a `<<ComboboxSelected>>`.
14. Cerrar y ejecutar nuevamente la aplicación para comprobar persistencia en `usuarios.json`.
15. Iniciar sesión como Cliente o Empleado y verificar que no disponen de la opción administrativa **Usuarios**.

## Separación de responsabilidades

- `ui/`: interacción, eventos y actualización visual.
- `modelos/`: representación de entidades.
- `RestauranteServicio`: validaciones, reglas y operaciones del dominio.
- `ArchivoServicio`: persistencia JSON.
- `datos/`: archivos persistentes.
- `assets/`: logo e íconos del sistema.
- `main.py`: arranque y navegación principal.
