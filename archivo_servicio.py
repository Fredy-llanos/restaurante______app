import json
from pathlib import Path


class ArchivoServicio:
    """Responsable únicamente de la lectura y escritura de archivos JSON."""

    def __init__(self, carpeta_datos=None):
        if carpeta_datos is None:
            carpeta_datos = Path(__file__).resolve().parent.parent / "datos"
        self.carpeta_datos = Path(carpeta_datos)
        self.carpeta_datos.mkdir(parents=True, exist_ok=True)

    def leer_json(self, nombre_archivo):
        ruta = self.carpeta_datos / nombre_archivo
        if not ruta.exists():
            return []

        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar_json(self, nombre_archivo, datos):
        ruta = self.carpeta_datos / nombre_archivo
        temporal = ruta.with_suffix(ruta.suffix + ".tmp")

        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

        temporal.replace(ruta)
