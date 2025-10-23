import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd

# ===================== CONFIG VENTANA =====================
ventana = tk.Tk()
ventana.title("Sistema de Matriculación y Control de Notas - UNAN")
ventana.geometry("1350x820")
COLOR_FONDO = "#FFFFFF"
ventana.config(bg=COLOR_FONDO)

# ===================== BANDERA / LOGO =====================
try:
    img = Image.open("bandera_unan.png")
    img = img.resize((250, 140))
    img_tk = ImageTk.PhotoImage(img)
    label_bandera = tk.Label(ventana, image=img_tk, bg=COLOR_FONDO)
    label_bandera.image = img_tk
    label_bandera.pack(pady=6)
except Exception:
    tk.Label(ventana, text="[ Bandera no encontrada ]", bg=COLOR_FONDO, fg="red", font=("Arial", 12, "bold")).pack(pady=6)

# ===================== DATOS =====================
estudiantes = []

# ===================== FUNCIONES =====================
def calcular_promedio(notas_list):
    try:
        notas = [float(n) for n in notas_list if str(n).strip() != ""]
        return round(sum(notas) / len(notas), 2) if notas else 0
    except Exception:
        return 0

def obtener_estado(promedio):
    try:
        prom = float(promedio)
        if prom == 0:
            return "Sin notas"
        return "Aprobado ✅" if prom >= 60 else "Reprobado ❌"
    except Exception:
        return "Inválido"

def recolectar_campos():
    datos = {
        "Cedula": entry_cedula.get().strip(),
        "Nombre": entry_nombre.get().strip(),
        "Apellido": entry_apellido.get().strip(),
        "Sexo": combo_sexo.get().strip(),
        "Fecha Nac": entry_fecha.get().strip(),
        "Estado Civil": combo_estado_civil.get().strip(),
        "Nacionalidad": entry_nacionalidad.get().strip(),
        "Departamento": entry_departamento.get().strip(),
        "Direccion": entry_direccion.get().strip(),
        "Telefono": entry_telefono.get().strip(),
        "Correo": entry_correo.get().strip(),
        "Carrera": entry_carrera.get().strip(),
        "Año": entry_anio.get().strip(),
        "Nombre Padre": entry_padre.get().strip(),
        "Nombre Madre": entry_madre.get().strip(),
        "Ingresos Padres": entry_ingresos.get().strip(),
        "Parcial 1": entry_parcial1.get().strip(),
        "Parcial 2": entry_parcial2.get().strip(),
        "Parcial 3": entry_parcial3.get().strip(),
        "Parcial 4": entry_parcial4.get().strip(),
    }
    notas = [datos["Parcial 1"], datos["Parcial 2"], datos["Parcial 3"], datos["Parcial 4"]]
    datos["Promedio"] = calcular_promedio(notas)
    datos["Estado"] = obtener_estado(datos["Promedio"])
    return datos

def actualizar_tabla():
    """Actualiza la vista de la tabla con la lista 'estudiantes' (diccionarios)."""
    # Limpia la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)
    # Inserta filas (manteniendo el orden de columnas 'cols')
    for est in estudiantes:
        fila = [
            est.get('Cedula',''), est.get('Nombre',''), est.get('Apellido',''), est.get('Sexo',''),
            est.get('Fecha Nac',''), est.get('Estado Civil',''), est.get('Nacionalidad',''), est.get('Departamento',''),
            est.get('Direccion',''), est.get('Telefono',''), est.get('Correo',''), est.get('Carrera',''),
            est.get('Año',''), est.get('Nombre Padre',''), est.get('Nombre Madre',''), est.get('Ingresos Padres',''),
            est.get('Parcial 1',''), est.get('Parcial 2',''), est.get('Parcial 3',''), est.get('Parcial 4',''),
            est.get('Promedio',''), est.get('Estado','')
        ]
        tabla.insert("", "end", values=fila)

def agregar_estudiante():
    datos = recolectar_campos()
    if not datos["Cedula"] or not datos["Nombre"]:
        messagebox.showwarning("Advertencia", "Cédula y Nombre son obligatorios.")
        return
    estudiantes.append(datos)
    actualizar_tabla()
    limpiar_campos()

def actualizar_estudiante():
    sel = tabla.focus()
    if not sel:
        messagebox.showwarning("Advertencia", "Selecciona un registro para actualizar.")
        return
    idx = tabla.index(sel)
    datos = recolectar_campos()
    estudiantes[idx] = datos
    actualizar_tabla()
    limpiar_campos()

