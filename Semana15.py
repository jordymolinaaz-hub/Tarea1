"""
Gestor de Tareas — Tkinter
Compatible con Windows / macOS / Linux (Python 3.8+)
Sin dependencias externas.
"""
import tkinter as tk
from tkinter import messagebox

# ──────────────────────────────────────────────
#  PALETA & CONSTANTES DE DISEÑO
# ──────────────────────────────────────────────
BG_MAIN      = "#0F0F13"
BG_PANEL     = "#16161D"
BG_ENTRY     = "#1E1E2A"
BG_ITEM      = "#1A1A24"
BG_ITEM_HOV  = "#22222F"
BG_DONE      = "#0D1A0D"

ACCENT       = "#7C6AF7"
COLOR_OK     = "#2A5A2A"
COLOR_DEL    = "#5A1A1A"
COLOR_CLR    = "#252530"

TEXT_PRI     = "#F0EFF8"
TEXT_SEC     = "#7A7A9A"
TEXT_DONE    = "#3A7A3A"
TEXT_TEAL    = "#4ECDC4"
TEXT_RED     = "#FF6B6B"
BORDER       = "#2A2A3A"

FONT_TITLE   = ("Georgia",     22, "bold")
FONT_SUB     = ("Courier New", 10)
FONT_BTN     = ("Courier New", 10, "bold")
FONT_ENTRY   = ("Courier New", 13)
FONT_ITEM    = ("Courier New", 12)
FONT_BADGE   = ("Courier New",  9, "bold")

PAD = 14


