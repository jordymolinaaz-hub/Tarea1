"""
=============================================================
  AGENDA PERSONAL - Aplicación GUI con Tkinter
=============================================================
Autor   : Generado con Claude (Anthropic)
Versión : 1.0
Descripción:
    Aplicación de agenda personal que permite al usuario
    agregar, visualizar y eliminar eventos o tareas
    programadas, con soporte de DatePicker integrado.
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, date


# ─────────────────────────────────────────────
#  PALETA DE COLORES (tema oscuro-elegante)
# ─────────────────────────────────────────────
BG_DARK    = "#1A1A2E"   # Fondo principal
BG_PANEL   = "#16213E"   # Fondo de paneles
BG_CARD    = "#0F3460"   # Fondo de tarjetas / cabeceras
ACCENT     = "#E94560"   # Acento / botón primario
ACCENT2    = "#533483"   # Acento secundario
TEXT_LIGHT = "#E8E8E8"   # Texto principal
TEXT_DIM   = "#9A9AB0"   # Texto secundario
SUCCESS    = "#2ECC71"   # Color de éxito
DANGER     = "#E74C3C"   # Color de peligro
ENTRY_BG   = "#1E2A4A"   # Fondo de campos de entrada
TREE_ODD   = "#1A2744"   # Filas impares del TreeView
TREE_EVEN  = "#1E2F55"   # Filas pares del TreeView
TREE_SEL   = "#E94560"   # Selección del TreeView


# ══════════════════════════════════════════════════════════
#  WIDGET PERSONALIZADO: DatePicker (calendario emergente)
# ══════════════════════════════════════════════════════════
class DatePicker(tk.Toplevel):
    """
    Ventana emergente (Toplevel) que muestra un calendario
    mensual interactivo para seleccionar una fecha.

    Parámetros
    ----------
    parent  : widget padre que invoca el picker
    callback: función que recibe la fecha seleccionada (str "DD/MM/YYYY")
    """

    def __init__(self, parent, callback):
        super().__init__(parent)

        self.callback     = callback          # Función a llamar con la fecha elegida
        self.current_date = date.today()      # Mes/año mostrado actualmente
        self.selected     = None             # Fecha seleccionada por el usuario

        # ── Configuración de la ventana ──────────────────
        self.title("Seleccionar Fecha")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.grab_set()                       # Modal: bloquea la ventana principal

        # ── Centrar sobre la ventana padre ───────────────
        self.geometry(self._center(parent, 320, 300))

        self._build_ui()
        self._render_calendar()

    # ── Helpers ──────────────────────────────────────────

    @staticmethod
    def _center(parent, w, h):
        """Calcula la geometría para centrar sobre el padre."""
        px = parent.winfo_rootx() + parent.winfo_width()  // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2
        return f"{w}x{h}+{px - w // 2}+{py - h // 2}"

    # ── Construcción de la interfaz ───────────────────────

    def _build_ui(self):
        """Crea todos los widgets del DatePicker."""

        # -- Cabecera: navegación de mes/año ---------------
        header = tk.Frame(self, bg=BG_CARD, pady=8)
        header.pack(fill="x")

        btn_cfg = dict(bg=BG_CARD, fg=TEXT_LIGHT,
                       font=("Consolas", 14, "bold"),
                       bd=0, activebackground=ACCENT,
                       activeforeground=TEXT_LIGHT, cursor="hand2")

        tk.Button(header, text="◀", command=self._prev_month, **btn_cfg).pack(side="left",  padx=12)
        tk.Button(header, text="▶", command=self._next_month, **btn_cfg).pack(side="right", padx=12)

        self.lbl_month = tk.Label(header, bg=BG_CARD, fg=TEXT_LIGHT,
                                  font=("Georgia", 12, "bold"))
        self.lbl_month.pack(side="left", expand=True)

        # -- Días de la semana -----------------------------
        days_frame = tk.Frame(self, bg=BG_PANEL, pady=4)
        days_frame.pack(fill="x")

        for abbr in ("Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"):
            tk.Label(days_frame, text=abbr, width=4,
                     bg=BG_PANEL, fg=ACCENT,
                     font=("Consolas", 9, "bold")).pack(side="left", expand=True)

        # -- Cuadrícula de días ----------------------------
        self.grid_frame = tk.Frame(self, bg=BG_DARK)
        self.grid_frame.pack(fill="both", expand=True, padx=6, pady=4)

        # -- Botón "Hoy" ----------------------------------
        tk.Button(self, text="Hoy", command=self._select_today,
                  bg=ACCENT2, fg=TEXT_LIGHT,
                  font=("Consolas", 9, "bold"),
                  relief="flat", cursor="hand2",
                  activebackground=ACCENT, activeforeground=TEXT_LIGHT
                  ).pack(fill="x", padx=12, pady=(0, 8))

    # ── Renderizado del calendario ────────────────────────

    def _render_calendar(self):
        """Dibuja los botones de días para el mes actual."""

        # Limpiar cuadrícula anterior
        for w in self.grid_frame.winfo_children():
            w.destroy()

        # Actualizar etiqueta de mes/año
        month_name = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ][self.current_date.month - 1]
        self.lbl_month.config(text=f"{month_name}  {self.current_date.year}")

        # Obtener matriz de días (semanas × días)
        cal   = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        today = date.today()

        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day == 0:
                    # Celda vacía (días de otros meses)
                    tk.Label(self.grid_frame, text="", width=4,
                             bg=BG_DARK).grid(row=row_idx, column=col_idx, padx=1, pady=1)
                    continue

                # Determinar estilo del botón
                is_today    = (day == today.day
                               and self.current_date.month == today.month
                               and self.current_date.year  == today.year)
                btn_bg  = ACCENT   if is_today else ENTRY_BG
                btn_fg  = TEXT_LIGHT
                btn_rel = "flat"

                tk.Button(
                    self.grid_frame,
                    text=str(day), width=3,
                    bg=btn_bg, fg=btn_fg,
                    font=("Consolas", 9, "bold" if is_today else "normal"),
                    relief=btn_rel, bd=0,
                    activebackground=ACCENT, activeforeground=TEXT_LIGHT,
                    cursor="hand2",
                    command=lambda d=day: self._select_day(d)
                ).grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")

        # Hacer que todas las celdas se expandan por igual
        for c in range(7):
            self.grid_frame.columnconfigure(c, weight=1)

    # ── Navegación de meses ───────────────────────────────

    def _prev_month(self):
        """Retrocede un mes en el calendario."""
        year, month = self.current_date.year, self.current_date.month
        month -= 1
        if month < 1:
            month, year = 12, year - 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self._render_calendar()

    def _next_month(self):
        """Avanza un mes en el calendario."""
        year, month = self.current_date.year, self.current_date.month
        month += 1
        if month > 12:
            month, year = 1, year + 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self._render_calendar()

    # ── Selección de fecha ────────────────────────────────

    def _select_day(self, day):
        """Selecciona el día indicado, invoca el callback y cierra el picker."""
        selected = date(self.current_date.year, self.current_date.month, day)
        self.callback(selected.strftime("%d/%m/%Y"))
        self.destroy()

    def _select_today(self):
        """Atajo para seleccionar la fecha de hoy."""
        self.callback(date.today().strftime("%d/%m/%Y"))
        self.destroy()


# ══════════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL: AgendaApp
# ══════════════════════════════════════════════════════════
class AgendaApp:
    """
    Clase principal de la Agenda Personal.
    Gestiona la ventana raíz, los frames y toda la lógica
    de agregar / eliminar eventos.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_root()
        self._apply_styles()
        self._build_ui()

    # ── Configuración inicial ─────────────────────────────

    def _configure_root(self):
        """Ajusta propiedades básicas de la ventana principal."""
        self.root.title("📅  Agenda Personal")
        self.root.geometry("860x560")
        self.root.minsize(720, 480)
        self.root.configure(bg=BG_DARK)
        # Icono de ventana (emoji fallback si no hay .ico)
        try:
            self.root.iconbitmap("agenda.ico")
        except Exception:
            pass

    def _apply_styles(self):
        """Configura el tema visual del TreeView (ttk.Style)."""
        style = ttk.Style()
        style.theme_use("clam")

        # Encabezado de columnas
        style.configure("Agenda.Treeview.Heading",
                        background=BG_CARD,
                        foreground=ACCENT,
                        font=("Consolas", 10, "bold"),
                        relief="flat")
        style.map("Agenda.Treeview.Heading",
                  background=[("active", ACCENT2)])

        # Filas del TreeView
        style.configure("Agenda.Treeview",
                        background=TREE_ODD,
                        foreground=TEXT_LIGHT,
                        rowheight=28,
                        fieldbackground=TREE_ODD,
                        font=("Consolas", 10),
                        borderwidth=0)
        style.map("Agenda.Treeview",
                  background=[("selected", TREE_SEL)],
                  foreground=[("selected", TEXT_LIGHT)])

        # Scrollbar
        style.configure("Dark.Vertical.TScrollbar",
                        background=BG_PANEL,
                        troughcolor=BG_DARK,
                        arrowcolor=TEXT_DIM)

    # ── Construcción de la interfaz ───────────────────────

    def _build_ui(self):
        """Ensambla todos los frames y widgets de la app."""
        self._build_header()
        self._build_body()

    def _build_header(self):
        """Crea la barra de título decorativa en la parte superior."""
        header = tk.Frame(self.root, bg=BG_CARD, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="📅  AGENDA PERSONAL",
                 bg=BG_CARD, fg=TEXT_LIGHT,
                 font=("Georgia", 16, "bold")).pack(side="left", padx=20, pady=10)

        # Fecha y hora actuales (se actualiza cada segundo)
        self.lbl_clock = tk.Label(header, bg=BG_CARD, fg=TEXT_DIM,
                                  font=("Consolas", 11))
        self.lbl_clock.pack(side="right", padx=20)
        self._update_clock()

    def _build_body(self):
        """Divide el cuerpo en panel izquierdo (lista) y derecho (formulario)."""
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # Columnas: lista (2 partes) y formulario (1 parte)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_event_list(body)
        self._build_form(body)

    # ── Panel izquierdo: lista de eventos ─────────────────

    def _build_event_list(self, parent):
        """Crea el TreeView con la lista de eventos y su barra de desplazamiento."""

        frame = tk.Frame(parent, bg=BG_PANEL, bd=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        # Sub-título del panel
        tk.Label(frame, text="  EVENTOS PROGRAMADOS",
                 bg=BG_CARD, fg=TEXT_DIM,
                 font=("Consolas", 9, "bold"),
                 anchor="w").grid(row=0, column=0, columnspan=2, sticky="ew")

        # TreeView con columnas: Fecha | Hora | Descripción
        self.tree = ttk.Treeview(
            frame,
            columns=("fecha", "hora", "descripcion"),
            show="headings",
            style="Agenda.Treeview",
            selectmode="browse"        # Solo una fila seleccionable a la vez
        )

        # Definición de columnas
        self.tree.heading("fecha",       text="📆 Fecha")
        self.tree.heading("hora",        text="⏰ Hora")
        self.tree.heading("descripcion", text="📝 Descripción")

        self.tree.column("fecha",        width=100, anchor="center", stretch=False)
        self.tree.column("hora",         width=70,  anchor="center", stretch=False)
        self.tree.column("descripcion",  width=240, anchor="w")

        # Colores alternos de filas (tags)
        self.tree.tag_configure("odd",  background=TREE_ODD)
        self.tree.tag_configure("even", background=TREE_EVEN)

        self.tree.grid(row=1, column=0, sticky="nsew")

        # Scrollbar vertical
        sb = ttk.Scrollbar(frame, orient="vertical",
                           command=self.tree.yview,
                           style="Dark.Vertical.TScrollbar")
        sb.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=sb.set)

        # Barra de estado inferior
        self.lbl_status = tk.Label(frame, text="Sin eventos",
                                   bg=BG_DARK, fg=TEXT_DIM,
                                   font=("Consolas", 9), anchor="w", padx=6)
        self.lbl_status.grid(row=2, column=0, columnspan=2, sticky="ew")

    # ── Panel derecho: formulario de entrada ──────────────

    def _build_form(self, parent):
        """Crea el panel de formulario con campos de entrada y botones."""

        frame = tk.Frame(parent, bg=BG_PANEL, bd=0)
        frame.grid(row=0, column=1, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        # ---- Sub-título ----
        tk.Label(frame, text="  NUEVO EVENTO",
                 bg=BG_CARD, fg=TEXT_DIM,
                 font=("Consolas", 9, "bold"),
                 anchor="w").grid(row=0, column=0, sticky="ew", columnspan=2)

        # ---- Sección: datos del evento ----
        fields_frame = tk.Frame(frame, bg=BG_PANEL, padx=14, pady=10)
        fields_frame.grid(row=1, column=0, sticky="nsew")
        fields_frame.columnconfigure(0, weight=1)

        # Estilo compartido para etiquetas de campo
        lbl_cfg = dict(bg=BG_PANEL, fg=TEXT_DIM,
                       font=("Consolas", 9, "bold"), anchor="w")
        # Estilo compartido para Entry
        entry_cfg = dict(bg=ENTRY_BG, fg=TEXT_LIGHT,
                         insertbackground=ACCENT,
                         font=("Consolas", 11),
                         relief="flat", bd=6,
                         highlightthickness=1,
                         highlightcolor=ACCENT,
                         highlightbackground=BG_CARD)

        # ── Campo FECHA ────────────────────────────────
        tk.Label(fields_frame, text="FECHA", **lbl_cfg).grid(
            row=0, column=0, sticky="w", pady=(0, 2))

        date_row = tk.Frame(fields_frame, bg=BG_PANEL)
        date_row.grid(row=1, column=0, sticky="ew")
        date_row.columnconfigure(0, weight=1)

        self.entry_fecha = tk.Entry(date_row, **entry_cfg)
        self.entry_fecha.grid(row=0, column=0, sticky="ew")
        self.entry_fecha.insert(0, date.today().strftime("%d/%m/%Y"))  # Valor por defecto

        # Botón que abre el DatePicker
        tk.Button(date_row, text="📅",
                  bg=ACCENT2, fg=TEXT_LIGHT,
                  font=("Segoe UI Emoji", 12),
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=ACCENT, activeforeground=TEXT_LIGHT,
                  command=self._open_datepicker
                  ).grid(row=0, column=1, padx=(4, 0))

        # ── Campo HORA ────────────────────────────────
        tk.Label(fields_frame, text="HORA  (HH:MM)", **lbl_cfg).grid(
            row=2, column=0, sticky="w", pady=(14, 2))

        self.entry_hora = tk.Entry(fields_frame, **entry_cfg)
        self.entry_hora.grid(row=3, column=0, sticky="ew")
        self.entry_hora.insert(0, datetime.now().strftime("%H:%M"))    # Valor por defecto

        # ── Campo DESCRIPCIÓN ─────────────────────────
        tk.Label(fields_frame, text="DESCRIPCIÓN", **lbl_cfg).grid(
            row=4, column=0, sticky="w", pady=(14, 2))

        self.entry_desc = tk.Entry(fields_frame, **entry_cfg)
        self.entry_desc.grid(row=5, column=0, sticky="ew")
        self.entry_desc.bind("<Return>", lambda e: self._agregar_evento())  # Enter = Agregar

        # ---- Sección: botones de acción ----
        btn_frame = tk.Frame(frame, bg=BG_PANEL, padx=14, pady=10)
        btn_frame.grid(row=2, column=0, sticky="ew")
        btn_frame.columnconfigure(0, weight=1)

        btn_style = dict(font=("Consolas", 10, "bold"),
                         relief="flat", bd=0,
                         cursor="hand2", pady=8)

        # Botón Agregar Evento
        tk.Button(btn_frame, text="＋  AGREGAR EVENTO",
                  bg=SUCCESS, fg="#0D1117",
                  activebackground="#27AE60", activeforeground="#0D1117",
                  command=self._agregar_evento, **btn_style
                  ).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        # Botón Eliminar Evento Seleccionado
        tk.Button(btn_frame, text="✕  ELIMINAR SELECCIONADO",
                  bg=DANGER, fg=TEXT_LIGHT,
                  activebackground="#C0392B", activeforeground=TEXT_LIGHT,
                  command=self._eliminar_evento, **btn_style
                  ).grid(row=1, column=0, sticky="ew", pady=(0, 6))

        # Separador visual
        tk.Frame(btn_frame, bg=BG_CARD, height=1).grid(
            row=2, column=0, sticky="ew", pady=8)

        # Botón Salir
        tk.Button(btn_frame, text="⏻  SALIR",
                  bg=BG_CARD, fg=TEXT_DIM,
                  activebackground=ACCENT, activeforeground=TEXT_LIGHT,
                  command=self._salir, **btn_style
                  ).grid(row=3, column=0, sticky="ew")

    # ── Reloj en tiempo real ──────────────────────────────

    def _update_clock(self):
        """Actualiza la etiqueta del reloj cada 1 000 ms."""
        now = datetime.now().strftime("%A  %d/%m/%Y  %H:%M:%S")
        self.lbl_clock.config(text=now.upper())
        self.root.after(1000, self._update_clock)

    # ── Acciones de botones ───────────────────────────────

    def _open_datepicker(self):
        """Abre el calendario emergente y espera a que devuelva una fecha."""
        DatePicker(self.root, callback=self._set_fecha)

    def _set_fecha(self, fecha_str: str):
        """Recibe la fecha elegida en el DatePicker y la escribe en el Entry."""
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, fecha_str)

    def _agregar_evento(self):
        """
        Valida los campos y agrega un nuevo evento al TreeView.
        - La fecha debe tener formato DD/MM/YYYY.
        - La hora debe tener formato HH:MM.
        - La descripción no puede estar vacía.
        Los eventos se insertan ordenados por fecha y hora.
        """
        fecha = self.entry_fecha.get().strip()
        hora  = self.entry_hora.get().strip()
        desc  = self.entry_desc.get().strip()

        # ── Validación de fecha ───────────────────────
        try:
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(
                "Fecha inválida",
                "Por favor ingresa la fecha en formato  DD/MM/YYYY\n\nEjemplo: 25/12/2025",
                parent=self.root)
            self.entry_fecha.focus_set()
            return

        # ── Validación de hora ────────────────────────
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Hora inválida",
                "Por favor ingresa la hora en formato  HH:MM\n\nEjemplo: 09:30",
                parent=self.root)
            self.entry_hora.focus_set()
            return

        # ── Validación de descripción ─────────────────
        if not desc:
            messagebox.showerror(
                "Descripción vacía",
                "Por favor escribe una descripción para el evento.",
                parent=self.root)
            self.entry_desc.focus_set()
            return

        # ── Inserción ordenada (fecha + hora) ─────────
        # Clave de ordenación: "YYYY/MM/DD HH:MM" → string comparable
        sort_key = fecha_dt.strftime("%Y%m%d") + hora.replace(":", "")

        # Buscar la posición de inserción
        insert_at = tk.END
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            existing_fecha = datetime.strptime(vals[0], "%d/%m/%Y").strftime("%Y%m%d")
            existing_key   = existing_fecha + vals[1].replace(":", "")
            if sort_key < existing_key:
                insert_at = self.tree.index(item)
                break

        # Insertar en el TreeView con tag de color alterno
        count = len(self.tree.get_children())
        tag   = "even" if count % 2 == 0 else "odd"
        self.tree.insert("", insert_at,
                         values=(fecha, hora, desc),
                         tags=(tag,))

        # Actualizar tags de todas las filas (alternancia correcta)
        self._refresh_row_tags()

        # Limpiar campo descripción y dar foco para nuevo evento
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.focus_set()

        # Actualizar barra de estado
        self._update_status()

    def _eliminar_evento(self):
        """
        Elimina el evento seleccionado en el TreeView.
        Muestra un diálogo de confirmación antes de proceder.
        """
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Sin selección",
                "Por favor selecciona un evento de la lista para eliminarlo.",
                parent=self.root)
            return

        # Obtener datos del evento para mostrarlo en la confirmación
        vals  = self.tree.item(selected[0], "values")
        texto = f"Fecha: {vals[0]}  |  Hora: {vals[1]}\nDescripción: {vals[2]}"

        # Diálogo de confirmación (requisito opcional cumplido)
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el siguiente evento?\n\n{texto}",
            icon="warning",
            parent=self.root)

        if confirmar:
            self.tree.delete(selected[0])
            self._refresh_row_tags()
            self._update_status()

    def _salir(self):
        """Pregunta al usuario si desea salir y cierra la aplicación."""
        if messagebox.askyesno("Salir", "¿Deseas cerrar la Agenda Personal?",
                               parent=self.root):
            self.root.destroy()

    # ── Utilidades internas ───────────────────────────────

    def _refresh_row_tags(self):
        """Re-asigna los tags de color alterno a todas las filas del TreeView."""
        for idx, item in enumerate(self.tree.get_children()):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.item(item, tags=(tag,))

    def _update_status(self):
        """Actualiza la etiqueta de estado con el número total de eventos."""
        total = len(self.tree.get_children())
        if total == 0:
            self.lbl_status.config(text="Sin eventos", fg=TEXT_DIM)
        elif total == 1:
            self.lbl_status.config(text="1 evento registrado", fg=SUCCESS)
        else:
            self.lbl_status.config(text=f"{total} eventos registrados", fg=SUCCESS)


# ══════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════
def main():
    """Inicializa la ventana Tk y arranca el bucle principal."""
    root = tk.Tk()
    app  = AgendaApp(root)         # noqa: F841 — mantener referencia
    root.protocol("WM_DELETE_WINDOW", app._salir)   # Manejar cierre con [X]
    root.mainloop()


if __name__ == "__main__":
    main()