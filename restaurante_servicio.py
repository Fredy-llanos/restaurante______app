from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Concentra validaciones, reglas de negocio y operaciones del restaurante."""

    ARCHIVO_PRODUCTOS = "productos.json"
    ARCHIVO_USUARIOS = "usuarios.json"
    ARCHIVO_VENTAS = "ventas.json"
    ROLES_GESTIONABLES = ("Empleado", "Cliente")

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self._usuarios = []
        self._productos = []
        self._ventas = []
        self.cargar_datos()

    # ---------------------------
    # Carga y persistencia
    # ---------------------------
    def cargar_datos(self):
        datos_usuarios = self.archivo_servicio.leer_json(self.ARCHIVO_USUARIOS)
        datos_productos = self.archivo_servicio.leer_json(self.ARCHIVO_PRODUCTOS)
        datos_ventas = self.archivo_servicio.leer_json(self.ARCHIVO_VENTAS)

        self._usuarios = [Usuario.desde_dict(item) for item in datos_usuarios]
        self._productos = [Producto.desde_dict(item) for item in datos_productos]
        self._ventas = [Venta.desde_dict(item) for item in datos_ventas]

        # Compatibilidad con versiones previas: garantiza al menos un administrador.
        if self._usuarios and not any(u.rol == "Administrador" for u in self._usuarios):
            self._usuarios[0].rol = "Administrador"
            self._guardar_usuarios()

    def _guardar_usuarios(self):
        self.archivo_servicio.guardar_json(
            self.ARCHIVO_USUARIOS,
            [usuario.a_dict() for usuario in self._usuarios],
        )

    def _guardar_productos(self):
        self.archivo_servicio.guardar_json(
            self.ARCHIVO_PRODUCTOS,
            [producto.a_dict() for producto in self._productos],
        )

    def _guardar_ventas(self):
        self.archivo_servicio.guardar_json(
            self.ARCHIVO_VENTAS,
            [venta.a_dict() for venta in self._ventas],
        )

    # ---------------------------
    # Acceso y consultas generales
    # ---------------------------
    def validar_acceso(self, usuario, contrasena):
        usuario = usuario.strip()
        contrasena = contrasena.strip()
        if not usuario or not contrasena:
            return None

        for persona in self._usuarios:
            if persona.usuario == usuario and persona.contrasena == contrasena:
                return persona
        return None

    def listar_usuarios(self):
        return list(self._usuarios)

    def listar_productos(self):
        return list(self._productos)

    def listar_ventas(self):
        return list(self._ventas)

    def cantidad_usuarios(self):
        return len(self._usuarios)

    def cantidad_productos(self):
        return len(self._productos)

    def cantidad_ventas(self):
        return len(self._ventas)

    def obtener_usuario(self, identificacion):
        identificacion = str(identificacion).strip()
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def _obtener_usuario_por_login(self, nombre_usuario):
        nombre_usuario = str(nombre_usuario).strip().lower()
        for usuario in self._usuarios:
            if usuario.usuario.lower() == nombre_usuario:
                return usuario
        return None

    # ---------------------------
    # Gestión de usuarios - Semana 16
    # ---------------------------
    def _validar_datos_usuario(self, identificacion, nombre, usuario, contrasena, rol):
        identificacion = str(identificacion).strip()
        nombre = str(nombre).strip()
        usuario = str(usuario).strip()
        contrasena = str(contrasena).strip()
        rol = str(rol).strip()

        if not identificacion:
            raise ValueError("Ingrese la identificación.")
        if not nombre:
            raise ValueError("Ingrese el nombre.")
        if not usuario:
            raise ValueError("Ingrese el nombre de usuario.")
        if not contrasena:
            raise ValueError("Ingrese la contraseña.")
        if rol not in self.ROLES_GESTIONABLES:
            raise ValueError("Seleccione un rol válido: Empleado o Cliente.")

        return identificacion, nombre, usuario, contrasena, rol

    def registrar_usuario(self, identificacion, nombre, usuario, contrasena, rol):
        datos = self._validar_datos_usuario(
            identificacion, nombre, usuario, contrasena, rol
        )
        if self.obtener_usuario(datos[0]) is not None:
            raise ValueError("Ya existe un usuario con esa identificación.")
        if self._obtener_usuario_por_login(datos[2]) is not None:
            raise ValueError("Ese nombre de usuario ya se encuentra registrado.")

        nuevo = Usuario(*datos)
        self._usuarios.append(nuevo)
        self._guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, identificacion, nombre, usuario, contrasena, rol):
        datos = self._validar_datos_usuario(
            identificacion, nombre, usuario, contrasena, rol
        )
        existente = self.obtener_usuario(datos[0])
        if existente is None:
            raise ValueError("No se encontró un usuario con esa identificación.")
        if existente.rol == "Administrador":
            raise ValueError("La cuenta Administrador no se modifica desde esta pantalla.")

        duplicado = self._obtener_usuario_por_login(datos[2])
        if duplicado is not None and duplicado.identificacion != existente.identificacion:
            raise ValueError("Ese nombre de usuario ya pertenece a otro registro.")

        existente.nombre = datos[1]
        existente.usuario = datos[2]
        existente.contrasena = datos[3]
        existente.rol = datos[4]
        self._guardar_usuarios()
        return existente

    def eliminar_usuario(self, identificacion, usuario_actual_id=None):
        usuario = self.obtener_usuario(identificacion)
        if usuario is None:
            raise ValueError("No se encontró un usuario con esa identificación.")
        if usuario_actual_id and usuario.identificacion == str(usuario_actual_id).strip():
            raise ValueError("No puede eliminar la cuenta con la que inició sesión.")
        if usuario.rol == "Administrador":
            raise ValueError("La cuenta Administrador está protegida y no puede eliminarse.")

        self._usuarios.remove(usuario)
        self._guardar_usuarios()
        return usuario

    # ---------------------------
    # Gestión de productos
    # ---------------------------
    def obtener_producto(self, codigo):
        codigo = str(codigo).strip().upper()
        if not codigo:
            return None
        for producto in self._productos:
            if producto.codigo.upper() == codigo:
                return producto
        return None

    def _validar_datos_producto(self, codigo, nombre, categoria, precio, cantidad):
        codigo = str(codigo).strip().upper()
        nombre = str(nombre).strip()
        categoria = str(categoria).strip()
        precio_texto = str(precio).strip().replace(",", ".")
        cantidad_texto = str(cantidad).strip()

        if not codigo:
            raise ValueError("Ingrese el código del producto.")
        if not nombre:
            raise ValueError("Ingrese el nombre del producto.")
        if not categoria:
            raise ValueError("Seleccione una categoría.")

        try:
            precio_num = float(precio_texto)
        except ValueError as exc:
            raise ValueError("El precio debe ser un número válido.") from exc
        try:
            cantidad_num = int(cantidad_texto)
        except ValueError as exc:
            raise ValueError("La cantidad debe ser un número entero.") from exc

        if precio_num < 0:
            raise ValueError("El precio no puede ser negativo.")
        if cantidad_num < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        return codigo, nombre, categoria, precio_num, cantidad_num

    def registrar_producto(self, codigo, nombre, categoria, precio, cantidad):
        datos = self._validar_datos_producto(codigo, nombre, categoria, precio, cantidad)
        if self.obtener_producto(datos[0]) is not None:
            raise ValueError(f"Ya existe un producto con el código {datos[0]}.")
        producto = Producto(*datos)
        self._productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, codigo, nombre, categoria, precio, cantidad):
        datos = self._validar_datos_producto(codigo, nombre, categoria, precio, cantidad)
        producto = self.obtener_producto(datos[0])
        if producto is None:
            raise ValueError("No se encontró un producto con ese código.")
        producto.nombre = datos[1]
        producto.categoria = datos[2]
        producto.precio = datos[3]
        producto.cantidad = datos[4]
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo):
        producto = self.obtener_producto(codigo)
        if producto is None:
            raise ValueError("No se encontró un producto con ese código.")
        self._productos.remove(producto)
        self._guardar_productos()
        return producto

    # ---------------------------
    # Gestión de ventas
    # ---------------------------
    def registrar_venta(self, usuario_id, producto_codigo):
        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip().upper()

        if not usuario_id:
            raise ValueError("Seleccione un usuario para registrar la venta.")
        if not producto_codigo:
            raise ValueError("Seleccione un producto para registrar la venta.")

        usuario = self.obtener_usuario(usuario_id)
        if usuario is None:
            raise ValueError("El usuario seleccionado no existe.")
        producto = self.obtener_producto(producto_codigo)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        siguiente = len(self._ventas) + 1
        identificador = f"V{siguiente:03d}"
        existentes = {venta.identificador for venta in self._ventas}
        while identificador in existentes:
            siguiente += 1
            identificador = f"V{siguiente:03d}"

        venta = Venta(
            identificador=identificador,
            usuario_id=usuario.identificacion,
            producto_codigo=producto.codigo,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self._ventas.append(venta)
        self._guardar_ventas()
        return venta