def _lighten(hex_color, amount=20):
    hex_color = hex_color.lstrip("#")
    r = min(255, int(hex_color[0:2], 16) + amount)
    g = min(255, int(hex_color[2:4], 16) + amount)
    b = min(255, int(hex_color[4:6], 16) + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def make_button(parent, text, command,
                bg=ACCENT, fg=TEXT_PRI, width=14):
    hover = _lighten(bg)
    btn = tk.Button(
        parent, text=text, command=command,
        font=FONT_BTN, bg=bg, fg=fg,
        activebackground=hover, activeforeground=fg,
        relief="flat", bd=0, padx=10, pady=6,
        width=width, cursor="hand2",
    )
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn


class GestorTareas:

    def __init__(self, root: tk.Tk):
        self.root  = root
        self.tasks = []
        self._setup_window()
        self._build_ui()
        self._update_counter()

    def _setup_window(self):
        self.root.title("✦ Gestor de Tareas")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(True, True)
        self.root.minsize(520, 500)
        w, h = 640, 720
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        outer = tk.Frame(self.root, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=22, pady=22)

        # cabecera
        hdr = tk.Frame(outer, bg=BG_MAIN)
        hdr.pack(fill="x", pady=(0, 4))
        tk.Label(hdr, text="✦ TASK BOARD",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_PRI).pack(side="left")
        self.counter_lbl = tk.Label(hdr, text="",
                                    font=FONT_BADGE, bg=ACCENT, fg=TEXT_PRI,
                                    padx=10, pady=3)
        self.counter_lbl.pack(side="right", pady=8)
        tk.Label(outer, text="ADMINISTRA TUS PENDIENTES",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_SEC).pack(anchor="w", pady=(0, 14))

        # panel entrada
        entry_panel = tk.Frame(outer, bg=BG_PANEL,
                               highlightbackground=BORDER, highlightthickness=1)
        entry_panel.pack(fill="x", pady=(0, 10))
        inner = tk.Frame(entry_panel, bg=BG_PANEL)
        inner.pack(fill="x", padx=PAD, pady=10)
        tk.Label(inner, text="NUEVA TAREA",
                 font=FONT_BADGE, bg=BG_PANEL, fg=TEXT_SEC).pack(anchor="w", pady=(0, 4))
        entry_row = tk.Frame(inner, bg=BG_PANEL)
        entry_row.pack(fill="x")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            entry_row, textvariable=self.entry_var,
            font=FONT_ENTRY, bg=BG_ENTRY, fg=TEXT_PRI,
            insertbackground=ACCENT, relief="flat", bd=0,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=6)
        self.entry.bind("<Return>",   lambda _: self.add_task())
        self.entry.bind("<FocusIn>",  self._entry_focus_in)
        self.entry.bind("<FocusOut>", self._entry_focus_out)
        self.entry.focus()

        make_button(entry_row, "+ AÑADIR", self.add_task,
                    bg=ACCENT, width=12).pack(side="right", padx=(8, 0))

        # botones acción
        btn_row = tk.Frame(outer, bg=BG_MAIN)
        btn_row.pack(fill="x", pady=(0, 12))
        make_button(btn_row, "✔  COMPLETAR",     self.mark_done,
                    bg=COLOR_OK,  fg=TEXT_TEAL, width=14).pack(side="left", padx=(0, 6))
        make_button(btn_row, "✕  ELIMINAR",      self.delete_task,
                    bg=COLOR_DEL, fg=TEXT_RED,  width=14).pack(side="left", padx=(0, 6))
        make_button(btn_row, "⊘  LIMPIAR HECHAS", self.clear_done,
                    bg=COLOR_CLR, fg=TEXT_SEC,  width=18).pack(side="right")

        # lista scrollable
        list_panel = tk.Frame(outer, bg=BG_PANEL,
                              highlightbackground=BORDER, highlightthickness=1)
        list_panel.pack(fill="both", expand=True)
        tk.Label(list_panel, text="  TAREAS",
                 font=FONT_BADGE, bg=BG_PANEL, fg=TEXT_SEC,
                 anchor="w").pack(fill="x", padx=PAD, pady=(8, 4))

        cf = tk.Frame(list_panel, bg=BG_PANEL)
        cf.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        self.canvas = tk.Canvas(cf, bg=BG_PANEL, highlightthickness=0)
        vsb = tk.Scrollbar(cf, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.task_frame = tk.Frame(self.canvas, bg=BG_PANEL)
        self._cw = self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind("<Configure>", self._on_frame_cfg)
        self.canvas.bind("<Configure>",     self._on_canvas_cfg)
        self.canvas.bind("<MouseWheel>",    self._on_scroll)
        self.task_frame.bind("<MouseWheel>",self._on_scroll)

        self.empty_lbl = tk.Label(
            self.task_frame,
            text="No hay tareas · escribe una arriba",
            font=FONT_SUB, bg=BG_PANEL, fg=TEXT_SEC,
        )
        self.empty_lbl.pack(pady=40)

    # ── lógica ───────────────────────────────

    def add_task(self):
        text = self.entry_var.get().strip()
        if not text:
            self._shake_entry()
            return
        task = {"text": text, "done": False, "selected": False,
                "frame": None, "label": None, "badge": None,
                "chk": None, "chk_var": None}
        self.tasks.append(task)
        self.entry_var.set("")
        self._render_task(task)
        self._update_counter()

    def mark_done(self):
        sel = self._get_selected()
        if not sel:
            messagebox.showinfo("Sin selección",
                                "Haz clic en una tarea para seleccionarla primero.")
            return
        for t in sel:
            if not t["done"]:
                t["done"] = True
                self._refresh_item(t)
        self._update_counter()

    def delete_task(self):
        sel = self._get_selected()
        if not sel:
            messagebox.showinfo("Sin selección",
                                "Haz clic en una tarea para seleccionarla primero.")
            return
        for t in sel:
            t["frame"].destroy()
            self.tasks.remove(t)
        self._show_empty_if_needed()
        self._update_counter()

    def clear_done(self):
        for t in [t for t in self.tasks if t["done"]]:
            t["frame"].destroy()
            self.tasks.remove(t)
        self._show_empty_if_needed()
        self._update_counter()

    # ── render ───────────────────────────────

    def _render_task(self, task):
        if self.empty_lbl.winfo_ismapped():
            self.empty_lbl.pack_forget()

        frame = tk.Frame(self.task_frame, bg=BG_ITEM,
                         highlightbackground=BORDER, highlightthickness=1,
                         cursor="hand2")
        frame.pack(fill="x", padx=6, pady=3)

        chk_var = tk.BooleanVar(value=task["done"])
        chk = tk.Checkbutton(
            frame, variable=chk_var,
            bg=BG_ITEM, activebackground=BG_ITEM,
            selectcolor=BG_DONE, fg=TEXT_TEAL, activeforeground=TEXT_TEAL,
            relief="flat", bd=0,
            command=lambda t=task, v=chk_var: self._toggle(t, v),
        )
        chk.pack(side="left", padx=(10, 4), pady=8)

        lbl = tk.Label(frame, text=task["text"],
                       font=FONT_ITEM, bg=BG_ITEM, fg=TEXT_PRI,
                       anchor="w", wraplength=380, justify="left",
                       cursor="hand2")
        lbl.pack(side="left", fill="x", expand=True, pady=8)

        badge = tk.Label(frame, text="PENDIENTE",
                         font=FONT_BADGE, bg=ACCENT, fg=TEXT_PRI,
                         padx=6, pady=1)
        badge.pack(side="right", padx=10)

        task.update(frame=frame, label=lbl, badge=badge,
                    chk=chk, chk_var=chk_var, selected=False)

        if task["done"]:
            self._refresh_item(task)

        for w in (frame, lbl, badge):
            w.bind("<Button-1>",        lambda e, t=task: self._select(t))
            w.bind("<Double-Button-1>", lambda e, t=task: self._double_click(t))
            w.bind("<Enter>",           lambda e, t=task:
                       t["frame"].configure(bg=BG_ITEM_HOV) if not t["selected"] else None)
            w.bind("<Leave>",           lambda e, t=task:
                       t["frame"].configure(
                           bg="#2A2A3F" if t["selected"]
                           else (BG_DONE if t["done"] else BG_ITEM)))

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def _refresh_item(self, task):
        if task["done"]:
            task["frame"].configure(bg=BG_DONE,  highlightbackground=TEXT_DONE)
            task["label"].configure(bg=BG_DONE,  fg=TEXT_DONE,
                                    font=(FONT_ITEM[0], FONT_ITEM[1], "overstrike"))
            task["badge"].configure(text="✔ HECHO", bg=TEXT_DONE, fg="#C8F5C8")
            task["chk"].configure(bg=BG_DONE, activebackground=BG_DONE)
            task["chk_var"].set(True)
        else:
            task["frame"].configure(bg=BG_ITEM,  highlightbackground=BORDER)
            task["label"].configure(bg=BG_ITEM,  fg=TEXT_PRI, font=FONT_ITEM)
            task["badge"].configure(text="PENDIENTE", bg=ACCENT, fg=TEXT_PRI)
            task["chk"].configure(bg=BG_ITEM, activebackground=BG_ITEM)
            task["chk_var"].set(False)

    def _select(self, task):
        task["selected"] = not task["selected"]
        bg = "#2A2A3F" if task["selected"] else (BG_DONE if task["done"] else BG_ITEM)
        task["frame"].configure(bg=bg)
        task["label"].configure(bg=bg)
        task["chk"].configure(bg=bg, activebackground=bg)

    def _double_click(self, task):
        task["done"] = not task["done"]
        self._refresh_item(task)
        self._update_counter()

    def _toggle(self, task, var):
        task["done"] = var.get()
        self._refresh_item(task)
        self._update_counter()

    def _get_selected(self):
        return [t for t in self.tasks if t["selected"]]

    def _show_empty_if_needed(self):
        if not self.tasks:
            self.empty_lbl.pack(pady=40)

    def _update_counter(self):
        total   = len(self.tasks)
        pending = sum(1 for t in self.tasks if not t["done"])
        s = "s" if pending != 1 else ""
        self.counter_lbl.configure(
            text=f"  {pending} pendiente{s} / {total} total  ")

    def _shake_entry(self, steps=6, dist=5):
        def _step(i):
            if i >= steps:
                self.entry.pack_configure(padx=(0, 0))
                return
            self.entry.pack_configure(padx=(dist if i % 2 == 0 else 0, 0))
            self.entry.after(40, lambda: _step(i + 1))
        _step(0)

    def _entry_focus_in(self, _):
        self.entry.configure(highlightthickness=2,
                             highlightbackground=ACCENT,
                             highlightcolor=ACCENT)

    def _entry_focus_out(self, _):
        self.entry.configure(highlightthickness=0)

    def _on_frame_cfg(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_cfg(self, event):
        self.canvas.itemconfig(self._cw, width=event.width)

    def _on_scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == "__main__":
    root = tk.Tk()
    app  = GestorTareas(root)
    root.mainloop()