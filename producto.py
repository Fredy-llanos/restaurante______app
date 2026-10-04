class Producto:
    def __init__(self, codigo, nombre, categoria, precio, cantidad):
        self.codigo = str(codigo).strip()
        self.nombre = str(nombre).strip()
        self.categoria = str(categoria).strip()
        self.precio = float(precio)
        self.cantidad = int(cantidad)

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            datos.get("codigo", ""),
            datos.get("nombre", ""),
            datos.get("categoria", ""),
            datos.get("precio", 0),
            datos.get("cantidad", 0),
        )

    def a_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }

    def __str__(self):
        return (
            f"{self.codigo} - {self.nombre} | {self.categoria} | "
            f"${self.precio:.2f} | Stock: {self.cantidad}"
        )
