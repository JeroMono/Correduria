import Utilidades
import Polizas
import json

def mostrar_menu_tomadores() -> None:
    """Menu de tomadores, permite crear, modificar o eliminar un tomador"""
    opcion_tomadores = "0"
    while opcion_tomadores != "9":
        Utilidades.limpiar_pantalla()
        print("1. Crear tomador")
        print("2. Modificar tomador")
        print("3. Eliminar tomador")
        print("9. Volver")
        opcion_tomadores = input("Introduce una opción: ")
        match opcion_tomadores:
            case "1":
                mostrar_menu_crear_tomador()
            case "2":
                mostrar_menu_modificar_tomador()
            case "3":
                mostrar_menu_eliminar_tomador()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")

def mostrar_menu_crear_tomador() -> None:
    """Pide datos para crear un tomador, los guarda en un diccionario y lo añade a la lista de tomadores"""
    global listaTomadores
    Utilidades.limpiar_pantalla()
    print("Creando tomador")
    id_tomador = configurar_tomador()
    if id_tomador == "":
        return
    
    denominacion = configurar_descripcion()
    fecha_nacimiento = configurar_fecha_nacimiento(id_tomador)
    domicilio = configurar_domicilio()
    movil_contacto = configurar_movil_contacto()
    email_contacto = configurar_email_contacto()
    tomador = {"id_tomador":id_tomador, "denominacion":denominacion, "fecha_nacimiento":fecha_nacimiento, "domicilio":domicilio, "movil_contacto":movil_contacto, "email_contacto":email_contacto}

    
    while True:
        Utilidades.limpiar_pantalla()
        listar_tomador(tomador, True)
        confirmacion = input("¿Estás seguro de que quieres crear el tomador? (s/n): ").lower()
        if confirmacion == "s":
            listaTomadores.append(tomador)
            guardar_tomadores()
            print("Tomador creado")
            break
        elif confirmacion == "n":
            print("Tomador no creado")

def mostrar_menu_modificar_tomador() -> None:
    """Pide el DNI, NIE o CIF del tomador a modificar, muestra los datos y entra en un menu que permite modificarlos"""
    Utilidades.limpiar_pantalla()
    listar_tomadores()
    id_tomador = configurar_tomador(True)
    if id_tomador == "":
        return
    for dato in listaTomadores:
        if dato["id_tomador"] == id_tomador:
            tomador_eleccion = dato
    
    while True:
        Utilidades.limpiar_pantalla()
        listar_tomador(tomador_eleccion)
        opcion_modificar = input("Introduce una opción: ")
        match opcion_modificar:
            case "1":
                dato["denominacion"] = configurar_descripcion(tomador_eleccion)
            case "2":
                dato["fecha_nacimiento"] = configurar_fecha_nacimiento(id_tomador,tomador_eleccion)
            case "3":
                dato["domicilio"] = configurar_domicilio(tomador_eleccion)
            case "4":
                dato["movil_contacto"] = configurar_movil_contacto(tomador_eleccion)
            case "5":
                dato["email_contacto"] = configurar_email_contacto(tomador_eleccion)
            case "9":
                print("Volviendo al menú de Tomadores")
                break
            case _:
                print("Opción incorrecta")

def mostrar_menu_eliminar_tomador() -> None:
    """Selecciona un tomador y si es posible lo elimina de la lista de tomadores"""
    Utilidades.limpiar_pantalla()
    listar_tomadores()
    id_tomador = configurar_tomador(True)
    if id_tomador == "":
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
        confirmacion = input("¿Estás seguro de que quieres borrar el tomador? (s/n): ").lower()
        if confirmacion == "s":
            if polizas_no_activas:
                for poliza in polizas_no_activas:
                    Polizas.eliminar_poliza(poliza)
                    Polizas.guardar_polizas()
            listaTomadores.remove(tomador_eleccion)
            guardar_tomadores()
            print("Tomador eliminado")
    input("Pulse <Enter> para continuar")

