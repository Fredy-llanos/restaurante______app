class Venta:
    """Representa una venta sencilla entre un usuario y un producto."""

    def __init__(self, identificador, usuario_id, producto_codigo, fecha):
        self.identificador = str(identificador).strip()
        self.usuario_id = str(usuario_id).strip()
        self.producto_codigo = str(producto_codigo).strip().upper()
        self.fecha = str(fecha).strip()

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            datos.get("identificador", ""),
            datos.get("usuario_id", ""),
            datos.get("producto_codigo", ""),
            datos.get("fecha", ""),
        )

    def a_dict(self):
        return {
            "identificador": self.identificador,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }

    def __str__(self):
        return f"{self.identificador} | Usuario: {self.usuario_id} | Producto: {self.producto_codigo} | {self.fecha}"
