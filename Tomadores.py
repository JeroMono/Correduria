import Utilidades
import Polizas
import json

def menu_tomadores():
    """Menu de tomadores, permite crear, modificar o eliminar un tomador"""
    opcion_tomadores = "0"
    while opcion_tomadores != "9":
        print("1. Crear tomador")
        print("2. Modificar tomador")
        print("3. Eliminar tomador")
        print("9. Volver")
        opcion_tomadores = input("Introduce una opción: ")
        match opcion_tomadores:
            case "1":
                crear_tomador()
            case "2":
                modificar_tomador()
            case "3":
                eliminar_tomador()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")
    

def crear_tomador():
    """Pide datos para crear un tomador, los guarda en un diccionario y lo añade a la lista de tomadores"""
    global listaTomadores
    print("Creando tomador")
    id_tomador = configurar_tomador()
    
    if id_tomador == "!salir":
        return
    
    denominacion = input("Introduce el nombre de la persona o empresa: ")
    fecha_nacimiento = configurar_fecha(id_tomador)
    domicilio = configurar_domicilio()
    movil_contacto = configurar_movil_contacto()
    email_contacto = configurar_email_contacto()
    listaTomadores.append({"id_tomador":id_tomador, "denominacion":denominacion, "fecha_nacimiento":fecha_nacimiento, "domicilio":domicilio, "movil_contacto":movil_contacto, "email_contacto":email_contacto})
    guardar_tomadores()
    print("Tomador creado")

def modificar_tomador():
    """Pide el DNI, NIE o CIF del tomador a modificar, muestra los datos y entra en un menu que permite modificarlos"""
    listar_tomadores()
    id_tomador = configurar_tomador(True)
    if id_tomador == "!salir":
        return
    for dato in listaTomadores:
        if dato["id_tomador"] == id_tomador:
            tomador_eleccion = dato
    
    while True:
        listar_tomador(tomador_eleccion)
        opcion_modificar = input("Introduce una opción: ")
        match opcion_modificar:
            case "1":
                dato["denominacion"] = input("Introduce la nueva denominación: ")
            case "2":
                dato["fecha_nacimiento"] = configurar_fecha(id_tomador)
            case "3":
                dato["domicilio"] = configurar_domicilio()
            case "4":
                dato["movil_contacto"] = configurar_movil_contacto()
            case "5":
                dato["email_contacto"] = configurar_email_contacto()
            case "9":
                print("Volviendo al menú de Tomadores")
                break
            case _:
                print("Opción incorrecta")

def eliminar_tomador():
    """Selecciona un tomador y si es posible lo elimina de la lista de tomadores"""
    listar_tomadores()
    id_tomador = configurar_tomador(True)
    if id_tomador == "!salir":
        return
    for dato in listaTomadores:
        if dato["id_tomador"] == id_tomador:
            print(f"ID: {dato['id_tomador']}, Denominación: {dato['denominacion']}")
            if dato["id_tomador"] == id_tomador:
                tomador_eleccion = dato
    
    polizas_no_activas = []
    for poliza in Polizas.listaPolizas:
        if poliza["id_tomador"] == tomador_eleccion["id_tomador"]:
            if Polizas.comprobar_vigencia(poliza):
                print(f"El tomador tiene una póliza activa, no se puede borrar")
                break
            else:
                polizas_no_activas.append(poliza)
    else:
        confirmacion = input("¿Estás seguro de que quieres borrar el tomador? (s/n): ")
        if confirmacion == "s":
            if polizas_no_activas:
                for poliza in polizas_no_activas:
                    Polizas.listaPolizas.remove(poliza)
                    Polizas.guardar_polizas()
            listaTomadores.remove(tomador_eleccion)
            guardar_tomadores()
            print("Tomador eliminado")

def listar_tomadores() -> None:
    """Muestra una lista de tomadores con su ID y denominación"""
    for datos in listaTomadores:
        print(f"ID: {datos['id_tomador']}, Denominación: {datos['denominacion']}")

def listar_tomador(tomador:dict) -> None:
    """Muestra los datos de un tomador"""
    print(f"ID: {tomador['id_tomador']}, Denominación: {tomador['denominacion']}")
    print(f"1. Denominación: {tomador['denominacion']}")
    print(f"2. Fecha de nacimiento: {tomador['fecha_nacimiento']}")
    print(f"3. Domicilio: {tomador['domicilio']}")
    print(f"4. Móvil de contacto: {tomador['movil_contacto']}")
    print(f"5. Email de contacto: {tomador['email_contacto']}")
    print("9. Volver")

def cargar_tomadores() -> None:
    """Carga los tomadores guardados en el archivo tomadores.json"""
    global listaTomadores
    try:
        with open("tomadores.json", "r") as archivo_tomadores:
            listaTomadores = json.load(archivo_tomadores)
    except:
        print(f"No existe tomadores guardados")

def guardar_tomadores() -> None:
    """Guarda los tomadores en el archivo tomadores.json"""
    try:
        with open("tomadores.json", "w") as archivo_tomadores:
            json.dump(listaTomadores, archivo_tomadores, indent=4)
    except:
        print(f"Error al guardar los tomadores")


def configurar_tomador(modificando:bool=False) -> str:
    """Pide el DNI, NIE o CIF del tomador y devuelve el valor introducido. Si el valor ya existe en la lista de tomadores, lo indica y pide otro valor. Si el valor introducido no es correcto, lo indica y pide otro valor."""
    while True:
        tomador_id = input("Introduce el DNI, NIE o CIF del tomador (!salir): ")
        if tomador_id == "!salir":
            return tomador_id
        elif tomador_id in [tomador["id_tomador"] for tomador in listaTomadores] and not modificando:
            print("El tomador ya existe")
        elif tomador_id not in [tomador["id_tomador"] for tomador in listaTomadores] and modificando:
            print("El tomador no existe")
        elif Utilidades.comprobar_dni(tomador_id)[0]:
            return tomador_id
        else:
            print("DNI, NIE o CIF incorrecto")


def configurar_fecha(tomador_id) -> str:
    """Pide la fecha de nacimiento en caso de ser una persona física y devuelve el valor introducido"""
    # Si es DNI o NIE
    if Utilidades.comprobar_dni(tomador_id)[1]:
        while True:
            fecha = input("Introduce la fecha de nacimiento del tomador dd/mm/aaaa: ")
            # Devuelve la fecha en formato dd/mm/aaaa si es correcta
            fecha = Utilidades.validar_fecha(fecha)
            if fecha:
                return fecha
    # Si es CIF no pedimos data y dejamos vacío
    else:
        return ""

def configurar_domicilio() -> str:
    """Pide la dirección del tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce la dirección del tomador: ")
        if entrada:
            return entrada


def configurar_movil_contacto() -> str:
    """Pide el teléfono del tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce el teléfono del tomador: ")
        if Utilidades.validar_telefono(entrada):
            return entrada


def configurar_email_contacto() -> str:
    """ Pide el email del tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce el email del tomador: ")
        if Utilidades.validar_email(entrada):
            return entrada

listaTomadores = list()