def listar_tomadores() -> None:
    """Muestra una lista de tomadores con su ID y denominación"""
    print(f"{'ID':<15}{'Denominación':<30}")
    print("="*45)
    for datos in listaTomadores:
        print(f"{datos['id_tomador']:<15}{datos['denominacion']:<30}")

def listar_tomador(tomador:dict, creando:bool = False) -> None:
    """Muestra los datos de un tomador"""
    print("Modifcando tomador:" if not creando else "Confirmando Tomador:")
    print(f"ID: {tomador['id_tomador']}")
    print(f"1. Denominación: {tomador['denominacion']}")
    print(f"2. Fecha de nacimiento: {tomador['fecha_nacimiento']}")
    print(f"3. Domicilio: {tomador['domicilio']}")
    print(f"4. Móvil de contacto: {tomador['movil_contacto']}")
    print(f"5. Email de contacto: {tomador['email_contacto']}")
    if not creando:
        print("9. Volver")

def cargar_tomadores() -> None:
    """Carga los tomadores guardados en el archivo tomadores.json"""
    global listaTomadores
    try:
        with open("tomadores.json", "r") as archivo_tomadores:
            listaTomadores = json.load(archivo_tomadores)
            print(f"{len(listaTomadores)} Tomadores cargados correctamente")
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
        tomador_id = input("Introduce el DNI, NIE o CIF del tomador: ").upper()
        if tomador_id == "":
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
            continue
        # Comprobamos si el tomador ya existe cuando estamos creando
        elif tomador_id in [tomador["id_tomador"] for tomador in listaTomadores] and not modificando:
            print("El tomador ya existe")
        # Comprobamos si el tomador no existe cuando estamos modificando
        elif tomador_id not in [tomador["id_tomador"] for tomador in listaTomadores] and modificando:
            print("El tomador no existe")
        elif Utilidades.comprobar_dni(tomador_id)[0]:
            return tomador_id
        else:
            print("DNI, NIE o CIF incorrecto")

def configurar_descripcion(tomador_eleccion:dict = {}) -> str:
    """Pide la descripción de un tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce la descripción del tomador: ")
        if not entrada and tomador_eleccion:
            return tomador_eleccion["denominacion"]
        if entrada:
            return entrada

def configurar_fecha_nacimiento(tomador_id:str,tomador_eleccion:dict = {}) -> str:
    """Pide la fecha de nacimiento en caso de ser una persona física y devuelve el valor introducido"""
    # Comprobamos que sea DNI o NIE
    if Utilidades.comprobar_dni(tomador_id)[1]:
        while True:
            fecha = input("Introduce la fecha de nacimiento del tomador dd/mm/aaaa: ")
            if not fecha and tomador_eleccion:
                return tomador_eleccion["fecha_nacimiento"]
            fecha = Utilidades.validar_fecha(fecha)
            if fecha:
                return fecha
    # Si es CIF no pedimos data y dejamos vacío
    else:
        return ""

def configurar_domicilio(tomador_eleccion:dict = {}) -> str:
    """Pide la dirección del tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce la dirección del tomador: ")
        if not entrada and tomador_eleccion:
            return tomador_eleccion["domicilio"]
        if entrada:
            return entrada

def configurar_movil_contacto(tomador_eleccion:dict = {}) -> str:
    """Pide el teléfono del tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce el teléfono del tomador: ")
        if not entrada and tomador_eleccion:
            return tomador_eleccion["movil_contacto"]
        if Utilidades.validar_telefono(entrada):
            return entrada

def configurar_email_contacto(tomador_eleccion:dict = {}) -> str:
    """ Pide el email del tomador y devuelve el valor introducido"""
    while True:
        entrada = input("Introduce el email del tomador: ")
        if not entrada and tomador_eleccion:
            return tomador_eleccion["email_contacto"]
        if Utilidades.validar_email(entrada):
            return entrada

listaTomadores = list()