def eliminar_estudiante():
    sel = tabla.selection()
    if not sel:
        messagebox.showwarning("Advertencia", "Selecciona un registro para eliminar.")
        return
    if not messagebox.askyesno("Confirmar", "¿Deseas eliminar el registro seleccionado?"):
        return
    idx = tabla.index(sel[0])
    estudiantes.pop(idx)
    actualizar_tabla()
    limpiar_campos()

def limpiar_campos():
    for e in [entry_cedula, entry_nombre, entry_apellido, entry_fecha, entry_nacionalidad, entry_departamento,
              entry_direccion, entry_telefono, entry_correo, entry_carrera, entry_anio, entry_padre, entry_madre, entry_ingresos,
              entry_parcial1, entry_parcial2, entry_parcial3, entry_parcial4]:
        e.delete(0, tk.END)
    combo_sexo.set('')
    combo_estado_civil.set('')

def on_seleccion(event):
    sel = tabla.focus()
    if not sel:
        return
    vals = tabla.item(sel, 'values')
    # asignar en el mismo orden de columnas definidas
    keys = [
        "Cedula","Nombre","Apellido","Sexo","Fecha Nac","Estado Civil","Nacionalidad","Departamento",
        "Direccion","Telefono","Correo","Carrera","Año","Nombre Padre","Nombre Madre","Ingresos Padres",
        "Parcial 1","Parcial 2","Parcial 3","Parcial 4","Promedio","Estado"
    ]
    for k, v in zip(keys, vals):
        # map field to widget
        if k == "Cedula":
            entry_cedula.delete(0, tk.END); entry_cedula.insert(0, v)
        elif k == "Nombre":
            entry_nombre.delete(0, tk.END); entry_nombre.insert(0, v)
        elif k == "Apellido":
            entry_apellido.delete(0, tk.END); entry_apellido.insert(0, v)
        elif k == "Sexo":
            combo_sexo.set(v)
        elif k == "Fecha Nac":
            entry_fecha.delete(0, tk.END); entry_fecha.insert(0, v)
        elif k == "Estado Civil":
            combo_estado_civil.set(v)
        elif k == "Nacionalidad":
            entry_nacionalidad.delete(0, tk.END); entry_nacionalidad.insert(0, v)
        elif k == "Departamento":
            entry_departamento.delete(0, tk.END); entry_departamento.insert(0, v)
        elif k == "Direccion":
            entry_direccion.delete(0, tk.END); entry_direccion.insert(0, v)
        elif k == "Telefono":
            entry_telefono.delete(0, tk.END); entry_telefono.insert(0, v)
        elif k == "Correo":
            entry_correo.delete(0, tk.END); entry_correo.insert(0, v)
        elif k == "Carrera":
            entry_carrera.delete(0, tk.END); entry_carrera.insert(0, v)
        elif k == "Año":
            entry_anio.delete(0, tk.END); entry_anio.insert(0, v)
        elif k == "Nombre Padre":
            entry_padre.delete(0, tk.END); entry_padre.insert(0, v)
        elif k == "Nombre Madre":
            entry_madre.delete(0, tk.END); entry_madre.insert(0, v)
        elif k == "Ingresos Padres":
            entry_ingresos.delete(0, tk.END); entry_ingresos.insert(0, v)
        elif k == "Parcial 1":
            entry_parcial1.delete(0, tk.END); entry_parcial1.insert(0, v)
        elif k == "Parcial 2":
            entry_parcial2.delete(0, tk.END); entry_parcial2.insert(0, v)
        elif k == "Parcial 3":
            entry_parcial3.delete(0, tk.END); entry_parcial3.insert(0, v)
        elif k == "Parcial 4":
            entry_parcial4.delete(0, tk.END); entry_parcial4.insert(0, v)

def exportar_excel():
    if not estudiantes:
        messagebox.showwarning("Advertencia", "No hay datos para exportar.")
        return
    df = pd.DataFrame(estudiantes)
    archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files","*.xlsx")])
    if not archivo:
        return
    try:
        with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Matricula')
            hoja = writer.sheets['Matricula']
            # ajustar anchos de columna
            for i, col in enumerate(df.columns, 1):
                max_len = df[col].astype(str).map(len).max()
                hoja.column_dimensions[hoja.cell(row=1, column=i).column_letter].width = max(max_len + 2, len(col) + 2)
        messagebox.showinfo('Éxito', f'Datos exportados a: {archivo}')
    except Exception as e:
        messagebox.showerror('Error', f'No se pudo exportar: {e}')

