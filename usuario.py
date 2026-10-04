class Usuario:
    ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion, nombre, usuario, contrasena, rol="Cliente"):
        self.identificacion = str(identificacion).strip()
        self.nombre = str(nombre).strip()
        self.usuario = str(usuario).strip()
        self.contrasena = str(contrasena)
        self.rol = rol if rol in self.ROLES_VALIDOS else "Cliente"

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            datos.get("identificacion", ""),
            datos.get("nombre", ""),
            datos.get("usuario", ""),
            datos.get("contrasena", ""),
            datos.get("rol", "Cliente"),
        )

    def a_dict(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    def __str__(self):
        return f"{self.identificacion} - {self.nombre} ({self.usuario}) [{self.rol}]"
