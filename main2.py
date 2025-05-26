 # Importar bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from exercises import empleados_exercise, tecnologias_exercise, proyectos_exercise, EmpleadosYHabilidades_exercise, EmpleadosYProyectos_exercise
from exercises import Certificaciones_exercise, Salario_exercise, TecnologiasyHabilidades_exercise, Proyempleados_exercise  
import pyodbc
from decimal import Decimal
from datetime import datetime


# Conexión a la base de datos
try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=148.239.60.61;"
        "DATABASE=ProyectoBD_MCJ;"
        "UID=ids;"
        "PWD=uag85;"
    )
    c = conn.cursor()
except pyodbc.Error as e:
    print("Error al conectar a la base de datos:", e)
    exit()

# Variables globales
last_result = []
current_frame = None

def normalize_results(results):
    """
    Normaliza los resultados para facilitar la comparación.
    """
    normalized = []
    for row in results:
        normalized_row = []
        for value in row:
            if isinstance(value, str):  # Cadenas de texto
                normalized_row.append(value.strip().lower())  # Convertir a minúsculas y quitar espacios
            elif isinstance(value, Decimal):  # Decimales
                normalized_row.append(round(float(value), 2))  # Redondear a 2 decimales
            elif isinstance(value, (int, float)):  # Números
                normalized_row.append(value)  # No cambiamos los valores numéricos
            elif isinstance(value, datetime):  # Fechas
                normalized_row.append(value.strftime('%d-%m-%Y'))  # Convertir la fecha al formato 'DD-MM-YYYY'
            else:
                normalized_row.append(value)  # Otros valores se mantienen igual
        normalized.append(tuple(normalized_row))
    return normalized

def verify_code(expected_result, resultado_correcto):
    """
    Compara los resultados obtenidos con los esperados.
    """
    global last_result

    # Verifica si no hay resultados de una consulta previa
    if last_result is None or len(last_result) == 0:
        resultado_correcto.config(
            text="No se ha ejecutado ninguna consulta válida aún.",
            bg="yellow"
        )
        return

    # Normalizar los resultados obtenidos y los esperados
    normalized_last_result = normalize_results(last_result)
    normalized_expected_result = normalize_results(expected_result)

    # Debug opcional para validar comparación
    print("Resultados obtenidos normalizados:", normalized_last_result)
    print("Resultados esperados normalizados:", normalized_expected_result)

    # Comparar resultados normalizados
    if normalized_last_result == normalized_expected_result:
        resultado_correcto.config(text="Código verificado: Correcto", bg="green")
    else:
        resultado_correcto.config(
            text=f"Código verificado: Incorrecto\n\nResultado esperado: {normalized_expected_result}\n\nResultado obtenido: {normalized_last_result}",
            bg="red"
        )


# Función para cambiar de pantalla
def switch_frame(new_frame_func):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame_func()
    current_frame.pack(fill="both", expand=True)

# Función para ejecutar consultas
def run_code(user_input, expected_result, resultado_correcto, resultado_codigo, table_frame):
    global last_result
    code = user_input.get("1.0", tk.END).strip()
    
    try:
        c.execute(code)
        if code.upper().startswith("SELECT"):
            columns = [column[0] for column in c.description]
            rows = c.fetchall()
            last_result = rows
            display_table(columns, rows, table_frame)
            resultado_codigo.config(text="Consulta ejecutada exitosamente.", bg="green")
        else:
            conn.commit()
            resultado_codigo.config(text="Consulta ejecutada exitosamente.", bg="green")
            last_result = None  # Limpiamos el resultado si no es un SELECT
    except pyodbc.Error as e:
        resultado_codigo.config(text=f"Error en la consulta: {e}", bg="red")
        last_result = None  # Limpiamos el resultado en caso de error


# Función para normalizar fechas
def normalize_date(date):
    if isinstance(date, datetime):
        return date.date()  # Solo la fecha, sin la hora
    return date

