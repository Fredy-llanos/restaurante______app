import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class MainView(ttk.Frame):
    """Interfaz principal del restaurante evolucionada para la Semana 16."""

    CATEGORIAS = ("Comida", "Bebida", "Acompañamiento", "Postre", "Otro")

    def __init__(self, parent, servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(parent, padding=0)
        self.parent = parent
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets"
        self._imagenes = {}

        self.contenido = None
        self.resumen_productos = None
        self.resumen_usuarios = None
        self.resumen_ventas = None

        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()
        self.venta_usuario_var = tk.StringVar()
        self.venta_producto_var = tk.StringVar()

        # Variables de la gestión de usuarios - Semana 16
        self.usuario_id_var = tk.StringVar()
        self.usuario_nombre_var = tk.StringVar()
        self.usuario_login_var = tk.StringVar()
        self.usuario_clave_var = tk.StringVar()
        self.usuario_rol_var = tk.StringVar()
        self.usuario_seleccionado_id = None
        self.tabla_usuarios = None
        self.usuario_rol_combo = None

        self.estado_var = tk.StringVar(value="Seleccione una opción del menú.")

        self._configurar_estilos()
        self._construir()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 19, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("Resumen.TLabel", font=("Segoe UI", 10, "bold"))
        estilo.configure("Menu.TButton", padding=(10, 8))
        estilo.configure("Accion.TButton", padding=(8, 6))

    def _cargar_imagen(self, nombre):
        ruta = self.assets_dir / nombre
        if not ruta.exists():
            return None
        try:
            imagen = tk.PhotoImage(file=str(ruta))
            self._imagenes[nombre] = imagen
            return imagen
        except tk.TclError:
            return None

    def _construir(self):
        self.pack(fill="both", expand=True)

        encabezado = ttk.Frame(self, padding=(18, 12))
        encabezado.pack(fill="x")
        logo = self._cargar_imagen("logo_restaurante.png")
        if logo is not None:
            ttk.Label(encabezado, image=logo).pack(side="left", padx=(0, 10))
        ttk.Label(encabezado, text="Restaurante App", style="Titulo.TLabel").pack(side="left")
        ttk.Label(encabezado, text=f"Sesión: {self.usuario_actual.nombre} | Rol: {self.usuario_actual.rol}").pack(side="right")

        resumen = ttk.Frame(self, padding=(18, 0, 18, 12))
        resumen.pack(fill="x")
        self.resumen_productos = ttk.Label(resumen, style="Resumen.TLabel")
        self.resumen_productos.pack(side="left", padx=(0, 25))
        self.resumen_usuarios = ttk.Label(resumen, style="Resumen.TLabel")
        self.resumen_usuarios.pack(side="left", padx=(0, 25))
        self.resumen_ventas = ttk.Label(resumen, style="Resumen.TLabel")
        self.resumen_ventas.pack(side="left")
        self._actualizar_resumen()

        cuerpo = ttk.Frame(self, padding=(18, 0, 18, 12))
        cuerpo.pack(fill="both", expand=True)

        menu = ttk.LabelFrame(cuerpo, text="Menú", padding=10)
        menu.pack(side="left", fill="y", padx=(0, 12))
        icono_producto = self._cargar_imagen("icono_producto.png")
        icono_usuario = self._cargar_imagen("icono_usuario.png")
        icono_venta = self._cargar_imagen("icono_venta.png")

        ttk.Button(
            menu,
            text="Productos",
            image=icono_producto or "",
            compound="left",
            style="Menu.TButton",
            command=self.mostrar_productos,
        ).pack(fill="x", pady=4)

        if self.usuario_actual.rol == "Administrador":
            ttk.Button(
                menu,
                text="Usuarios",
                image=icono_usuario or "",
                compound="left",
                style="Menu.TButton",
                command=self.mostrar_usuarios,
            ).pack(fill="x", pady=4)

        ttk.Button(
            menu,
            text="Ventas",
            image=icono_venta or "",
            compound="left",
            style="Menu.TButton",
            command=self.mostrar_ventas,
        ).pack(fill="x", pady=4)
        ttk.Separator(menu, orient="horizontal").pack(fill="x", pady=8)
        ttk.Button(menu, text="Cerrar sesión", style="Menu.TButton", command=self.al_cerrar_sesion).pack(fill="x", pady=4)

        self.contenido = ttk.Frame(cuerpo)
        self.contenido.pack(side="left", fill="both", expand=True)

        estado = ttk.Label(self, textvariable=self.estado_var, anchor="w", padding=(18, 5))
        estado.pack(fill="x")

        self.mostrar_productos()

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _actualizar_resumen(self):
        self.resumen_productos.config(text=f"Productos: {self.servicio.cantidad_productos()}")
        self.resumen_usuarios.config(text=f"Usuarios: {self.servicio.cantidad_usuarios()}")
        self.resumen_ventas.config(text=f"Ventas: {self.servicio.cantidad_ventas()}")

    # ---------------------------
    # Productos (se conserva Semana 14)
    # ---------------------------
    def mostrar_productos(self):
        self._limpiar_contenido()
        self.estado_var.set("Gestión de productos: registrar, consultar, actualizar o eliminar.")

        ttk.Label(self.contenido, text="Gestión de productos", style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 8))
        formulario = ttk.LabelFrame(self.contenido, text="Datos del producto", padding=12)
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Código:").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=5)
        ttk.Entry(formulario, textvariable=self.codigo_var, width=18).grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=5)
        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, sticky="w", padx=(0, 6), pady=5)
        ttk.Entry(formulario, textvariable=self.nombre_var, width=28).grid(row=0, column=3, sticky="ew", pady=5)

        ttk.Label(formulario, text="Categoría:").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=5)
        ttk.Combobox(
            formulario,
            textvariable=self.categoria_var,
            values=self.CATEGORIAS,
            state="readonly",
            width=16,
        ).grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=5)
        ttk.Label(formulario, text="Precio:").grid(row=1, column=2, sticky="w", padx=(0, 6), pady=5)
        ttk.Entry(formulario, textvariable=self.precio_var, width=12).grid(row=1, column=3, sticky="ew", pady=5)
        ttk.Label(formulario, text="Cantidad:").grid(row=2, column=0, sticky="w", padx=(0, 6), pady=5)
        ttk.Entry(formulario, textvariable=self.cantidad_var, width=12).grid(row=2, column=1, sticky="ew", padx=(0, 12), pady=5)

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=2)

        acciones = ttk.Frame(formulario)
        acciones.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(10, 2))
        ttk.Button(acciones, text="Registrar", style="Accion.TButton", command=self.registrar_producto).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Cargar / Consultar", style="Accion.TButton", command=self.consultar_producto).pack(side="left", padx=6)
        ttk.Button(acciones, text="Actualizar", style="Accion.TButton", command=self.actualizar_producto).pack(side="left", padx=6)
        ttk.Button(acciones, text="Eliminar", style="Accion.TButton", command=self.eliminar_producto).pack(side="left", padx=6)
        ttk.Button(acciones, text="Limpiar", style="Accion.TButton", command=self.limpiar_formulario).pack(side="left", padx=6)

        tabla_frame = ttk.LabelFrame(self.contenido, text="Productos registrados", padding=8)
        tabla_frame.pack(fill="both", expand=True)
        columnas = ("codigo", "nombre", "categoria", "precio", "cantidad")
        self.tabla_productos = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=11)
        encabezados = {
            "codigo": "Código", "nombre": "Nombre", "categoria": "Categoría",
            "precio": "Precio", "cantidad": "Stock"
        }
        for clave, texto in encabezados.items():
            self.tabla_productos.heading(clave, text=texto)
        self.tabla_productos.column("codigo", width=90, anchor="center")
        self.tabla_productos.column("nombre", width=210)
        self.tabla_productos.column("categoria", width=135)
        self.tabla_productos.column("precio", width=90, anchor="e")
        self.tabla_productos.column("cantidad", width=80, anchor="center")
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.refrescar_tabla_productos()

    def refrescar_tabla_productos(self):
        if not hasattr(self, "tabla_productos") or not self.tabla_productos.winfo_exists():
            return
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert("", tk.END, values=(
                producto.codigo, producto.nombre, producto.categoria,
                f"${producto.precio:.2f}", producto.cantidad,
            ))
        self._actualizar_resumen()

    def limpiar_formulario(self):
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")
        self.estado_var.set("Formulario limpio.")

    def _cargar_en_formulario(self, producto):
        self.codigo_var.set(producto.codigo)
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(f"{producto.precio:.2f}")
        self.cantidad_var.set(str(producto.cantidad))

    def registrar_producto(self):
        try:
            producto = self.servicio.registrar_producto(
                self.codigo_var.get(), self.nombre_var.get(), self.categoria_var.get(),
                self.precio_var.get(), self.cantidad_var.get(),
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Registro de producto", str(error))
            return
        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.estado_var.set(f"Producto {producto.codigo} registrado correctamente.")
        messagebox.showinfo("Registro", "Producto registrado y guardado en productos.json.")

    def consultar_producto(self):
        producto = self.servicio.obtener_producto(self.codigo_var.get())
        if producto is None:
            messagebox.showwarning("Consulta", "No se encontró un producto con ese código.")
            return
        self._cargar_en_formulario(producto)
        self.estado_var.set(f"Producto {producto.codigo} cargado en el formulario.")

    def actualizar_producto(self):
        try:
            producto = self.servicio.actualizar_producto(
                self.codigo_var.get(), self.nombre_var.get(), self.categoria_var.get(),
                self.precio_var.get(), self.cantidad_var.get(),
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Actualización", str(error))
            return
        self.refrescar_tabla_productos()
        self._cargar_en_formulario(producto)
        self.estado_var.set(f"Producto {producto.codigo} actualizado correctamente.")
        messagebox.showinfo("Actualización", "Los cambios fueron guardados en productos.json.")

    def eliminar_producto(self):
        codigo = self.codigo_var.get().strip()
        producto = self.servicio.obtener_producto(codigo)
        if producto is None:
            messagebox.showwarning("Eliminación", "No se encontró un producto con ese código.")
            return
        confirmar = messagebox.askyesno("Eliminar producto", f"¿Desea eliminar {producto.codigo} - {producto.nombre}?")
        if not confirmar:
            return
        try:
            eliminado = self.servicio.eliminar_producto(codigo)
        except (ValueError, OSError) as error:
            messagebox.showerror("Eliminación", str(error))
            return
        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.estado_var.set(f"Producto {eliminado.codigo} eliminado correctamente.")
        messagebox.showinfo("Eliminación", "Producto eliminado de productos.json.")

    # ---------------------------
    # Usuarios - Semana 16
    # ---------------------------
    def mostrar_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning(
                "Acceso restringido",
                "Solo el usuario con rol Administrador puede gestionar usuarios.",
            )
            self.mostrar_productos()
            return

        self._limpiar_contenido()
        self.estado_var.set(
            "Gestión de usuarios: seleccione una fila o utilice el formulario."
        )
        self.usuario_seleccionado_id = None

        ttk.Label(
            self.contenido,
            text="Gestión de usuarios",
            style="Subtitulo.TLabel",
        ).pack(anchor="w", pady=(0, 8))

        formulario = ttk.LabelFrame(
            self.contenido, text="Datos del usuario", padding=12
        )
        formulario.pack(fill="x", pady=(0, 10))

        ttk.Label(formulario, text="Identificación:").grid(
            row=0, column=0, sticky="w", padx=(0, 6), pady=5
        )
        self.usuario_id_entry = ttk.Entry(
            formulario, textvariable=self.usuario_id_var, width=18
        )
        self.usuario_id_entry.grid(
            row=0, column=1, sticky="ew", padx=(0, 12), pady=5
        )

        ttk.Label(formulario, text="Nombre:").grid(
            row=0, column=2, sticky="w", padx=(0, 6), pady=5
        )
        ttk.Entry(
            formulario, textvariable=self.usuario_nombre_var, width=28
        ).grid(row=0, column=3, sticky="ew", pady=5)

        ttk.Label(formulario, text="Usuario:").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=5
        )
        ttk.Entry(
            formulario, textvariable=self.usuario_login_var, width=18
        ).grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=5)

        ttk.Label(formulario, text="Contraseña:").grid(
            row=1, column=2, sticky="w", padx=(0, 6), pady=5
        )
        ttk.Entry(
            formulario,
            textvariable=self.usuario_clave_var,
            width=28,
            show="*",
        ).grid(row=1, column=3, sticky="ew", pady=5)

        ttk.Label(formulario, text="Rol:").grid(
            row=2, column=0, sticky="w", padx=(0, 6), pady=5
        )
        self.usuario_rol_combo = ttk.Combobox(
            formulario,
            textvariable=self.usuario_rol_var,
            values=("Empleado", "Cliente"),
            state="readonly",
            width=16,
        )
        self.usuario_rol_combo.grid(
            row=2, column=1, sticky="ew", padx=(0, 12), pady=5
        )
        self.usuario_rol_combo.bind(
            "<<ComboboxSelected>>", self._al_cambiar_rol_usuario
        )

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=2)

        acciones = ttk.Frame(formulario)
        acciones.grid(
            row=3, column=0, columnspan=4, sticky="ew", pady=(10, 2)
        )
        ttk.Button(
            acciones,
            text="Registrar",
            style="Accion.TButton",
            command=self.registrar_usuario,
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            acciones,
            text="Actualizar",
            style="Accion.TButton",
            command=self.actualizar_usuario,
        ).pack(side="left", padx=6)
        ttk.Button(
            acciones,
            text="Eliminar",
            style="Accion.TButton",
            command=self.eliminar_usuario,
        ).pack(side="left", padx=6)
        ttk.Button(
            acciones,
            text="Limpiar",
            style="Accion.TButton",
            command=self.limpiar_formulario_usuario,
        ).pack(side="left", padx=6)

        ayuda = ttk.Label(
            formulario,
            text=(
                "Eventos: <<TreeviewSelect>> carga datos | "
                "<Return> registra | <Escape> limpia | "
                "<<ComboboxSelected>> responde al cambio de rol"
            ),
        )
        ayuda.grid(
            row=4, column=0, columnspan=4, sticky="w", pady=(8, 0)
        )

        tabla_frame = ttk.LabelFrame(
            self.contenido, text="Usuarios registrados", padding=8
        )
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("identificacion", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            tabla_frame, columns=columnas, show="headings", height=12
        )
        encabezados = {
            "identificacion": "Identificación",
            "nombre": "Nombre",
            "usuario": "Usuario",
            "rol": "Rol",
        }
        for clave, titulo in encabezados.items():
            self.tabla_usuarios.heading(clave, text=titulo)

        self.tabla_usuarios.column(
            "identificacion", width=125, anchor="center"
        )
        self.tabla_usuarios.column("nombre", width=240)
        self.tabla_usuarios.column("usuario", width=160)
        self.tabla_usuarios.column("rol", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tabla_usuarios.yview
        )
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento virtual solicitado para seleccionar un registro.
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>", self._al_seleccionar_usuario
        )

        # Atajos solicitados: se enlazan únicamente a los controles del formulario.
        controles_evento = (
            self.usuario_id_entry,
            *[w for w in formulario.winfo_children() if isinstance(w, ttk.Entry)],
            self.usuario_rol_combo,
        )
        for control in controles_evento:
            control.bind("<Return>", self._evento_registrar_usuario)
            control.bind("<Escape>", self._evento_limpiar_usuario)

        self.refrescar_tabla_usuarios()
        self.usuario_id_entry.focus_set()

    def refrescar_tabla_usuarios(self):
        if (
            self.tabla_usuarios is None
            or not self.tabla_usuarios.winfo_exists()
        ):
            return

        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol,
                ),
            )
        self._actualizar_resumen()

    def _al_seleccionar_usuario(self, _event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return

        identificacion = str(valores[0])
        usuario = self.servicio.obtener_usuario(identificacion)
        if usuario is None:
            return

        self.usuario_seleccionado_id = usuario.identificacion
        self.usuario_id_var.set(usuario.identificacion)
        self.usuario_nombre_var.set(usuario.nombre)
        self.usuario_login_var.set(usuario.usuario)
        self.usuario_clave_var.set(usuario.contrasena)
        self.usuario_rol_var.set(usuario.rol)

        # El identificador es la clave del registro: no se cambia al editar.
        self.usuario_id_entry.configure(state="disabled")

        if usuario.rol == "Administrador":
            self.estado_var.set(
                "Cuenta Administrador seleccionada: protegida contra "
                "actualización y eliminación desde esta pantalla."
            )
        else:
            self.estado_var.set(
                f"Usuario {usuario.identificacion} cargado en el formulario."
            )

    def _al_cambiar_rol_usuario(self, _event):
        rol = self.usuario_rol_var.get()
        self.estado_var.set(f"Rol seleccionado: {rol}.")

    def _evento_registrar_usuario(self, _event):
        # Reutiliza el mismo método del botón; no duplica la lógica.
        if self.usuario_actual.rol == "Administrador":
            self.registrar_usuario()
        return "break"

    def _evento_limpiar_usuario(self, _event):
        self.limpiar_formulario_usuario()
        return "break"

    def limpiar_formulario_usuario(self):
        self.usuario_seleccionado_id = None
        self.usuario_id_entry.configure(state="normal")
        self.usuario_id_var.set("")
        self.usuario_nombre_var.set("")
        self.usuario_login_var.set("")
        self.usuario_clave_var.set("")
        self.usuario_rol_var.set("")
        if self.tabla_usuarios is not None and self.tabla_usuarios.winfo_exists():
            self.tabla_usuarios.selection_remove(
                self.tabla_usuarios.selection()
            )
        self.estado_var.set("Formulario de usuario limpio.")
        self.usuario_id_entry.focus_set()

    def registrar_usuario(self):
        try:
            usuario = self.servicio.registrar_usuario(
                self.usuario_id_var.get(),
                self.usuario_nombre_var.get(),
                self.usuario_login_var.get(),
                self.usuario_clave_var.get(),
                self.usuario_rol_var.get(),
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Registro de usuario", str(error))
            return

        self.refrescar_tabla_usuarios()
        self.limpiar_formulario_usuario()
        self.estado_var.set(
            f"Usuario {usuario.identificacion} registrado correctamente."
        )
        messagebox.showinfo(
            "Registro",
            "Usuario registrado y persistido en usuarios.json.",
        )

    def actualizar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning(
                "Actualización",
                "Seleccione primero un usuario en la tabla.",
            )
            return

        try:
            usuario = self.servicio.actualizar_usuario(
                self.usuario_seleccionado_id,
                self.usuario_nombre_var.get(),
                self.usuario_login_var.get(),
                self.usuario_clave_var.get(),
                self.usuario_rol_var.get(),
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Actualización de usuario", str(error))
            return

        self.refrescar_tabla_usuarios()
        self.estado_var.set(
            f"Usuario {usuario.identificacion} actualizado correctamente."
        )
        messagebox.showinfo(
            "Actualización",
            "Los cambios fueron guardados en usuarios.json.",
        )

    def eliminar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning(
                "Eliminación",
                "Seleccione primero un usuario en la tabla.",
            )
            return

        usuario = self.servicio.obtener_usuario(
            self.usuario_seleccionado_id
        )
        if usuario is None:
            messagebox.showwarning(
                "Eliminación", "El usuario seleccionado ya no existe."
            )
            return

        confirmar = messagebox.askyesno(
            "Eliminar usuario",
            f"¿Desea eliminar a {usuario.nombre} ({usuario.usuario})?",
        )
        if not confirmar:
            return

        try:
            eliminado = self.servicio.eliminar_usuario(
                self.usuario_seleccionado_id,
                self.usuario_actual.identificacion,
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Eliminación de usuario", str(error))
            return

        self.refrescar_tabla_usuarios()
        self.limpiar_formulario_usuario()
        self.estado_var.set(
            f"Usuario {eliminado.identificacion} eliminado correctamente."
        )
        messagebox.showinfo(
            "Eliminación",
            "Usuario eliminado de usuarios.json.",
        )

    # ---------------------------
    # Ventas - funcionalidad conservada de Semana 15
    # ---------------------------
    def mostrar_ventas(self):
        self._limpiar_contenido()
        self.estado_var.set("Ventas: seleccione un usuario y un producto, luego registre la operación.")

        ttk.Label(self.contenido, text="Registro de ventas", style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 8))

        formulario = ttk.LabelFrame(self.contenido, text="Nueva venta", padding=12)
        formulario.pack(fill="x", pady=(0, 10))

        usuarios = self.servicio.listar_usuarios()
        productos = self.servicio.listar_productos()

        opciones_usuario = [f"{u.identificacion} | {u.nombre}" for u in usuarios]
        opciones_producto = [f"{p.codigo} | {p.nombre}" for p in productos]

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.venta_usuario_combo = ttk.Combobox(
            formulario, textvariable=self.venta_usuario_var,
            values=opciones_usuario, state="readonly", width=36,
        )
        self.venta_usuario_combo.grid(row=0, column=1, sticky="ew", padx=(0, 18), pady=6)

        ttk.Label(formulario, text="Producto:").grid(row=0, column=2, sticky="w", padx=(0, 8), pady=6)
        self.venta_producto_combo = ttk.Combobox(
            formulario, textvariable=self.venta_producto_var,
            values=opciones_producto, state="readonly", width=36,
        )
        self.venta_producto_combo.grid(row=0, column=3, sticky="ew", pady=6)

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        ttk.Button(
            formulario,
            text="Registrar venta",
            style="Accion.TButton",
            command=self.registrar_venta,
        ).grid(row=1, column=0, columnspan=4, pady=(10, 2), ipadx=18)

        ayuda = ttk.Label(
            formulario,
            text="Flujo: acción del usuario → command= → callback → servicio → ventas.json → respuesta visual",
        )
        ayuda.grid(row=2, column=0, columnspan=4, sticky="w", pady=(8, 0))

        tabla_frame = ttk.LabelFrame(self.contenido, text="Ventas registradas", padding=8)
        tabla_frame.pack(fill="both", expand=True)
        columnas = ("id", "fecha", "usuario", "producto")
        self.tabla_ventas = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=13)
        self.tabla_ventas.heading("id", text="Venta")
        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.heading("usuario", text="Usuario")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.column("id", width=80, anchor="center")
        self.tabla_ventas.column("fecha", width=155, anchor="center")
        self.tabla_ventas.column("usuario", width=240)
        self.tabla_ventas.column("producto", width=240)
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.refrescar_tabla_ventas()

    def registrar_venta(self):
        """Callback asociado al botón mediante command=self.registrar_venta."""
        usuario_texto = self.venta_usuario_var.get().strip()
        producto_texto = self.venta_producto_var.get().strip()

        usuario_id = usuario_texto.split("|", 1)[0].strip() if usuario_texto else ""
        producto_codigo = producto_texto.split("|", 1)[0].strip() if producto_texto else ""

        try:
            venta = self.servicio.registrar_venta(usuario_id, producto_codigo)
        except (ValueError, OSError) as error:
            messagebox.showerror("Registrar venta", str(error))
            return

        self.venta_usuario_var.set("")
        self.venta_producto_var.set("")
        self.refrescar_tabla_ventas()
        self._actualizar_resumen()
        self.estado_var.set(f"Venta {venta.identificador} registrada y guardada correctamente.")
        messagebox.showinfo("Venta registrada", f"La venta {venta.identificador} se guardó en ventas.json.")

    def refrescar_tabla_ventas(self):
        if not hasattr(self, "tabla_ventas") or not self.tabla_ventas.winfo_exists():
            return
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for venta in self.servicio.listar_ventas():
            usuario = self.servicio.obtener_usuario(venta.usuario_id)
            producto = self.servicio.obtener_producto(venta.producto_codigo)
            usuario_texto = usuario.nombre if usuario else venta.usuario_id
            producto_texto = producto.nombre if producto else venta.producto_codigo
            self.tabla_ventas.insert("", tk.END, values=(
                venta.identificador, venta.fecha,
                f"{venta.usuario_id} - {usuario_texto}",
                f"{venta.producto_codigo} - {producto_texto}",
            ))
        self._actualizar_resumen()
