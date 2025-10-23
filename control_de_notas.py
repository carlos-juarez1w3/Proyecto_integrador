# ==========================================
# SISTEMA DE CONTROL DE MATRÍCULA Y NOTAS
# Universidad Nacional Autónoma de Nicaragua - León
# ==========================================
# Autores: Carlos Alfonso Juarez Chevez, Wiston Emilio Laínez Balladares, Sergio Angel Maldonado Serrano y
# Natasha Michelle Espinosa Fonseca
# Descripción: Sistema de control de notas
# Registro completo de estudiantes, validación de datos
# y control de múltiples notas académicas.
# ==========================================

import re

# ---------- FUNCIONES DE VALIDACIÓN ----------

def validar_carnet(carnet):
    """Valida el formato del carnet (##-#####-#)."""
    patron = r"^\d{2}-\d{5}-\d$"
    if not re.match(patron, carnet):
        raise ValueError("Carnet inválido. Ejemplo válido: 25-02395-0")
    return carnet


def validar_estado_civil(estado):
    """Valida el estado civil del estudiante."""
    opciones = ["soltero", "casado", "divorciado", "viudo"]
    if estado.lower() not in opciones:
        raise ValueError("Estado civil inválido. Opciones: Soltero, Casado, Divorciado, Viudo.")
    return estado.capitalize()


def validar_sexo(sexo):
    """Valida el sexo (M/F)."""
    if sexo.upper() not in ["M", "F"]:
        raise ValueError("Sexo inválido. Debe ser M (masculino) o F (femenino).")
    return sexo.upper()


def validar_cedula(cedula):
    """Valida el formato de la cédula nicaragüense."""
    patron = r"^\d{3}-\d{6}-\d{4}[A-Z]$"
    if not re.match(patron, cedula):
        raise ValueError("Cédula inválida. Ejemplo válido: 001-123456-0000A")
    return cedula


def validar_anio(anio):
    """Valida el año de estudio (1 a 6)."""
    if not anio.isdigit() or not (1 <= int(anio) <= 6):
        raise ValueError("Año inválido. Debe estar entre 1 y 6.")
    return int(anio)


def validar_nota(nota):
    """Valida una nota entre 0 y 100."""
    try:
        nota = float(nota)
        if nota < 0 or nota > 100:
            raise ValueError("La nota debe estar entre 0 y 100.")
    except ValueError:
        raise ValueError("Nota inválida. Debe ser un número entre 0 y 100.")
    return nota


# ---------- FUNCIONES PRINCIPALES ----------

def agregar_estudiante(estudiantes):
    """Registra un nuevo estudiante con múltiples notas."""
    try:
        print("\n===========================================")
        print("           REGISTRO DE MATRÍCULA")
        print("===========================================")
        carnet = validar_carnet(input("Carnet (ejemplo 25-02395-0): "))
        nombre = input("Nombre completo: ").title()
        estado_civil = validar_estado_civil(input("Estado civil (Soltero/Casado/Divorciado/Viudo): "))
        sexo = validar_sexo(input("Sexo (M/F): "))
        cedula = validar_cedula(input("Cédula (001-123456-0000A): "))
        direccion = input("Dirección: ").title()
        departamento = input("Departamento: ").title()
        municipio = input("Municipio: ").title()
        area_conocimiento = input("Área de conocimiento: ").title()
        carrera = input("Carrera: ").title()
        anio = validar_anio(input("Año de estudio (1-6): "))
        plan_estudio = input("Plan de estudio: ").upper()

        # Registrar múltiples notas
        notas = []
        print("\n--- Ingreso de notas académicas ---")
        while True:
            materia = input("Nombre de la materia (o presione ENTER para terminar): ").title()
            if materia == "":
                break
            nota = validar_nota(input(f"Ingrese la nota de {materia} (0-100): "))
            notas.append({"materia": materia, "nota": nota})

        if not notas:
            print("   No se ingresaron notas. El registro no se guardará.")
            return

        # Guardar toda la información
        estudiantes.append({
            "carnet": carnet,
            "nombre": nombre,
            "estado_civil": estado_civil,
            "sexo": sexo,
            "cedula": cedula,
            "direccion": direccion,
            "departamento": departamento,
            "municipio": municipio,
            "area_conocimiento": area_conocimiento,
            "carrera": carrera,
            "anio": anio,
            "plan_estudio": plan_estudio,
            "notas": notas
        })
        print(f"\n  Estudiante '{nombre}' matriculado correctamente.\n")

    except ValueError as e:
        print(f"\n Error: {e}\n")


