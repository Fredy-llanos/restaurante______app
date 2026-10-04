import tkinter as tk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Restaurante App - Semana 16")
        self.ventana.geometry("1050x680")
        self.ventana.minsize(930, 600)

        archivo_servicio = ArchivoServicio()
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.vista_actual = None
        self.mostrar_login()

    def _limpiar_vista(self):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def mostrar_login(self):
        self._limpiar_vista()
        self.vista_actual = LoginView(self.ventana, self.restaurante_servicio, self.mostrar_principal)

    def mostrar_principal(self, usuario):
        self._limpiar_vista()
        self.vista_actual = MainView(self.ventana, self.restaurante_servicio, usuario, self.mostrar_login)

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    app = RestauranteApp()
    app.ejecutar()
