import Polizas
import Utilidades
import json

def mostrar_menu_siniestros() -> None:
    """Menu de siniestros, permite crear, modificar o eliminar un siniestro"""
    opcion_siniestros = "0"
    while (opcion_siniestros != "9"):
        Utilidades.limpiar_pantalla()
        print("1. Crear siniestro")
        print("2. Modificar siniestro")
        print("3. Eliminar siniestro")
        print("9. Volver")
        opcion_siniestros = input("Introduce una opción: ")
        match opcion_siniestros:
            case "1":
                mostrar_menu_crear_siniestro()
            case "2":
                mostrar_menu_modificar_siniestro()
            case "3":
                mostrar_menu_eliminar_siniestro()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")

def mostrar_menu_crear_siniestro() -> None:
    """Pide los datos para un nuevo siniestro y lo añade a la lista de siniestros"""
    global listaSiniestros
    print("Creando siniestro")
    fecha_siniestro = configurar_fecha_siniestro()
    if fecha_siniestro == "":
        return
    nro_siniestro = generar_nro_siniestro(fecha_siniestro)
    nro_poliza = configurar_poliza_siniestro()
    if nro_poliza == "":
        return
    descripcion = configurar_desc_siniestro()
    matricula_contrario = configurar_matricula_contrario()
    if matricula_contrario == "":
        return
    compañia_contrario = configurar_compañia_contrario()
    nro_poliza_contrario = configurar_nro_poliza_contrario()
    importe_pagar = configurar_importe_pagar()
    estado_siniestro = configurar_estado_siniestro()
    fecha_abono = configurar_fecha_abono()
    estado_liquidacion = "Pendiente"
    fecha_liquidacion = ""
    siniestro = {"nro_siniestro":nro_siniestro, "nro_poliza":nro_poliza, "descripcion":descripcion, "matricula_contrario":matricula_contrario, "compañia_contrario":compañia_contrario, "nro_poliza_contrario":nro_poliza_contrario, "importe_pagar":importe_pagar, "estado_siniestro":estado_siniestro, "fecha_abono":fecha_abono, "estado_liquidacion":estado_liquidacion, "fecha_liquidacion":fecha_liquidacion}
    crear_siniestro(siniestro)

def crear_siniestro(siniestro:dict) -> None:
    while True:
        Utilidades.limpiar_pantalla()
        listar_siniestro(siniestro, True)
        confirmacion = input("¿Estás seguro de que quieres crear el siniestro? (s/n): ").lower()
        if confirmacion == "s":
            listaSiniestros.append(siniestro)
            ultimos_siniestros[siniestro["nro_siniestro"].split("-")[0]] = int(siniestro["nro_siniestro"].split("-")[1])
            guardar_siniestros()
            input("Siniestro creado. <Enter> para continuar")
            break
        elif confirmacion == "n":
            print("Siniestro no creado")
            break



def mostrar_menu_modificar_siniestro() -> None:
    """Selecciona un siniestro valido, y entra en un menú"""
    global listaSiniestros
    Utilidades.limpiar_pantalla()
    listar_siniestros()
    modificar_siniestro = seleccionar_siniestro()
    if not modificar_siniestro:
        return

    while True:
        Utilidades.limpiar_pantalla()
        listar_siniestro(modificar_siniestro)
        opcion_modificar = input("Introduce una opción: ")
        match opcion_modificar:
            case "1":
                poliza = configurar_poliza_siniestro(modificar_siniestro)
                if poliza != "":
                    modificar_siniestro["nro_poliza"] = poliza
            case "2":
                modificar_siniestro["descripcion"] = configurar_desc_siniestro(modificar_siniestro)
            case "3":
                modificar_siniestro["matricula_contrario"] = configurar_matricula_contrario(modificar_siniestro)
            case "4":
                modificar_siniestro["compañia_contrario"] = configurar_compañia_contrario(modificar_siniestro)
            case "5":
                modificar_siniestro["nro_poliza_contrario"] = configurar_nro_poliza_contrario(modificar_siniestro)
            case "6":
                modificar_siniestro["importe_pagar"] = configurar_importe_pagar(modificar_siniestro)
            case "7":
                modificar_siniestro["estado_siniestro"] = configurar_estado_siniestro(modificar_siniestro)
            case "8":
                modificar_siniestro["fecha_abono"] = configurar_fecha_abono(modificar_siniestro)
            case "9":
                print("Volviendo al menú de siniestros")
                break
            case _:
                print("Opción incorrecta")
    guardar_siniestros()