# Función para verificar consultas
def verify_code(expected_result, resultado_correcto):
    global last_result
    code = last_result  # Los resultados de la consulta ejecutada previamente
    
    # Verifica si no se ejecutó una consulta
    if code is None or len(code) == 0:
        resultado_correcto.config(
            text="No se ha ejecutado ninguna consulta válida aún.",
            bg="yellow"
        )
        return
    
    # Normalizar las fechas en los resultados obtenidos
    normalized_last_result = [tuple(normalize_date(value) if isinstance(value, datetime) else value for value in row) for row in last_result]
    normalized_expected_result = [tuple(normalize_date(value) if isinstance(value, datetime) else value for value in row) for row in expected_result]

    # Debug: Imprimir resultados para depuración
    print("Resultados obtenidos normalizados:", normalized_last_result)
    print("Resultados esperados normalizados:", normalized_expected_result)
    
    # Comparar los resultados obtenidos con los esperados
    if normalized_last_result == normalized_expected_result:
        resultado_correcto.config(text="Código verificado: Correcto", bg="green")
    else:
        resultado_correcto.config(
            text=f"Código verificado: Incorrecto\n\nResultado esperado: {normalized_expected_result}\n\nResultado obtenido: {normalized_last_result}",
            bg="red"
        )




# Mostrar resultados en tabla
def display_table(columns, rows, table_frame):
    for widget in table_frame.winfo_children():
        widget.destroy()
    table = ttk.Treeview(table_frame, columns=columns, show="headings")
    table.pack(fill=tk.BOTH, expand=True)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor=tk.CENTER)
    for row in rows:
        table.insert("", tk.END, values=row)

def open_exercise_interface(exercise_func):
    """
    Función para abrir la interfaz de un ejercicio.
    """
    description, expected_result = exercise_func()

    # Identificar y redirigir según el ejercicio
    if description.lower().startswith("listar los nombres y apellidos"):
        switch_frame(lambda: create_empleados_interface(description, expected_result))
    elif description.lower().startswith("Mostrar las tecnologías"):
        switch_frame(lambda: create_tecnologias_interface(description, expected_result))
    elif description.lower().startswith("Listar los nombres de los proyectos"):
        switch_frame(lambda: create_proyectos_interface(description, expected_result))
    elif description.lower().startswith("Listar los empleados con sus habilidades"):
        switch_frame(lambda: create_empleados_y_habilidades_interface(description, expected_result))
    else:
        switch_frame(lambda: create_main_interface(description, expected_result))
# Actualización del diseño con esquema de colores morado/blanco
PRIMARY_COLOR = "#6c63ff"  # Morado principal
SECONDARY_COLOR = "#f4f4fc"  # Fondo claro
ACCENT_COLOR = "#3e3a63"  # Fondo oscuro
TEXT_COLOR = "#ffffff"  # Texto blanco
HIGHLIGHT_COLOR = "#a99deb"  # Morado claro

