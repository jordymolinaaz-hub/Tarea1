import tkinter as tk
from tkinter import font as tkfont
import datetime

class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("620x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f14")

        self.tareas = []  # Lista de dicts: {texto, completada, widget_frame, ...}

        self._setup_fonts()
        self._build_ui()
        self._bind_keys()

    # ─── Fuentes ────────────────────────────────────────────────────────────────

    def _setup_fonts(self):
        self.font_title  = tkfont.Font(family="Courier", size=18, weight="bold")
        self.font_entry  = tkfont.Font(family="Courier", size=13)
        self.font_btn    = tkfont.Font(family="Courier", size=11, weight="bold")
        self.font_task   = tkfont.Font(family="Courier", size=12)
        self.font_hint   = tkfont.Font(family="Courier", size=9)

    # ─── UI ─────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Cabecera ──────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg="#0f0f14", pady=20)
        header.pack(fill="x", padx=30)

        tk.Label(
            header, text="▸ TAREAS", font=self.font_title,
            bg="#0f0f14", fg="#e2ff5d"
        ).pack(side="left")

        self.lbl_contador = tk.Label(
            header, text="0 / 0", font=self.font_hint,
            bg="#0f0f14", fg="#555566"
        )
        self.lbl_contador.pack(side="right", pady=6)

        # ── Barra de entrada ──────────────────────────────────────────────────
        entrada_frame = tk.Frame(self.root, bg="#1a1a24", pady=14, padx=16)
        entrada_frame.pack(fill="x", padx=30)

        self.entry = tk.Entry(
            entrada_frame, font=self.font_entry,
            bg="#1a1a24", fg="#f0f0f5",
            insertbackground="#e2ff5d",
            relief="flat", bd=0,
            highlightthickness=0
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.focus()

        btn_add = tk.Button(
            entrada_frame, text="+ AÑADIR",
            font=self.font_btn,
            bg="#e2ff5d", fg="#0f0f14",
            relief="flat", bd=0,
            activebackground="#d4f040",
            activeforeground="#0f0f14",
            cursor="hand2",
            command=self.anadir_tarea,
            padx=14, pady=4
        )
        btn_add.pack(side="right")

        # ── Divisor ───────────────────────────────────────────────────────────
        tk.Frame(self.root, bg="#2a2a36", height=1).pack(fill="x", padx=30, pady=(8, 0))

        # ── Lista de tareas (canvas + scrollbar) ──────────────────────────────
        contenedor = tk.Frame(self.root, bg="#0f0f14")
        contenedor.pack(fill="both", expand=True, padx=30, pady=10)

        self.canvas = tk.Canvas(contenedor, bg="#0f0f14", highlightthickness=0)
        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.lista_frame = tk.Frame(self.canvas, bg="#0f0f14")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.lista_frame, anchor="nw"
        )
        self.lista_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # ── Divisor ───────────────────────────────────────────────────────────
        tk.Frame(self.root, bg="#2a2a36", height=1).pack(fill="x", padx=30)

        # ── Botones de acción ─────────────────────────────────────────────────
        acciones_frame = tk.Frame(self.root, bg="#0f0f14", pady=14)
        acciones_frame.pack(fill="x", padx=30)

        btn_completar = tk.Button(
            acciones_frame, text="✔ COMPLETAR  [C]",
            font=self.font_btn,
            bg="#1a1a24", fg="#7cffb2",
            relief="flat", bd=0,
            activebackground="#2a2a36",
            activeforeground="#7cffb2",
            cursor="hand2",
            command=self.completar_tarea,
            padx=16, pady=8
        )
        btn_completar.pack(side="left", padx=(0, 10))

        btn_eliminar = tk.Button(
            acciones_frame, text="✖ ELIMINAR  [Del]",
            font=self.font_btn,
            bg="#1a1a24", fg="#ff6b6b",
            relief="flat", bd=0,
            activebackground="#2a2a36",
            activeforeground="#ff6b6b",
            cursor="hand2",
            command=self.eliminar_tarea,
            padx=16, pady=8
        )
        btn_eliminar.pack(side="left")

        btn_limpiar = tk.Button(
            acciones_frame, text="⊘ LIMPIAR COMPLETADAS",
            font=self.font_hint,
            bg="#0f0f14", fg="#444455",
            relief="flat", bd=0,
            activebackground="#1a1a24",
            activeforeground="#7777aa",
            cursor="hand2",
            command=self.limpiar_completadas,
            padx=16, pady=8
        )
        btn_limpiar.pack(side="right")

        # ── Pie de atajos ─────────────────────────────────────────────────────
        pie = tk.Frame(self.root, bg="#0a0a10", pady=8)
        pie.pack(fill="x")

        atajos = "Enter: añadir  ·  C: completar  ·  D / Del: eliminar  ·  Esc: salir"
        tk.Label(
            pie, text=atajos, font=self.font_hint,
            bg="#0a0a10", fg="#333344"
        ).pack()

    # ─── Atajos de teclado ───────────────────────────────────────────────────────

    def _bind_keys(self):
        self.root.bind("<Return>",   lambda e: self.anadir_tarea())
        self.root.bind("<c>",        lambda e: self.completar_tarea())
        self.root.bind("<C>",        lambda e: self.completar_tarea())
        self.root.bind("<Delete>",   lambda e: self.eliminar_tarea())
        self.root.bind("<d>",        lambda e: self.eliminar_tarea())
        self.root.bind("<D>",        lambda e: self.eliminar_tarea())
        self.root.bind("<Escape>",   lambda e: self.root.destroy())

    # ─── Operaciones de tareas ───────────────────────────────────────────────────

    def anadir_tarea(self):
        texto = self.entry.get().strip()
        if not texto:
            self._shake_entry()
            return

        tarea = {
            "texto":      texto,
            "completada": False,
            "seleccionada": False,
            "frame":      None,
            "check_lbl":  None,
            "texto_lbl":  None,
        }
        self.tareas.append(tarea)
        self._render_tarea(tarea)
        self._seleccionar(tarea)
        self.entry.delete(0, tk.END)
        self._actualizar_contador()

    def completar_tarea(self):
        sel = self._tarea_seleccionada()
        if not sel:
            return
        sel["completada"] = not sel["completada"]
        self._actualizar_visual(sel)
        self._actualizar_contador()

    def eliminar_tarea(self):
        sel = self._tarea_seleccionada()
        if not sel:
            return
        idx = self.tareas.index(sel)
        sel["frame"].destroy()
        self.tareas.remove(sel)
        # Seleccionar la siguiente (o anterior) tarea
        if self.tareas:
            nuevo_idx = min(idx, len(self.tareas) - 1)
            self._seleccionar(self.tareas[nuevo_idx])
        self._actualizar_contador()

    def limpiar_completadas(self):
        completadas = [t for t in self.tareas if t["completada"]]
        for t in completadas:
            t["frame"].destroy()
            self.tareas.remove(t)
        self._actualizar_contador()

    # ─── Selección ───────────────────────────────────────────────────────────────

    def _seleccionar(self, tarea):
        for t in self.tareas:
            t["seleccionada"] = False
            self._actualizar_visual(t)
        tarea["seleccionada"] = True
        self._actualizar_visual(tarea)

    def _tarea_seleccionada(self):
        for t in self.tareas:
            if t["seleccionada"]:
                return t
        return None

    # ─── Render ──────────────────────────────────────────────────────────────────

    def _render_tarea(self, tarea):
        frame = tk.Frame(
            self.lista_frame,
            bg="#1a1a24",
            pady=10, padx=14,
            cursor="hand2"
        )
        frame.pack(fill="x", pady=(0, 4))

        # Indicador de estado (check)
        check_lbl = tk.Label(
            frame, text="○",
            font=self.font_entry,
            bg="#1a1a24", fg="#444455",
            width=2
        )
        check_lbl.pack(side="left")

        # Texto de la tarea
        texto_lbl = tk.Label(
            frame, text=tarea["texto"],
            font=self.font_task,
            bg="#1a1a24", fg="#d0d0e0",
            anchor="w"
        )
        texto_lbl.pack(side="left", fill="x", expand=True, padx=(8, 0))

        tarea["frame"]     = frame
        tarea["check_lbl"] = check_lbl
        tarea["texto_lbl"] = texto_lbl

        # Clic para seleccionar; doble clic para completar
        for widget in (frame, check_lbl, texto_lbl):
            widget.bind("<Button-1>",        lambda e, t=tarea: self._seleccionar(t))
            widget.bind("<Double-Button-1>",  lambda e, t=tarea: (self._seleccionar(t), self.completar_tarea()))

        self._actualizar_visual(tarea)

    def _actualizar_visual(self, tarea):
        sel  = tarea["seleccionada"]
        comp = tarea["completada"]

        bg        = "#252535" if sel else "#1a1a24"
        fg_texto  = "#555566" if comp else ("#f0f0ff" if sel else "#b0b0cc")
        fg_check  = "#7cffb2" if comp else ("#e2ff5d" if sel else "#444455")
        check_chr = "✔" if comp else ("▸" if sel else "○")
        overstrike = comp

        tarea["frame"].configure(bg=bg)
        tarea["check_lbl"].configure(bg=bg, fg=fg_check, text=check_chr)
        tarea["texto_lbl"].configure(
            bg=bg, fg=fg_texto,
            font=tkfont.Font(
                family="Courier", size=12,
                overstrike=overstrike,
                slant="italic" if comp else "roman"
            )
        )

    # ─── Scroll ──────────────────────────────────────────────────────────────────

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ─── Contador ────────────────────────────────────────────────────────────────

    def _actualizar_contador(self):
        total     = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t["completada"])
        self.lbl_contador.configure(
            text=f"{completadas} / {total} completadas",
            fg="#7cffb2" if completadas == total and total > 0 else "#555566"
        )

    # ─── Animación de entrada vacía ───────────────────────────────────────────────

    def _shake_entry(self):
        original_bg = self.entry.master.cget("bg")
        self.entry.master.configure(bg="#3a1a24")
        self.root.after(120, lambda: self.entry.master.configure(bg=original_bg))


# ─── Main ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()