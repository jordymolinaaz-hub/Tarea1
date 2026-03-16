import tkinter as tk
from tkinter import ttk, messagebox


def agregar():
    nombre = entry_nombre.get().strip()
    edad = entry_edad.get().strip()
    correo = entry_correo.get().strip()

    if not nombre or not edad or not correo:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    if not edad.isdigit():
        messagebox.showerror("Error", "La edad debe ser un número entero.")
        return

    tabla.insert("", "end", values=(nombre, edad, correo))
    limpiar_campos()


def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_nombre.focus()


def limpiar_seleccion():
    seleccionados = tabla.selection()
    if not seleccionados:
        messagebox.showinfo("Sin selección", "Selecciona al menos un registro para eliminar.")
        return
    for item in seleccionados:
        tabla.delete(item)


def limpiar_todo():
    for item in tabla.get_children():
        tabla.delete(item)
    limpiar_campos()


# ── Ventana principal ──────────────────────────────────────────────────────────
root = tk.Tk()
root.title("📋 Gestión de Usuarios — GUI con Tkinter")
root.geometry("720x560")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# ── Estilos ttk ───────────────────────────────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel",       background="#1e1e2e", foreground="#cdd6f4", font=("Courier New", 11))
style.configure("Title.TLabel", background="#1e1e2e", foreground="#89b4fa", font=("Courier New", 18, "bold"))
style.configure("Sub.TLabel",   background="#313244", foreground="#a6e3a1", font=("Courier New", 10, "bold"))

style.configure("TEntry",       fieldbackground="#313244", foreground="#cdd6f4",
                insertcolor="#cdd6f4", font=("Courier New", 11), relief="flat")

style.configure("Add.TButton",   background="#a6e3a1", foreground="#1e1e2e",
                font=("Courier New", 11, "bold"), padding=6, relief="flat")
style.map("Add.TButton",   background=[("active", "#94d3ac")])

style.configure("Del.TButton",   background="#f38ba8", foreground="#1e1e2e",
                font=("Courier New", 11, "bold"), padding=6, relief="flat")
style.map("Del.TButton",   background=[("active", "#e07a96")])

style.configure("Clear.TButton", background="#fab387", foreground="#1e1e2e",
                font=("Courier New", 11, "bold"), padding=6, relief="flat")
style.map("Clear.TButton", background=[("active", "#e8a070")])

style.configure("Treeview",
                background="#313244", foreground="#cdd6f4",
                fieldbackground="#313244", rowheight=28,
                font=("Courier New", 10))
style.configure("Treeview.Heading",
                background="#45475a", foreground="#89b4fa",
                font=("Courier New", 10, "bold"), relief="flat")
style.map("Treeview", background=[("selected", "#585b70")])

# ── Título ─────────────────────────────────────────────────────────────────────
frm_titulo = tk.Frame(root, bg="#1e1e2e")
frm_titulo.pack(pady=(20, 8))
ttk.Label(frm_titulo, text="Sistema de Registro de Usuarios", style="Title.TLabel").pack()
ttk.Label(frm_titulo, text="Agrega, visualiza y elimina registros fácilmente",
          style="TLabel").pack()

# ── Formulario ─────────────────────────────────────────────────────────────────
frm_form = tk.Frame(root, bg="#313244", padx=20, pady=16, relief="flat")
frm_form.pack(padx=30, pady=8, fill="x")

ttk.Label(frm_form, text="FORMULARIO DE ENTRADA", style="Sub.TLabel").grid(
    row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

# Fila de campos
labels = ["Nombre:", "Edad:", "Correo:"]
for i, texto in enumerate(labels):
    ttk.Label(frm_form, text=texto, style="TLabel").grid(row=1, column=i*2, sticky="e", padx=(0, 6))

entry_nombre = ttk.Entry(frm_form, width=20)
entry_nombre.grid(row=1, column=1, padx=(0, 16), ipady=4)

entry_edad = ttk.Entry(frm_form, width=8)
entry_edad.grid(row=1, column=3, padx=(0, 16), ipady=4)

entry_correo = ttk.Entry(frm_form, width=24)
entry_correo.grid(row=1, column=5, ipady=4)

# Fila de botones
frm_btns = tk.Frame(frm_form, bg="#313244")
frm_btns.grid(row=2, column=0, columnspan=6, pady=(14, 0), sticky="e")

ttk.Button(frm_btns, text="➕  Agregar",          style="Add.TButton",   command=agregar).pack(side="left", padx=4)
ttk.Button(frm_btns, text="🗑  Eliminar selección", style="Del.TButton",   command=limpiar_seleccion).pack(side="left", padx=4)
ttk.Button(frm_btns, text="🧹  Limpiar todo",       style="Clear.TButton", command=limpiar_todo).pack(side="left", padx=4)

# ── Tabla ──────────────────────────────────────────────────────────────────────
frm_tabla = tk.Frame(root, bg="#1e1e2e")
frm_tabla.pack(padx=30, pady=(8, 20), fill="both", expand=True)

columnas = ("Nombre", "Edad", "Correo")
tabla = ttk.Treeview(frm_tabla, columns=columnas, show="headings", selectmode="extended")

for col in columnas:
    tabla.heading(col, text=col)
tabla.column("Nombre", width=220, anchor="w")
tabla.column("Edad",   width=70,  anchor="center")
tabla.column("Correo", width=280, anchor="w")

scrollbar = ttk.Scrollbar(frm_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ── Barra de estado ────────────────────────────────────────────────────────────
tk.Label(root, text="Listo  •  Tkinter GUI  •  Python 3",
         bg="#181825", fg="#585b70", font=("Courier New", 9),
         anchor="w", padx=10).pack(side="bottom", fill="x")

entry_nombre.focus()
root.mainloop()