def create_empleados_interface(description, expected_result):
    """
    Interfaz específica para el ejercicio de Empleados.
    Incluye una tabla como parte del "Output esperado".
    """
    frame = tk.Frame(root, bg=SECONDARY_COLOR)

    # Botón de volver
    tk.Button(frame, text="Volver", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: switch_frame(create_exercise_menu)).pack(anchor="ne", padx=10, pady=10)

    left_panel = tk.Frame(frame, bg=ACCENT_COLOR, pady=10, padx=10)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(left_panel, text=description, bg=SECONDARY_COLOR, fg=ACCENT_COLOR, wraplength=500).pack(padx=10, pady=10)

    # Imagen del diagrama
    imagenDiagram = Image.open(r"C:\Users\chris\OneDrive\Pictures\Screenshots\DIAGRAMAAA.png")
    imagenDiagram = imagenDiagram.resize((700, 500))
    imagen_tk = ImageTk.PhotoImage(imagenDiagram)
    tk.Label(left_panel, image=imagen_tk, bg=ACCENT_COLOR).pack()
    left_panel.image = imagen_tk

    # Agregar texto "Output esperado:"
    tk.Label(left_panel, text="Output esperado:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 12, "bold")).pack(pady=10)

    # Crear la tabla específica para el ejercicio "Empleados"
    table_frame = tk.Frame(left_panel, bg=ACCENT_COLOR)
    table_frame.pack(pady=10, anchor="w")  # Alineación a la izquierda

    # Crear el Treeview (la tabla)
    columns = ("ID", "Nombre", "Apellido")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Configurar encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    # Insertar los datos en la tabla
    data = [
        (1, "Sofía", "Castro"),
        (2, "Ana", "García"),
        (3, "José", "González"),
        (4, "Carlos", "Hernández"),
        (5, "Pedro", "Jiménez"),
        (6, "María", "López"),
        (7, "Luis", "Martínez"),
        (8, "Juan", "Pérez"),
        (9, "Laura", "Ramírez"),
        (10, "Sandra", "Torres"),
    ]
    for row in data:
        tree.insert("", tk.END, values=row)

    # Empaquetar la tabla
    tree.pack()

    right_panel = tk.Frame(frame, padx=10, pady=10, bg=SECONDARY_COLOR)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(right_panel, text="Escribe aquí tu código SQL:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR).pack(anchor="w", padx=10, pady=5)
    user_input = tk.Text(right_panel, width=80, height=20, bg="white")
    user_input.pack(anchor="w", pady=10)

    resultado_correcto = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_correcto.pack(pady=5)
    resultado_codigo = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_codigo.pack(pady=5)

    table_frame = tk.Frame(right_panel, bg=SECONDARY_COLOR)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(right_panel, text="Ejecutar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: run_code(user_input, expected_result, resultado_correcto, resultado_codigo, table_frame)).pack(anchor="w", pady=5)
    tk.Button(right_panel, text="Verificar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: verify_code(expected_result, resultado_correcto)).pack(anchor="w", pady=5)

    return frame

def create_tecnologias_interface(description, expected_result):
    """
    Función para crear la interfaz del ejercicio "Tecnologías disponibles".
    """
    frame = tk.Frame(root, bg=SECONDARY_COLOR)
    # Botón de volver
    tk.Button(frame, text="Volver", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: switch_frame(create_exercise_menu)).pack(anchor="ne", padx=10, pady=10)

    left_panel = tk.Frame(frame, bg=ACCENT_COLOR, pady=10, padx=10)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(left_panel, text=description, bg=SECONDARY_COLOR, fg=ACCENT_COLOR, wraplength=500).pack(padx=10, pady=10)

    # Imagen del diagrama
    imagenDiagram = Image.open(r"C:\Users\chris\OneDrive\Pictures\Screenshots\DIAGRAMAAA.png")
    imagenDiagram = imagenDiagram.resize((700, 500))
    imagen_tk = ImageTk.PhotoImage(imagenDiagram)
    tk.Label(left_panel, image=imagen_tk, bg=ACCENT_COLOR).pack()
    left_panel.image = imagen_tk

    # Agregar texto "Output esperado:"
    tk.Label(left_panel, text="Output esperado:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 12, "bold")).pack(pady=10)

    # Añadir la tabla para "Tecnologías disponibles"
    table_frame = tk.Frame(left_panel, bg=ACCENT_COLOR)
    table_frame.pack(pady=10)
    columns = ("NombreTecnologia", "Descripcion")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Configurar encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")

    # Insertar los datos de la tabla (de la imagen proporcionada)
    data = [
        ("AWS", "Plataforma de servicios en la nube"),
        ("Azure", "Plataforma de servicios en la nube de Microsoft"),
        ("Docker", "Herramienta de contenedores"),
        ("Java", "Lenguaje de programación orientado a objetos"),
        ("JavaScript", "Lenguaje de programación para desarrollo web"),
        ("Kubernetes", "Plataforma de orquestación de contenedores"),
        ("Linux", "Sistema operativo de código abierto"),
        ("Node.js", "Entorno de ejecución para JavaScript en el servidor"),
        ("Python", "Lenguaje de programación versátil"),
        ("SQL", "Lenguaje para gestión de bases de datos"),
    ]

    for row in data:
        tree.insert("", tk.END, values=row)

    # Empaquetar la tabla
    tree.pack()

    right_panel = tk.Frame(frame, padx=10, pady=10, bg=SECONDARY_COLOR)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(right_panel, text="Escribe aquí tu código SQL:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR).pack(anchor="w", padx=10, pady=5)
    user_input = tk.Text(right_panel, width=80, height=20, bg="white")
    user_input.pack(anchor="w", pady=10)

    resultado_correcto = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_correcto.pack(pady=5)
    resultado_codigo = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_codigo.pack(pady=5)

    table_frame = tk.Frame(right_panel, bg=SECONDARY_COLOR)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(right_panel, text="Ejecutar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: run_code(user_input, expected_result, resultado_correcto, resultado_codigo, table_frame)).pack(anchor="w", pady=5)
    tk.Button(right_panel, text="Verificar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: verify_code(expected_result, resultado_correcto)).pack(anchor="w", pady=5)

    return frame

def create_empleados_y_habilidades_interface(description, expected_result):
    """
    Función para crear la interfaz del ejercicio "Empleados y habilidades".
    Incluye una tabla como parte del "Output esperado".
    """
    frame = tk.Frame(root, bg=SECONDARY_COLOR)

    # Botón de volver
    tk.Button(frame, text="Volver", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: switch_frame(create_exercise_menu)).pack(anchor="ne", padx=10, pady=10)

    left_panel = tk.Frame(frame, bg=ACCENT_COLOR, pady=10, padx=10)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(left_panel, text=description, bg=SECONDARY_COLOR, fg=ACCENT_COLOR, wraplength=500).pack(padx=10, pady=10)

    # Imagen del diagrama
    imagenDiagram = Image.open(r"C:\Users\chris\OneDrive\Pictures\Screenshots\DIAGRAMAAA.png")
    imagenDiagram = imagenDiagram.resize((700, 500))
    imagen_tk = ImageTk.PhotoImage(imagenDiagram)
    tk.Label(left_panel, image=imagen_tk, bg=ACCENT_COLOR).pack()
    left_panel.image = imagen_tk

    # Agregar texto "Output esperado:"
    tk.Label(left_panel, text="Output esperado:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 12, "bold")).pack(pady=10)

    # Crear la tabla para "Empleados y habilidades"
    table_frame = tk.Frame(left_panel, bg=ACCENT_COLOR)
    table_frame.pack(pady=10, anchor="w")  # Alineación a la izquierda

    # Crear el Treeview (la tabla)
    columns = ("Nombre", "Apellido", "Tecnología", "Nivel")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Configurar encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")

    # Insertar los datos en la tabla
    data = [
        ("Sofía", "Castro", "Node.js", "Avanzado"),
        ("Pedro", "Jiménez", "Linux", "Avanzado"),
        ("María", "López", "SQL", "Avanzado"),
        ("Juan", "Pérez", "Java", "Avanzado"),
        ("Laura", "Ramírez", "Kubernetes", "Avanzado"),
        ("Ana", "García", "Python", "Intermedio"),
        ("Carlos", "Hernández", "Docker", "Intermedio"),
        ("Sandra", "Torres", "Azure", "Intermedio"),
        ("José", "González", "AWS", "Básico"),
        ("Luis", "Martínez", "JavaScript", "Básico"),
    ]

    for row in data:
        tree.insert("", tk.END, values=row)

    # Empaquetar la tabla
    tree.pack()

    right_panel = tk.Frame(frame, padx=10, pady=10, bg=SECONDARY_COLOR)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(right_panel, text="Escribe aquí tu código SQL:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR).pack(anchor="w", padx=10, pady=5)
    user_input = tk.Text(right_panel, width=80, height=20, bg="white")
    user_input.pack(anchor="w", pady=10)

    resultado_correcto = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_correcto.pack(pady=5)
    resultado_codigo = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_codigo.pack(pady=5)

    table_frame = tk.Frame(right_panel, bg=SECONDARY_COLOR)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(right_panel, text="Ejecutar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: run_code(user_input, expected_result, resultado_correcto, resultado_codigo, table_frame)).pack(anchor="w", pady=5)
    tk.Button(right_panel, text="Verificar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: verify_code(expected_result, resultado_correcto)).pack(anchor="w", pady=5)

    return frame



def create_proyectos_interface(description, expected_result):
    """
    Función para crear la interfaz del ejercicio "Proyectos y presupuesto".
    """
    frame = tk.Frame(root, bg=SECONDARY_COLOR)
    # Botón de volver
    tk.Button(frame, text="Volver", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: switch_frame(create_exercise_menu)).pack(anchor="ne", padx=10, pady=10)

    left_panel = tk.Frame(frame, bg=ACCENT_COLOR, pady=10, padx=10)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(left_panel, text=description, bg=SECONDARY_COLOR, fg=ACCENT_COLOR, wraplength=500).pack(padx=10, pady=10)

    # Imagen del diagrama
    imagenDiagram = Image.open(r"C:\Users\chris\OneDrive\Pictures\Screenshots\DIAGRAMAAA.png")
    imagenDiagram = imagenDiagram.resize((700, 500))
    imagen_tk = ImageTk.PhotoImage(imagenDiagram)
    tk.Label(left_panel, image=imagen_tk, bg=ACCENT_COLOR).pack()
    left_panel.image = imagen_tk

    # Agregar texto "Output esperado:"
    tk.Label(left_panel, text="Output esperado:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 12, "bold")).pack(pady=10)

    # Añadir la tabla para "Proyectos y presupuesto"
    table_frame = tk.Frame(left_panel, bg=ACCENT_COLOR)
    table_frame.pack(pady=10)
    columns = ("Nombre", "Presupuesto")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Configurar encabezados de la tabla
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")

    # Insertar los datos de la tabla (de la imagen proporcionada)
    data = [
        ("Data Warehouse", "300000.00"),
        ("E-commerce", "280000.00"),
        ("Migración a la Nube", "250000.00"),
        ("Seguridad", "220000.00"),
        ("Aplicación Móvil", "200000.00"),
        ("Automatización", "180000.00"),
        ("Sistema de Gestión", "150000.00"),
        ("Rediseño Web", "120000.00"),
        ("Chatbot", "100000.00"),
        ("Monitorización", "90000.00"),
    ]

    for row in data:
        tree.insert("", tk.END, values=row)

    # Empaquetar la tabla
    tree.pack()

    right_panel = tk.Frame(frame, padx=10, pady=10, bg=SECONDARY_COLOR)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(right_panel, text="Escribe aquí tu código SQL:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR).pack(anchor="w", padx=10, pady=5)
    user_input = tk.Text(right_panel, width=80, height=20, bg="white")
    user_input.pack(anchor="w", pady=10)

    resultado_correcto = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_correcto.pack(pady=5)
    resultado_codigo = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_codigo.pack(pady=5)

    table_frame = tk.Frame(right_panel, bg=SECONDARY_COLOR)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(right_panel, text="Ejecutar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: run_code(user_input, expected_result, resultado_correcto, resultado_codigo, table_frame)).pack(anchor="w", pady=5)
    tk.Button(right_panel, text="Verificar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: verify_code(expected_result, resultado_correcto)).pack(anchor="w", pady=5)

    return frame

# Modificación para crear la interfaz con tablas correctamente dimensionadas
def create_main_interface(description, expected_result):
    frame = tk.Frame(root, bg=SECONDARY_COLOR)
    
    # Botón de volver
    tk.Button(frame, text="Volver", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: switch_frame(create_exercise_menu)).pack(anchor="ne", padx=10, pady=10)

    left_panel = tk.Frame(frame, bg=ACCENT_COLOR, pady=10, padx=10)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(left_panel, text=description, bg=SECONDARY_COLOR, fg=ACCENT_COLOR, wraplength=500).pack(padx=10, pady=10)

    # Imagen del diagrama
    imagenDiagram = Image.open(r"C:\Users\chris\OneDrive\Pictures\Screenshots\DIAGRAMAAA.png")
    imagenDiagram = imagenDiagram.resize((700, 500))
    imagen_tk = ImageTk.PhotoImage(imagenDiagram)
    tk.Label(left_panel, image=imagen_tk, bg=ACCENT_COLOR).pack()
    left_panel.image = imagen_tk

    # Agregar texto "Output esperado:"
    tk.Label(left_panel, text="Output esperado:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 12, "bold")).pack(pady=10)

    # Determinar qué tabla mostrar con base en la descripción
    table_frame = tk.Frame(left_panel, bg=ACCENT_COLOR)
    table_frame.pack(pady=10)

    # Crear y configurar la tabla
    columns = ("Col1", "Col2")  # Establecer columnas generales, se reemplazan según la descripción
    data = expected_result  # Usar los datos directamente si están disponibles

    # Ejercicio "Empleados"
    if "Empleados" in description:
        columns = ("Nombre", "Apellido")
        data = [
            ('Sofía', 'Castro'),
            ('Ana', 'García'),
            ('José', 'González'),
            ('Carlos', 'Hernández'),
            ('Pedro', 'Jiménez'),
            ('María', 'López'),
            ('Luis', 'Martínez'),
            ('Juan', 'Pérez'),
            ('Laura', 'Ramírez'),
            ('Sandra', 'Torres'),
        ]
    # Ejercicio "Tecnologías disponibles"
    elif "Tecnologías disponibles" in description:
        columns = ("NombreTecnologia", "Descripcion")
        data = [
            ('AWS', 'Plataforma de servicios en la nube'),
            ('Azure', 'Plataforma de servicios en la nube de Microsoft'),
            ('Docker', 'Herramienta de contenedores'),
            ('Java', 'Lenguaje de programación orientado a objetos'),
            ('JavaScript', 'Lenguaje de programación para desarrollo web'),
            ('Kubernetes', 'Plataforma de orquestación de contenedores'),
            ('Linux', 'Sistema operativo de código abierto'),
            ('Node.js', 'Entorno de ejecución para JavaScript en el servidor'),
            ('Python', 'Lenguaje de programación versátil'),
            ('SQL', 'Lenguaje para gestión de bases de datos')
        ]
    # Ejercicio "Proyectos y presupuesto"
    elif "Proyectos y presupuesto" in description:
        columns = ("Nombre", "Presupuesto")
        data = [
            ('Data Warehouse', 300000.0),
            ('E-commerce', 280000.0),
            ('Migración a la Nube', 250000.0),
            ('Seguridad', 220000.0),
            ('Aplicación Móvil', 200000.0),
            ('Automatización', 180000.0),
            ('Sistema de Gestión', 150000.0),
            ('Rediseño Web', 120000.0),
            ('Chatbot', 100000.0),
            ('Monitorización', 90000.0),
        ]
    # Ejercicio "Tecnologías y habilidades"
    elif "Tecnologías y habilidades" in description:
        columns = ("Tecnología", "Habilidad")
        data = [
            ('AWS', 'Administrar servicios en la nube'),
            ('Azure', 'Desarrollar aplicaciones en la nube'),
            ('Docker', 'Crear contenedores'),
            ('Java', 'Desarrollar aplicaciones orientadas a objetos'),
            ('JavaScript', 'Desarrollar aplicaciones web interactivas'),
            ('Kubernetes', 'Orquestar contenedores'),
            ('Linux', 'Administrar servidores y sistemas operativos'),
            ('Node.js', 'Desarrollar aplicaciones del lado del servidor'),
            ('Python', 'Desarrollar aplicaciones de software de todo tipo'),
            ('SQL', 'Gestionar bases de datos relacionales')
        ]
    # Ejercicio "Proyectos y empleados versión 2"
    elif "Proyectos y empleados versión 2" in description:
        columns = ("Proyecto", "Empleado", "Rol")
        data = [
            ("Data Warehouse", "Sofía Castro", "Líder"),
            ("E-commerce", "Pedro Jiménez", "Desarrollador"),
            ("Migración a la Nube", "Ana García", "Técnico"),
            ("Seguridad", "Luis Martínez", "Líder"),
            ("Aplicación Móvil", "Carlos Hernández", "Desarrollador"),
            ("Automatización", "José González", "Técnico"),
            ("Sistema de Gestión", "María López", "Líder"),
            ("Rediseño Web", "Sandra Torres", "Desarrollador"),
            ("Chatbot", "Laura Ramírez", "Técnico"),
            ("Monitorización", "Juan Pérez", "Líder"),
        ]
    # Ejercicio "Empleados y habilidades"
    elif "Empleados y habilidades" in description:
        columns = ("Empleado", "Habilidad")
        data = [
            ('Sofía Castro', 'Administrar proyectos'),
            ('Ana García', 'Desarrollar en Python'),
            ('José González', 'Gestión de equipos'),
            ('Carlos Hernández', 'Desarrollar en JavaScript'),
            ('Pedro Jiménez', 'Administrar servidores Linux'),
            ('María López', 'Desarrollar en Java'),
            ('Luis Martínez', 'Administrar bases de datos SQL'),
            ('Juan Pérez', 'Desarrollar aplicaciones móviles'),
            ('Laura Ramírez', 'Desarrollar en Node.js'),
            ('Sandra Torres', 'Desarrollar en Docker'),
        ]
    # Ejercicio "Proyectos del 2023"
    elif "Proyectos del 2023" in description:
        columns = ("Proyecto", "Año")
        data = [
            ('Data Warehouse', 2023),
            ('E-commerce', 2023),
            ('Migración a la Nube', 2023),
            ('Seguridad', 2023),
            ('Aplicación Móvil', 2023),
            ('Automatización', 2023),
            ('Sistema de Gestión', 2023),
            ('Rediseño Web', 2023),
            ('Chatbot', 2023),
            ('Monitorización', 2023),
        ]
    # Otros ejercicios
    else:
        columns = ("Col1", "Col2")  # Personalizar según el ejercicio
        data = expected_result  # Usar los datos directamente si están disponibles

    # Crear la tabla
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Ajustar el ancho de las columnas para que se vean completas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")

    for row in data:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)

    # Panel derecho para la entrada de código
    right_panel = tk.Frame(frame, padx=10, pady=10, bg=SECONDARY_COLOR)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(right_panel, text="Escribe aquí tu código SQL:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR).pack(anchor="w", padx=10, pady=5)
    user_input = tk.Text(right_panel, width=80, height=20, bg="white")
    user_input.pack(anchor="w", pady=10)

    resultado_correcto = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_correcto.pack(pady=5)
    resultado_codigo = tk.Label(right_panel, text="", bg=SECONDARY_COLOR, fg=ACCENT_COLOR)
    resultado_codigo.pack(pady=5)

    table_frame = tk.Frame(right_panel, bg=SECONDARY_COLOR)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(right_panel, text="Ejecutar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: run_code(user_input, expected_result, resultado_correcto, resultado_codigo, table_frame)).pack(anchor="w", pady=5)
    tk.Button(right_panel, text="Verificar Código", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: verify_code(expected_result, resultado_correcto)).pack(anchor="w", pady=5)

    return frame



def create_exercise_menu():
    frame = tk.Frame(root, bg=SECONDARY_COLOR)
    tk.Button(frame, text="Volver", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: switch_frame(create_database_selection)).pack(anchor="ne", padx=10, pady=10)

    tk.Label(frame, text="Consultas de nivel básico:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 18, "bold")).pack(pady=20)
    tk.Button(frame, text="#Empleados", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(empleados_exercise)).pack(pady=10)
    tk.Button(frame, text="#Tecnologías disponibles", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(tecnologias_exercise)).pack(pady=10)
    tk.Button(frame, text="#Proyectos y presupuesto", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(proyectos_exercise)).pack(pady=10)

    tk.Label(frame, text="Consultas de nivel intermedio:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 18, "bold")).pack(pady=20)
    tk.Button(frame, text="#Empleados y habilidades", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(EmpleadosYHabilidades_exercise)).pack(pady=10)
    tk.Button(frame, text="#Empleados y sus tecnologias", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(EmpleadosYProyectos_exercise)).pack(pady=10)
    tk.Button(frame, text="#Proyectos y empleados", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(Certificaciones_exercise)).pack(pady=10)

    tk.Label(frame, text="Consultas de nivel avanzado:", bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 18, "bold")).pack(pady=20)
    tk.Button(frame, text="#Proyectos del 2023", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(Salario_exercise)).pack(pady=10)
    tk.Button(frame, text="#Tecnologías y habilidades", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(TecnologiasyHabilidades_exercise)).pack(pady=10)
    tk.Button(frame, text="#Proyectos y empleados version 2", bg=PRIMARY_COLOR, fg=TEXT_COLOR, command=lambda: open_exercise_interface(Proyempleados_exercise)).pack(pady=10)

    return frame

def create_database_selection():
    frame = tk.Frame(root, bg=SECONDARY_COLOR)
    frame.pack(fill="both", expand=True)
    content = tk.Frame(frame, bg=SECONDARY_COLOR)
    content.pack(expand=True)
    
    tk.Label(content, text="Seleccione la base de datos con la que desea practicar:", 
             bg=SECONDARY_COLOR, fg=ACCENT_COLOR, font=("Arial", 18, "bold")).pack(pady=50)
    # Botón ProyectoBD_MCJ
    tk.Button(content, text="ProyectoBD_MCJ", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Arial", 16, "bold"), command=lambda: switch_frame(create_exercise_menu)).pack(pady=20)
    
    # Botones adicionales
    tk.Button(content, text="Base de Datos 2", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(content, text="Base de Datos 3", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Arial", 16, "bold")).pack(pady=10)
    
    return frame


def create_start_screen():
    frame = tk.Frame(root, bg=PRIMARY_COLOR)
    frame.pack(fill="both", expand=True)
    content = tk.Frame(frame, bg=PRIMARY_COLOR)
    content.pack(expand=True)
    
    tk.Label(content, text="¡Bienvenido a SQLTrainer!", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Arial", 24, "bold")).pack(pady=50)
    tk.Button(content, text="PROBAR", bg=HIGHLIGHT_COLOR, fg=TEXT_COLOR, font=("Arial", 16, "bold"), command=lambda: switch_frame(create_database_selection)).pack(pady=20)
    return frame

# Configuración principal
root = tk.Tk()
root.title("SQLTrainer")
root.geometry("1200x800")
root.config(bg=SECONDARY_COLOR)
root.resizable(True, True)

switch_frame(create_start_screen)
root.mainloop()

# Configuración de la ventana principal
root = tk.Tk()
root.title("SQLTrainer")
root.geometry("1200x800")
root.config(bg="lightblue")
root.resizable(True, True)

# Pantalla inicial
switch_frame(create_start_screen)

# Ejecutar la interfaz
root.mainloop()