def mostrar_matricula(est):
    """Imprime la información del estudiante en formato de hoja de matrícula."""
    print("\n===========================================")
    print("          HOJA DE MATRÍCULA - UNAN-León")
    print("===========================================\n")
    print(f"Carnet:           {est['carnet']}")
    print(f"Nombre completo:  {est['nombre']}")
    print(f"Cédula:           {est['cedula']}")
    print(f"Sexo:             {est['sexo']}")
    print(f"Estado civil:     {est['estado_civil']}")
    print(f"Dirección:        {est['direccion']}")
    print(f"Departamento:     {est['departamento']}")
    print(f"Municipio:        {est['municipio']}")
    print(f"Área:             {est['area_conocimiento']}")
    print(f"Carrera:          {est['carrera']}")
    print(f"Año:              {est['anio']}")
    print(f"Plan de estudio:  {est['plan_estudio']}")
    print("-------------------------------------------")
    print("            DETALLE DE NOTAS")
    print("-------------------------------------------")
    print(f"{'Materia':<25}{'Nota':>10}{'Estado':>15}")
    print("-" * 50)
    for n in est["notas"]:
        estado = "Aprobado ✅" if n["nota"] >= 60 else "Reprobado ❌"
        print(f"{n['materia']:<25}{n['nota']:>10.2f}{estado:>15}")
    print("-" * 50)


def buscar_estudiante(estudiantes):
    """Busca e imprime la hoja de matrícula de un estudiante."""
    carnet = input("\nIngrese el carnet del estudiante a buscar: ")
    for est in estudiantes:
        if est["carnet"] == carnet:
            mostrar_matricula(est)
            return
    print("\nNo se encontró un estudiante con ese carnet.\n")


def calcular_promedio(estudiantes):
    """Calcula el promedio general de todas las notas."""
    print("\n=== PROMEDIO GENERAL ===")
    if not estudiantes:
        print("No hay estudiantes registrados.\n")
        return

    total_notas = 0
    cantidad_notas = 0
    for est in estudiantes:
        for n in est["notas"]:
            total_notas += n["nota"]
            cantidad_notas += 1

    promedio = total_notas / cantidad_notas if cantidad_notas > 0 else 0
    print(f"Promedio general de notas: {promedio:.2f}\n")


def mostrar_todos(estudiantes):
    """Muestra un resumen de todos los estudiantes registrados."""
    print("\n=== LISTA GENERAL DE ESTUDIANTES ===")
    if not estudiantes:
        print("No hay estudiantes registrados.\n")
        return

    print(f"{'CARNET':<15}{'NOMBRE':<30}{'CARRERA':<25}{'PROMEDIO':<10}")
    print("-" * 80)

    for est in estudiantes:
        promedio = sum(n["nota"] for n in est["notas"]) / len(est["notas"])
        print(f"{est['carnet']:<15}{est['nombre']:<30}{est['carrera']:<25}{promedio:<10.2f}")
    print("-" * 80 + "\n")


# ---------- PROGRAMA PRINCIPAL ----------

def main():
    estudiantes = []
    while True:
        print("\n===========================================")
        print("     SISTEMA DE MATRÍCULA Y CONTROL DE NOTAS")
        print("===========================================")
        print(" 1️.Registrar nuevo estudiante")
        print(" 2️.Buscar estudiante por carnet")
        print(" 3️.Mostrar todos los estudiantes")
        print(" 4️.Calcular promedio general")
        print(" 5️.Salir")
        print("===========================================")

        opcion = input("Seleccione una opción (1-5): ")

        if opcion == "1":
            agregar_estudiante(estudiantes)
        elif opcion == "2":
            buscar_estudiante(estudiantes)
        elif opcion == "3":
            mostrar_todos(estudiantes)
        elif opcion == "4":
            calcular_promedio(estudiantes)
        elif opcion == "5":
            print("\n Gracias por usar  nuestro el Sistema de control de notas.\n")
            break
        else:
            print("\n Opción inválida. Intente de nuevo.\n")


if __name__ == "__main__":
    main()