# ===================== INTERFAZ - FORMULARIO =====================
frame_form = tk.LabelFrame(ventana, text='Datos de Matrícula', bg=COLOR_FONDO, fg='black', font=('Arial', 11, 'bold'))
frame_form.pack(padx=12, pady=8, fill='x')

estilo = {'width': 22, 'font': ('Arial', 10)}

# fila 1
tk.Label(frame_form, text='Cédula:', bg=COLOR_FONDO).grid(row=0, column=0, padx=6, pady=4, sticky='e')
entry_cedula = tk.Entry(frame_form, **estilo)
entry_cedula.grid(row=0, column=1, padx=6, pady=4)
tk.Label(frame_form, text='Nombre:', bg=COLOR_FONDO).grid(row=0, column=2, padx=6, pady=4, sticky='e')
entry_nombre = tk.Entry(frame_form, **estilo)
entry_nombre.grid(row=0, column=3, padx=6, pady=4)
tk.Label(frame_form, text='Apellido:', bg=COLOR_FONDO).grid(row=0, column=4, padx=6, pady=4, sticky='e')
entry_apellido = tk.Entry(frame_form, **estilo)
entry_apellido.grid(row=0, column=5, padx=6, pady=4)

# fila 2
tk.Label(frame_form, text='Sexo:', bg=COLOR_FONDO).grid(row=1, column=0, padx=6, pady=4, sticky='e')
combo_sexo = ttk.Combobox(frame_form, values=['Masculino','Femenino','Otro'], width=20)
combo_sexo.grid(row=1, column=1, padx=6, pady=4)
tk.Label(frame_form, text='Fecha Nac.:', bg=COLOR_FONDO).grid(row=1, column=2, padx=6, pady=4, sticky='e')
entry_fecha = tk.Entry(frame_form, **estilo)
entry_fecha.grid(row=1, column=3, padx=6, pady=4)
tk.Label(frame_form, text='Estado Civil:', bg=COLOR_FONDO).grid(row=1, column=4, padx=6, pady=4, sticky='e')
combo_estado_civil = ttk.Combobox(frame_form, values=['Soltero/a','Casado/a','Divorciado/a','Viudo/a'], width=20)
combo_estado_civil.grid(row=1, column=5, padx=6, pady=4)

# fila 3
tk.Label(frame_form, text='Nacionalidad:', bg=COLOR_FONDO).grid(row=2, column=0, padx=6, pady=4, sticky='e')
entry_nacionalidad = tk.Entry(frame_form, **estilo)
entry_nacionalidad.grid(row=2, column=1, padx=6, pady=4)
tk.Label(frame_form, text='Departamento:', bg=COLOR_FONDO).grid(row=2, column=2, padx=6, pady=4, sticky='e')
entry_departamento = tk.Entry(frame_form, **estilo)
entry_departamento.grid(row=2, column=3, padx=6, pady=4)
tk.Label(frame_form, text='Dirección:', bg=COLOR_FONDO).grid(row=2, column=4, padx=6, pady=4, sticky='e')
entry_direccion = tk.Entry(frame_form, **estilo)
entry_direccion.grid(row=2, column=5, padx=6, pady=4)

# fila 4
tk.Label(frame_form, text='Teléfono:', bg=COLOR_FONDO).grid(row=3, column=0, padx=6, pady=4, sticky='e')
entry_telefono = tk.Entry(frame_form, **estilo)
entry_telefono.grid(row=3, column=1, padx=6, pady=4)
tk.Label(frame_form, text='Correo:', bg=COLOR_FONDO).grid(row=3, column=2, padx=6, pady=4, sticky='e')
entry_correo = tk.Entry(frame_form, **estilo)
entry_correo.grid(row=3, column=3, padx=6, pady=4)
tk.Label(frame_form, text='Carrera:', bg=COLOR_FONDO).grid(row=3, column=4, padx=6, pady=4, sticky='e')
entry_carrera = tk.Entry(frame_form, **estilo)
entry_carrera.grid(row=3, column=5, padx=6, pady=4)

