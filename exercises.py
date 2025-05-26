# exercises.py

def empleados_exercise():
    """Consulta básica: Empleados"""
    description = "Listar los nombres y apellidos de los empleados ordenados alfabéticamente por apellido."
    expected_result = [
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
    return description, expected_result


def tecnologias_exercise():
    """Consulta básica: Tecnologías disponibles"""
    description = "Mostrar las tecnologías disponibles ordenadas alfabéticamente por su nombre."
    expected_result = [
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
    return description, expected_result

def proyectos_exercise():
    """Consulta básica: Proyectos y presupuestos"""
    description = "Listar los nombres de los proyectos y su presupuesto ordenados por presupuesto descendente."
    expected_result = [
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
    return description, expected_result






def EmpleadosYHabilidades_exercise():
    """Consulta intermedia: Empleados, habilidades y niveles"""
    description = "Listar los empleados con sus habilidades y niveles, ordenados por el nivel de habilidad (Avanzado, Intermedio, Básico)."
    
    expected_result = [
        ("Sofía","Castro","Node.js","Avanzado"),
        ("Pedro","Jiménez","Linux","Avanzado"),
        ("María","López","SQL","Avanzado"),
        ("Juan","Pérez","Java","Avanzado"),
        ("Laura","Ramírez","Kubernetes","Avanzado"),
        ("Ana","García","Python","Intermedio"),
        ("Carlos","Hernández","Docker","Intermedio"),
        ("Sandra","Torres","Azure","Intermedio"),
        ("José","González","AWS","Básico"),
        ("Luis","Martínez","JavaScript","Básico")
    ]
    
    return description, expected_result



def EmpleadosYProyectos_exercise():
    """Consulta intermedia: Empleados y sus tecnologias"""
    description = "Listar las tecnologías que dominan los empleados, junto con el nivel de habilidad, ordenado por nivel de habilidad en orden descendente."
    
    expected_result = [
        ("Juan", "Pérez", "Java", "Avanzado"),
        ("Laura", "Ramírez", "Kubernetes", "Avanzado"),
        ("María", "López", "SQL", "Avanzado"),
        ("Pedro", "Jiménez", "Linux", "Avanzado"),
        ("Sofía", "Castro", "Node.js", "Avanzado"),
        ("Ana", "García", "Python", "Intermedio"),
        ("Carlos", "Hernández", "Docker", "Intermedio"),
        ("Sandra", "Torres", "Azure", "Intermedio"),
        ("José", "González", "AWS", "Básico"),
        ("Luis", "Martínez", "JavaScript", "Básico")
    ]
    
    return description, expected_result


def Certificaciones_exercise():
    """Consulta Avanzada: Empleados y proyectos ver.2"""
    description = """Obtener el nombre de los empleados junto con la tecnología en la que tienen nivel avanzado y el proyecto al que están asignados,
    ordenados por el nombre del proyecto en orden ascendente y, dentro de cada proyecto, por el nombre del empleado en orden descendente."""
    expected_result = [
        ("Laura", "Ramírez", "Kubernetes", "Data Warehouse"),
        ("Sofía", "Castro", "Node.js", "E-commerce"),
        ("María", "López", "SQL", "Rediseño Web"),
        ("Pedro", "Jiménez", "Linux", "Seguridad"),
        ("Juan", "Pérez", "Java", "Sistema de Gestión")
    ]
    
    return description, expected_result
    






def Salario_exercise():
    """Consulta intermedia: Proyectos del 2023"""
    description = "Obtener los proyectos iniciados en 2023 y el número total de empleados asignados a cada proyecto."
    
    expected_result =   expected_result = [
        ("Aplicación Móvil", 1),
        ("Automatización", 1),
        ("Chatbot", 1),
        ("Data Warehouse", 1),
        ("E-commerce", 1),
        ("Migración a la Nube", 1),
        ("Monitorización", 1),
        ("Rediseño Web", 1),
        ("Seguridad", 1),
        ("Sistema de Gestión", 1)
    ]
    
    return description, expected_result



def TecnologiasyHabilidades_exercise():
    """Consulta Avanzada: Tecnologías y habilidades"""
    description = "Listar las tecnologías con el promedio de niveles de habilidad de los empleados, ordenadas por el promedio más alto."
    expected_result = [
        ("Java",3),
        ("Kubernetes",3),
        ("Linux",3),
        ("Node.js",3),
        ("SQL",3 ),
        ("Python",2),
        ("Azure",2),
        ("Docker",2),
        ("JavaScript",1),
        ("AWS",1),
    ]
    
    return description, expected_result

def Proyempleados_exercise():
    """Consulta Avanzada: Proyectos y empleados"""
    description = "Obtener los proyectos con mayor cantidad de empleados asignados, ordenados por el número de empleados descendente."
    expected_result = [
        ('Aplicación Móvil', 1),
        ('Automatización', 1),
        ('Chatbot', 1),
        ('Data Warehouse', 1),
        ('E-commerce', 1),
        ('Migración a la Nube', 1),
        ('Monitorización', 1),
        ('Rediseño Web', 1),
        ('Seguridad', 1),
        ('Sistema de Gestión', 1)
    ]
    
    return description, expected_result
