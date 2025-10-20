import csv
from datetime import datetime
import os

ARCHIVO = "equipos_control.csv"

def existe_archivo():
    return os.path.isfile(ARCHIVO)

def asegurar_archivo():
    if not existe_archivo():
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
            pass

# Crear equipo y guardar en el archivo
def crear_equipo():
    asegurar_archivo()
    id_equipo = input("ID del equipo: ").strip()
    nombre = input("Nombre del equipo: ").strip()
    tipo = input("Tipo (Sensor, Actuador, PLC): ").strip()
    try:
        valor_calibracion = float(input("Valor de calibración: "))
    except ValueError:
        print("Valor inválido.")
        return
    fecha_mantenimiento = input("Fecha último mantenimiento (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(fecha_mantenimiento, "%Y-%m-%d")
    except ValueError:
        print("Fecha inválida.")
        return
    with open(ARCHIVO, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([id_equipo, nombre, tipo, valor_calibracion, fecha_mantenimiento])
    print("Equipo agregado.")

# Lectura secuencial
def lectura_secuencial():
    if not existe_archivo():
        print("No hay archivo aún.")
        return
    with open(ARCHIVO, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for linea in reader:
            if linea:
                print(f"ID: {linea[0]} | Nombre: {linea[1]} | Tipo: {linea[2]} | Calibración: {linea[3]} | Mant.: {linea[4]}")

# Índice de posiciones para acceso directo
def construir_indice_offset():
    indices = {}
    if not existe_archivo():
        return indices
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        while True:
            pos = f.tell()
            linea = f.readline()
            if not linea:
                break
            partes = linea.strip().split(",")
            if len(partes) > 0:
                indices[partes[0]] = pos
    return indices

# Búsqueda por acceso directo
def buscar_por_id(id_buscar):
    if not existe_archivo():
        print("No hay archivo.")
        return
    indices = construir_indice_offset()
    if id_buscar not in indices:
        print("No encontrado.")
        return
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        f.seek(indices[id_buscar])
        linea = f.readline().strip().split(",")
        if len(linea) >= 5:
            print(f"ID: {linea[0]} | Nombre: {linea[1]} | Tipo: {linea[2]} | Calibración: {linea[3]} | Mant.: {linea[4]}")

# Índice por tipo
def construir_indice_tipo():
    indice = {}
    if not existe_archivo():
        return indice
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for linea in reader:
            if len(linea) >= 3:
                tipo = linea[2]
                indice.setdefault(tipo, []).append(linea)
    return indice

# Listar por tipo (indexado)
def listar_por_tipo(tipo_equipo):
    indice = construir_indice_tipo()
    if tipo_equipo in indice:
        for r in indice[tipo_equipo]:
            print(f"ID: {r[0]} | Nombre: {r[1]} | Calib.: {r[3]} | Mant.: {r[4]}")
    else:
        print("No hay equipos de ese tipo.")

# Filtrar por fechas
def listar_mantenimiento(fecha_inicio, fecha_fin):
    if not existe_archivo():
        print("No hay archivo.")
        return
    try:
        f1 = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        f2 = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        print("Fechas inválidas.")
        return
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for linea in reader:
            if len(linea) >= 5:
                try:
                    fecha_m = datetime.strptime(linea[4], "%Y-%m-%d")
                    if f1 <= fecha_m <= f2:
                        print(f"ID: {linea[0]} | Nombre: {linea[1]} | Tipo: {linea[2]} | Mant.: {linea[4]}")
                except ValueError:
                    continue

# Menú principal
def menu():
    asegurar_archivo()
    while True:
        print("\n--- MENÚ ---")
        print("1. Agregar equipo")
        print("2. Lectura secuencial")
        print("3. Buscar por ID (acceso directo)")
        print("4. Listar por tipo (indexado)")
        print("5. Listar por rango de mantenimiento")
        print("6. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            crear_equipo()
        elif op == "2":
            lectura_secuencial()
        elif op == "3":
            buscar_por_id(input("ID a buscar: ").strip())
        elif op == "4":
            listar_por_tipo(input("Tipo: ").strip())
        elif op == "5":
            f1 = input("Fecha inicio (YYYY-MM-DD): ").strip()
            f2 = input("Fecha fin (YYYY-MM-DD): ").strip()
            listar_mantenimiento(f1, f2)
        elif op == "6":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()