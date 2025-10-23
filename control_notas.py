# ==========================================
# SISTEMA DE CONTROL DE MATRÍCULA Y NOTAS (con FICHEROS)
# Universidad Nacional Autónoma de Nicaragua - León
# ==========================================
# Autores: Carlos Alfonso Juarez Chevez, Wiston Emilio Laínez Balladares,
# Sergio Angel Maldonado Serrano y Natasha Michelle Espinosa Fonseca
# ==========================================

import re
import json
import os

ARCHIVO = "estudiantes.json"

# ---------- FUNCIONES DE VALIDACIÓN ----------

def validar_carnet(carnet):
    patron = r"^\d{2}-\d{5}-\d$"
    if not re.match(patron, carnet):
        raise ValueError("Carnet inválido. Ejemplo válido: 25-02395-0")
    return carnet

def validar_estado_civil(estado):
    opciones = ["soltero", "casado", "divorciado", "viudo"]
    if estado.lower() not in opciones:
        raise ValueError("Estado civil inválido. Opciones: Soltero, Casado, Divorciado, Viudo.")
    return estado.capitalize()

def validar_sexo(sexo):
    if sexo.upper() not in ["M", "F"]:
        raise ValueError("Sexo inválido. Debe ser M o F.")
    return sexo.upper()

def validar_cedula(cedula):
    patron = r"^\d{3}-\d{6}-\d{4}[A-Z]$"
    if not re.match(patron, cedula):
        raise ValueError("Cédula inválida. Ejemplo válido: 001-123456-0000A")
    return cedula

def validar_anio(anio):
    if not anio.isdigit() or not (1 <= int(anio) <= 6):
        raise ValueError("Año inválido. Debe estar entre 1 y 6.")
    return int(anio)

def validar_nota(nota):
    try:
        nota = float(nota)
        if nota < 0 or nota > 100:
            raise ValueError
    except ValueError:
        raise ValueError("Nota inválida. Debe estar entre 0 y 100.")
    return nota

def validar_ingreso(monto):
    try:
        monto = float(monto)
        if monto < 0:
            raise ValueError
    except ValueError:
        raise ValueError("Monto inválido. Debe ser un número positivo.")
    return monto

# ---------- FUNCIONES DE ARCHIVO ----------

def cargar_estudiantes():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_estudiantes(estudiantes):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(estudiantes, f, ensure_ascii=False, indent=4)

# ---------- FUNCIONES PRINCIPALES ----------

def agregar_estudiante(estudiantes):
    while True:  #  Si hay error, vuelve a empezar todo el registro
        try:
            print("\n===========================================")
            print("           REGISTRO DE MATRÍCULA")
            print("===========================================")

            carnet = validar_carnet(input("Carnet (ejemplo 25-02395-0): "))
            nombre = input("Nombre completo: ").title()
            estado_civil = validar_estado_civil(input("Estado civil (Soltero/Casado/Divorciado/Viudo): "))
            sexo = validar_sexo(input("Sexo (M/F): "))
            cedula = validar_cedula(input("Cédula (001-250108-1001B): "))
            direccion = input("Dirección: ").title()
            departamento = input("Departamento: ").title()
            municipio = input("Municipio: ").title()
            area_conocimiento = input("Área de conocimiento: ").title()
            carrera = input("Carrera: ").title()
            anio = validar_anio(input("Año de estudio (1-6): "))
            plan_estudio = input("Plan de estudio: ").upper()
            ingreso_padre = validar_ingreso(input("Ingreso mensual del padre: "))

            # 🔸 Pregunta si desea agregar notas después de datos personales
            agregar_notas = input("\n¿Desea ingresar notas para este estudiante? (S/N): ").upper()
            notas = []

            if agregar_notas == "S":
                print("\n--- Ingreso de notas académicas ---")
                while True:
                    materia = input("Nombre de la materia (o ENTER para terminar): ").title()
                    if materia == "":
                        break
                    nota = validar_nota(input(f"Ingrese la nota de {materia} (0-100): "))
                    notas.append({"materia": materia, "nota": nota})

            if not notas:
                print("\n No se ingresaron notas. El registro no se guardará.\n")
                return

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
                "ingreso_padre": ingreso_padre,
                "notas": notas
            })

            guardar_estudiantes(estudiantes)
            print(f"\n Estudiante '{nombre}' matriculado correctamente y guardado en fichero.\n")
            break  # Salimos si no hubo errores

        except ValueError as e:
            print(f"\n Error: {e}")
            print("Se reiniciará el registro. Vuelva a ingresar todos los datos.\n")
            # Si querés limpiar la pantalla aquí:
            # os.system("cls" if os.name == "nt" else "clear")