def mostrar_menu_eliminar_siniestro() -> None:
    """Selecciona un siniestro valido y lo elimina de la lista de siniestros si es posible"""
    global listaSiniestros
    listar_siniestros()
    siniestro_eliminar = seleccionar_siniestro()

    if not siniestro_eliminar:
        return
    
    if siniestro_eliminar['estado_siniestro'] == "Pendiente_Confirmar" or siniestro_eliminar['estado_liquidacion'] == "Liquidado":
        confirmacion = input("¿Estás seguro de que quieres eliminar el siniestro? (s/n): ").upper()
        if confirmacion == "S":
            listaSiniestros.remove(siniestro_eliminar)
            guardar_siniestros()
            print("Siniestro eliminado")
        else:
            print("Siniestro no eliminado")
    else:
        print("No se puede eliminar un siniestro confirmado")
    input("Presione <Enter> para continuar")


def listar_siniestros() -> None:
    """Muestra un listado de todos los siniestros"""
    print("Listado de siniestros")
    print(f"{'Nro.Siniestro':<14}{'Nro. Póliza':<15}{'Descripción':<40}{'Mat.Ctrio':<10}")
    for siniestro in listaSiniestros:
        print(f"{siniestro['nro_siniestro']:<14}{siniestro['nro_poliza']:<15}{siniestro['descripcion']:<40}{siniestro['matricula_contrario']:<10}")

def listar_siniestro(siniestro:dict, creando:bool = False) -> None:
    """Muestra los datos de un siniestro"""
    print(f"Modificando Siniestro Número: {siniestro['nro_siniestro']}")
    print(f"1. Nro. Póliza: {siniestro['nro_poliza']}")
    print(f"2. Descripción: {siniestro['descripcion']}")
    print(f"3. Matrícula Contrario: {siniestro['matricula_contrario']}")
    print(f"4. Compañía Contrario: {siniestro['compañia_contrario']}")
    print(f"5. Nro. Póliza Contrario: {siniestro['nro_poliza_contrario']}")
    print(f"6. Importe a Pagar: {siniestro['importe_pagar']}")
    print(f"7. Estado Siniestro: {siniestro['estado_siniestro']}")
    print(f"8. Fecha Abono: {siniestro['fecha_abono']}")
    print(f"-> Estado Liquidación: {siniestro['estado_liquidacion']}")
    print(f"-> Fecha Liquidación: {siniestro['fecha_liquidacion']}")
    if not creando:
        print("9 . Volver")

def generar_nro_siniestro(fecha:str) -> str:
    """Genera un identificador de siniestro único correlativo para un año dado."""
    año_s = fecha.split("/")[2]
    if not ultimos_siniestros.get(año_s):
        ultimos_siniestros[año_s] = 0
    ultimo_siniestro = ultimos_siniestros[año_s] + 1
    return f"{año_s}-{str(ultimo_siniestro).zfill(6)}"

