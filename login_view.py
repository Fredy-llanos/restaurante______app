import tkinter as tk
from pathlib import Path
from tkinter import ttk


class LoginView(ttk.Frame):
    def __init__(self, parent, servicio, al_ingresar):
        super().__init__(parent, padding=25)
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets"
        self.logo = None
        self._construir()

    def _construir(self):
        self.pack(fill="both", expand=True)
        contenedor = ttk.Frame(self, padding=25)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        ruta_logo = self.assets_dir / "logo_restaurante.png"
        if ruta_logo.exists():
            try:
                self.logo = tk.PhotoImage(file=str(ruta_logo))
                ttk.Label(contenedor, image=self.logo).grid(row=0, column=0, columnspan=2, pady=(0, 8))
            except tk.TclError:
                pass

        ttk.Label(contenedor, text="Restaurante App", font=("Segoe UI", 20, "bold")).grid(row=1, column=0, columnspan=2, pady=(0, 8))
        ttk.Label(contenedor, text="Acceso al sistema", font=("Segoe UI", 11)).grid(row=2, column=0, columnspan=2, pady=(0, 20))
        ttk.Label(contenedor, text="Usuario:").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=7)
        self.usuario_entry = ttk.Entry(contenedor, width=28)
        self.usuario_entry.grid(row=3, column=1, pady=7)
        ttk.Label(contenedor, text="Contraseña:").grid(row=4, column=0, sticky="w", padx=(0, 10), pady=7)
        self.contrasena_entry = ttk.Entry(contenedor, width=28, show="*")
        self.contrasena_entry.grid(row=4, column=1, pady=7)
        ttk.Button(contenedor, text="Iniciar sesión", command=self._intentar_ingreso).grid(row=5, column=0, columnspan=2, pady=(15, 8), ipadx=15)
        self.mensaje_label = ttk.Label(contenedor, text="")
        self.mensaje_label.grid(row=6, column=0, columnspan=2, pady=(6, 0))
        self.usuario_entry.focus()
        self.contrasena_entry.bind("<Return>", lambda _evento: self._intentar_ingreso())

    def _intentar_ingreso(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        if not usuario or not contrasena:
            self.mensaje_label.config(text="Complete usuario y contraseña.", foreground="red")
            return
        usuario_validado = self.servicio.validar_acceso(usuario, contrasena)
        if usuario_validado is None:
            self.mensaje_label.config(text="Usuario o contraseña incorrectos.", foreground="red")
            self.contrasena_entry.delete(0, tk.END)
            return
        self.mensaje_label.config(text=f"Bienvenido/a, {usuario_validado.nombre}.", foreground="green")
        self.al_ingresar(usuario_validado)