def mostrar_matricula(est):
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
    print(f"Ingreso Padre:    C${est['ingreso_padre']:.2f}")
    print("-------------------------------------------")
    print("            DETALLE DE NOTAS")
    print("-------------------------------------------")
    print(f"{'Materia':<25}{'Nota':>10}{'Estado':>15}")
    print("-" * 50)
    for n in est["notas"]:
        estado = "Aprobado" if n["nota"] >= 60 else "Reprobado"
        print(f"{n['materia']:<25}{n['nota']:>10.2f}{estado:>15}")
    print("-" * 50)

def buscar_estudiante(estudiantes):
    carnet = input("\nIngrese el carnet del estudiante a buscar: ")
    for est in estudiantes:
        if est["carnet"] == carnet:
            mostrar_matricula(est)
            return
    print("\nNo se encontró un estudiante con ese carnet.\n")

def eliminar_estudiante(estudiantes):
    carnet = input("\nIngrese el carnet del estudiante a eliminar: ")
    for i, est in enumerate(estudiantes):
        if est["carnet"] == carnet:
            confirm = input(f"¿Seguro que desea eliminar a {est['nombre']}? (S/N): ").upper()
            if confirm == "S":
                estudiantes.pop(i)
                guardar_estudiantes(estudiantes)
                print("\nEstudiante eliminado y fichero actualizado.\n")
            else:
                print("\nOperación cancelada.\n")
            return
    print("\nNo se encontró un estudiante con ese carnet.\n")

def actualizar_estudiante(estudiantes):
    carnet = input("\nIngrese el carnet del estudiante a actualizar: ")
    for est in estudiantes:
        if est["carnet"] == carnet:
            print(f"\nActualizando datos de {est['nombre']}")
            nuevo_nombre = input(f"Nombre ({est['nombre']}): ").title() or est['nombre']
            est['nombre'] = nuevo_nombre

            nueva_carrera = input(f"Carrera ({est['carrera']}): ").title() or est['carrera']
            est['carrera'] = nueva_carrera

            opc = input("¿Desea actualizar notas? (S/N): ").upper()
            if opc == "S":
                est['notas'].clear()
                while True:
                    materia = input("Nombre de la materia (o ENTER para terminar): ").title()
                    if materia == "":
                        break
                    nota = validar_nota(input(f"Ingrese la nota de {materia} (0-100): "))
                    est['notas'].append({"materia": materia, "nota": nota})
            guardar_estudiantes(estudiantes)
            print("\nDatos actualizados y guardados en fichero.\n")
            return
    print("\nNo se encontró un estudiante con ese carnet.\n")

def calcular_promedio(estudiantes):
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
    estudiantes = cargar_estudiantes()
    while True:
        print("\n===========================================")
        print("     SISTEMA DE MATRÍCULA Y CONTROL DE NOTAS")
        print("===========================================")
        print(" 1️. Registrar nuevo estudiante")
        print(" 2️. Buscar estudiante por carnet")
        print(" 3️. Mostrar todos los estudiantes")
        print(" 4️. Calcular promedio general")
        print(" 5️. Salir")
        print(" 6️. Eliminar estudiante")
        print(" 7️. Actualizar estudiante")
        print("===========================================")

        opcion = input("Seleccione una opción (1-7): ")

        if opcion == "1":
            agregar_estudiante(estudiantes)
        elif opcion == "2":
            buscar_estudiante(estudiantes)
        elif opcion == "3":
            mostrar_todos(estudiantes)
        elif opcion == "4":
            calcular_promedio(estudiantes)
        elif opcion == "5":
            print("\n Gracias por usar el Sistema de control de notas.\n")
            break
        elif opcion == "6":
            eliminar_estudiante(estudiantes)
        elif opcion == "7":
            actualizar_estudiante(estudiantes)
        else:
            print("\n Opción inválida. Intente de nuevo.\n")

if __name__ == "__main__":
    main()