def seleccionar_siniestro() -> dict:
    """Pide los datos de un siniestro y devuelve el siniestro si existe"""
    while True:
        try:
            año_siniestro = input("Introduce el año de siniestro: ")
            if not año_siniestro:
                confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
                if confirmacion == "s":
                    return ""
                continue
            año_siniestro = int(año_siniestro)
        except:
            print("El año debe ser un número")
            continue
        if año_siniestro < Utilidades.AÑO_LIMITE_INFERIOR or año_siniestro > Utilidades.AÑO_LIMITE_SUPERIOR:
            print("El año debe estar entre 1900 y 2100")
            continue
        año_siniestro = str(año_siniestro)
        numero_recibos_año = []
        recibos_año = []
        for siniestro in listaSiniestros:
            if siniestro["nro_siniestro"][:4] == año_siniestro:
                numero_recibos_año.append(siniestro["nro_siniestro"])
                recibos_año.append(siniestro)
        if not numero_recibos_año:
            print("No hay siniestros para ese año")
            continue
        
        while True:
            numero_siniestro = input("Introduce el número de siniestro: ")
            if not numero_siniestro:
                confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
                if confirmacion == "s":
                    return ""
                continue
            try: 
                numero_siniestro = str(int(numero_siniestro)).zfill(6)
            except:
                print("El número de siniestro debe ser un número")
                continue
            if not f"{año_siniestro}-{numero_siniestro}" in numero_recibos_año:
                print("El número de siniestro no existe")
                continue
            for siniestro in recibos_año:
                if siniestro["nro_siniestro"] == f"{año_siniestro}-{numero_siniestro}":
                    return siniestro


def cargar_siniestros() -> None:
    """Carga los siniestros desde el archivo siniestros.json"""
    global listaSiniestros
    global ultimos_siniestros
    try:
        with open("siniestros.json", "r", encoding="utf-8") as archivo_siniestros:
            datos = json.load(archivo_siniestros)
            ultimos_siniestros = datos["ultimos_siniestros"]
            listaSiniestros = datos["listaSiniestros"]
            print(f"{len(listaSiniestros)} Siniestros cargados correctamente")
    except:
        print("No existen datos de siniestros")
        ultimos_siniestros = {}

def guardar_siniestros() -> None:
    """Guarda los siniestros en el archivo siniestros.json"""
    try:
        with open("siniestros.json", "w", encoding="utf-8") as archivo_siniestros:
            json.dump({"ultimos_siniestros":ultimos_siniestros ,"listaSiniestros":listaSiniestros}, archivo_siniestros, ensure_ascii=False, indent=4)
    except:
        print("Error al guardar los siniestros")


def configurar_fecha_siniestro() -> str:
    """Pide la fecha del siniestro y la valida"""
    while True:
        fecha_siniestro = input("Introduce la fecha del siniestro (dd/mm/aaaa): ")
        if not fecha_siniestro:
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
            continue
        fecha_siniestro = Utilidades.validar_fecha(fecha_siniestro)
        if fecha_siniestro:
            return fecha_siniestro
        else:
            print("Fecha incorrecta")
    


def configurar_poliza_siniestro(siniestro_modificar:dict = {}) -> str:
    """Pide el número de póliza del siniestro y lo valida"""
    while True:
        nro_poliza = input("Introduce el número de póliza: ")
        if nro_poliza == "" and siniestro_modificar:
            return siniestro_modificar["nro_poliza"]
        if not nro_poliza:
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
        try:
            nro_poliza = str(int(nro_poliza)).zfill(12)
        except:
            print("El número de póliza debe ser un número")
            continue
        poliza_encontrada = False
        for poliza in Polizas.listaPolizas:
            if poliza["nro_poliza"] == nro_poliza:
                poliza_encontrada = True
                if Polizas.comprobar_vigencia(poliza):
                    return nro_poliza
                else:
                    print("La póliza no está vigente")
                    confirmacion = input("¿Quieres introducir otro número de póliza? (s/n): ").upper()
                    if confirmacion == "N":
                        return ""
                    else:
                        continue
        if not poliza_encontrada:
            print("La póliza no existe")
            confirmacion = input("¿Quieres introducir otro número de póliza? (s/n): ").upper()
            if confirmacion == "N":
                return ""
            else:
                continue
        
def configurar_desc_siniestro(siniestro_modificar:dict = {}) -> str:
    """Pide la descripción del siniestro, valida que no esté vacía y la devuelve"""
    while True:
        descripcion = input("Introduce la descripción del siniestro: ")
        if not descripcion and siniestro_modificar:
            return siniestro_modificar["descripcion"]
        if descripcion:
            return descripcion