# fila 5
tk.Label(frame_form, text='Año Académico:', bg=COLOR_FONDO).grid(row=4, column=0, padx=6, pady=4, sticky='e')
entry_anio = tk.Entry(frame_form, **estilo)
entry_anio.grid(row=4, column=1, padx=6, pady=4)
tk.Label(frame_form, text='Nombre Padre:', bg=COLOR_FONDO).grid(row=4, column=2, padx=6, pady=4, sticky='e')
entry_padre = tk.Entry(frame_form, **estilo)
entry_padre.grid(row=4, column=3, padx=6, pady=4)
tk.Label(frame_form, text='Nombre Madre:', bg=COLOR_FONDO).grid(row=4, column=4, padx=6, pady=4, sticky='e')
entry_madre = tk.Entry(frame_form, **estilo)
entry_madre.grid(row=4, column=5, padx=6, pady=4)

# fila 6
tk.Label(frame_form, text='Ingresos Padres:', bg=COLOR_FONDO).grid(row=5, column=0, padx=6, pady=4, sticky='e')
entry_ingresos = tk.Entry(frame_form, **estilo)
entry_ingresos.grid(row=5, column=1, padx=6, pady=4)

# separador
sep = ttk.Separator(ventana, orient='horizontal')
sep.pack(fill='x', padx=12, pady=8)

# ===================== NOTAS - PARCIALES EN ORDEN =====================
frame_notas = tk.LabelFrame(ventana, text='Notas Parciales', bg=COLOR_FONDO, fg='black', font=('Arial', 11, 'bold'))
frame_notas.pack(padx=12, pady=6, fill='x')

tk.Label(frame_notas, text='Parcial 1:', bg=COLOR_FONDO).grid(row=0, column=0, padx=6, pady=6, sticky='e')
entry_parcial1 = tk.Entry(frame_notas, width=15)
entry_parcial1.grid(row=0, column=1, padx=6, pady=6)

tk.Label(frame_notas, text='Parcial 2:', bg=COLOR_FONDO).grid(row=0, column=2, padx=6, pady=6, sticky='e')
entry_parcial2 = tk.Entry(frame_notas, width=15)
entry_parcial2.grid(row=0, column=3, padx=6, pady=6)

tk.Label(frame_notas, text='Parcial 3:', bg=COLOR_FONDO).grid(row=0, column=4, padx=6, pady=6, sticky='e')
entry_parcial3 = tk.Entry(frame_notas, width=15)
entry_parcial3.grid(row=0, column=5, padx=6, pady=6)

tk.Label(frame_notas, text='Parcial 4:', bg=COLOR_FONDO).grid(row=0, column=6, padx=6, pady=6, sticky='e')
entry_parcial4 = tk.Entry(frame_notas, width=15)
entry_parcial4.grid(row=0, column=7, padx=6, pady=6)

# ===================== BOTONES =====================
frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
frame_botones.pack(pady=10)

btn_style = {'font':('Arial', 10, 'bold'), 'width':14}

tk.Button(frame_botones, text='Agregar', command=agregar_estudiante, bg='#4DB6AC', fg='white', **btn_style).grid(row=0, column=0, padx=8)
tk.Button(frame_botones, text='Actualizar', command=actualizar_estudiante, bg='#64B5F6', fg='white', **btn_style).grid(row=0, column=1, padx=8)
tk.Button(frame_botones, text='Eliminar', command=eliminar_estudiante, bg='#E57373', fg='white', **btn_style).grid(row=0, column=2, padx=8)
tk.Button(frame_botones, text='Limpiar', command=limpiar_campos, bg='#9E9E9E', fg='white', **btn_style).grid(row=0, column=3, padx=8)
tk.Button(frame_botones, text='Exportar Excel', command=exportar_excel, bg='#81C784', fg='white', **btn_style).grid(row=0, column=4, padx=8)

# ===================== TABLA =====================
cols = [
    'Cedula','Nombre','Apellido','Sexo','Fecha Nac','Estado Civil','Nacionalidad','Departamento',
    'Direccion','Telefono','Correo','Carrera','Año','Nombre Padre','Nombre Madre','Ingresos Padres',
    'Parcial 1','Parcial 2','Parcial 3','Parcial 4','Promedio','Estado'
]

tabla = ttk.Treeview(ventana, columns=cols, show='headings', height=12)
for c in cols:
    tabla.heading(c, text=c)
    tabla.column(c, width=110, anchor='center')

tabla.pack(fill='both', expand=True, padx=12, pady=12)
tabla.bind('<<TreeviewSelect>>', on_seleccion)

# estilo simple
style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
style.configure('Treeview', font=('Arial', 10), rowheight=24)

ventana.mainloop()