def configurar_matricula_contrario(siniestro_modificar:dict = {}) -> str:
    """Pide la matrícula del vehículo contrario, la valida y la devuelve"""
    while True:
        matricula_contrario = input("Introduce la matrícula del vehículo contrario: ")
        if matricula_contrario == "" and siniestro_modificar:
            return siniestro_modificar["matricula_contrario"]
        if matricula_contrario == "":
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
        while True:
            tipos = {"1": "Ciclomotor", "2": "Moto", "3": "Turismo", "4": "Furgoneta", "5": "Camión"}
            for numero, tipo in tipos.items():
                print(f"{numero}. {tipo}")
            entrada = input("Introduce el tipo de vehículo(): ")
            if entrada in ["1", "2", "3", "4", "5"]:
                tipo = tipos[entrada]
                break
        if Utilidades.validar_matricula(matricula_contrario, tipo):
            return matricula_contrario

def configurar_compañia_contrario(siniestro_modificar:dict = {}) -> str:
    """Pide la compañía del vehículo contrario, la valida y la devuelve"""
    while True:
        compañia_contrario = input("Introduce la compañía del vehículo contrario: ")
        if compañia_contrario == "" and siniestro_modificar:
            return siniestro_modificar["compañia_contrario"]
        if compañia_contrario:
            return compañia_contrario

def configurar_nro_poliza_contrario(siniestro_modificar:dict = {}) -> str:
    """Pide el número de póliza del vehículo contrario, lo valida y lo devuelve"""
    while True:
        nro_poliza_contrario = input("Introduce el número de póliza del vehículo contrario: ")
        if nro_poliza_contrario == "" and siniestro_modificar:
            return siniestro_modificar["nro_poliza_contrario"]
        if nro_poliza_contrario:
            return nro_poliza_contrario

def configurar_importe_pagar(siniestro_modificar:dict = {}) -> float:
    """Pide el importe a pagar, lo valida y lo devuelve"""
    while True:
        importe_pagar = input("Introduce el importe a pagar: ")
        if importe_pagar == "" and siniestro_modificar:
            return siniestro_modificar["importe_pagar"]
        try:
            importe_pagar = float(importe_pagar)
            importe_pagar = round(importe_pagar, 2)
            return importe_pagar
        except ValueError:
            print("El importe debe ser un número")

def configurar_estado_siniestro(siniestro_modificar:dict = {}) -> str:
    """Pide el estado del siniestro, lo valida y lo devuelve"""
    while True:
        estado_siniestro = input("Introduce el estado del siniestro (PC)Pendiente Confirmar,(C)Confirmado, (PP)Pendiente Pago ó (P)Pagado: ").upper()
        if estado_siniestro == "" and siniestro_modificar:
            return siniestro_modificar["estado_siniestro"]
        if estado_siniestro in ["PC", "C", "PP", "P", "PENDIENTE CONFIRMAR", "CONFIRMADO", "PENDIENTE PAGO", "PAGADO"]:
            if estado_siniestro in ["PC", "PENDIENTE CONFIRMAR"]:
                estado_siniestro = "Pendiente_Confirmar"
            elif estado_siniestro in ["C", "CONFIRMADO"]:
                estado_siniestro = "Confirmado"
            elif estado_siniestro in ["PP", "PENDIENTE PAGO"]:
                estado_siniestro = "Pendiente_Pago"
            elif estado_siniestro in ["P", "PAGADO"]:
                estado_siniestro = "Pagado"
            return estado_siniestro

def configurar_fecha_abono(siniestro_modificar:dict = {}) -> str:
    """Pide la fecha de abono del siniestro, la valida y la devuelve"""
    while True:
        fecha_abono = input("Introduce la fecha de abono del siniestro (dd/mm/aaaa): ")
        if fecha_abono == "" and siniestro_modificar:
            return siniestro_modificar["fecha_abono"]
        if Utilidades.validar_fecha(fecha_abono):
            return fecha_abono

listaSiniestros = list()
