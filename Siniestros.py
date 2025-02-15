import Polizas
import Utilidades
import json

def menu_siniestros() -> None:
    """Menu de siniestros, permite crear, modificar o eliminar un siniestro"""
    opcion_siniestros = "0"
    while (opcion_siniestros != "9"):
        print("1. Crear siniestro")
        print("2. Modificar siniestro")
        print("3. Eliminar siniestro")
        print("9. Volver")
        opcion_siniestros = input("Introduce una opción: ")
        match opcion_siniestros:
            case "1":
                crear_siniestro()
            case "2":
                modificar_siniestro()
            case "3":
                eliminar_siniestro()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")

def crear_siniestro() -> None:
    """Pide los datos para un nuevo siniestro y lo añade a la lista de siniestros"""
    global listaSiniestros
    print("Creando siniestro")
    fecha_siniestro = configurar_fecha_siniestro()
    nro_siniestro = generar_nro_siniestro(fecha_siniestro)
    nro_poliza = configurar_poliza_siniestro(fecha_siniestro)
    if nro_poliza == "Caducada":
        print("Poliza no vigente. Volviendo al menú")
        return
    elif nro_poliza == "":
        print("Poliza no encontrada. Volviendo al menú")
        return
    descripcion = configurar_desc_siniestro()
    matricula_contrario = configurar_matricula_contrario()
    compañia_contrario = configurar_compañia_contrario()
    nro_poliza_contrario = configurar_nro_poliza_contrario()
    importe_pagar = configurar_importe_pagar()
    estado_siniestro = configurar_estado_siniestro()
    fecha_abono = configurar_fecha_abono()
    estado_liquidacion = configurar_estado_liquidacion()
    fecha_liquidacion = configurar_fecha_liquidacion(estado_liquidacion)

    listaSiniestros.append({"nro_siniestro":nro_siniestro, "nro_poliza":nro_poliza, "descripcion":descripcion, "matricula_contrario":matricula_contrario, "compañia_contrario":compañia_contrario, "nro_poliza_contrario":nro_poliza_contrario, "importe_pagar":importe_pagar, "estado_siniestro":estado_siniestro, "fecha_abono":fecha_abono, "estado_liquidacion":estado_liquidacion, "fecha_liquidacion":fecha_liquidacion})
    guardar_siniestros()



def modificar_siniestro() -> None:
    """Selecciona un siniestro valido, y entra en un menú"""
    global listaSiniestros
    listar_siniestros()
    modificar_siniestro = seleccionar_siniestro()

    while True:
        listar_siniestro(modificar_siniestro)
        opcion_modificar = input("Introduce una opción: ")
        match opcion_modificar:
            case "1":
                modificar_siniestro["nro_poliza"] = configurar_poliza_siniestro(modificar_siniestro["fecha_abono"])
            case "2":
                modificar_siniestro["descripcion"] = configurar_desc_siniestro()
            case "3":
                modificar_siniestro["matricula_contrario"] = configurar_matricula_contrario()
            case "4":
                modificar_siniestro["compañia_contrario"] = configurar_compañia_contrario()
            case "5":
                modificar_siniestro["nro_poliza_contrario"] = configurar_nro_poliza_contrario()
            case "6":
                modificar_siniestro["importe_pagar"] = configurar_importe_pagar()
            case "7":
                modificar_siniestro["estado_siniestro"] = configurar_estado_siniestro()
            case "8":
                modificar_siniestro["fecha_abono"] = configurar_fecha_abono()
            case "9":
                modificar_siniestro["estado_liquidacion"] = configurar_estado_liquidacion()
            case "10":
                modificar_siniestro["fecha_liquidacion"] = configurar_fecha_liquidacion(modificar_siniestro["estado_liquidacion"])
            case "0":
                print("Volviendo al menú de siniestros")
                break
            case _:
                print("Opción incorrecta")
    guardar_siniestros()

def eliminar_siniestro() -> None:
    """Selecciona un siniestro valido y lo elimina de la lista de siniestros si es posible"""
    global listaSiniestros
    listar_siniestros()
    siniestro_eliminar = seleccionar_siniestro()

    if not siniestro_eliminar:
        return
    
    if siniestro_eliminar['estado_siniestro'] == "Pendiente_Confirmar":
        confirmacion = input("¿Estás seguro de que quieres eliminar el siniestro? (s/n): ").upper()
        if confirmacion == "S":
            listaSiniestros.remove(siniestro_eliminar)
            guardar_siniestros()
            print("Siniestro eliminado")
        else:
            print("Siniestro no eliminado")
    else:
        print("No se puede eliminar un siniestro confirmado")


def listar_siniestros() -> None:
    """Muestra un listado de todos los siniestros"""
    print("Listado de siniestros")
    print(f"{'Nro.Siniestro':<13}{'Nro. Póliza':<15}{'Descripción':<30}{'Mat.Ctrio':<10}{'Cmpñía.Ctrrio':<13}{'Nro. Póliza Contrario':<15}{'Importe a Pagar':<10}{'Estado Siniestro':<12}{'Fecha Abono':<15}{'Estado Liquidación':<15}{'Fecha Liquidación':<15}")
    for siniestro in listaSiniestros:
        print(f"{siniestro['nro_siniestro']:<13}{siniestro['nro_poliza']:<15}{siniestro['descripcion']:<30}{siniestro['matricula_contrario']:<10}{siniestro['compañia_contrario']:<13}{siniestro['nro_poliza_contrario']:<15}{siniestro['importe_pagar']:<10}{siniestro['estado_siniestro']:<12}{siniestro['fecha_abono']:<15}{siniestro['estado_liquidacion']:<15}{siniestro['fecha_liquidacion']:<15}")

def listar_siniestro(siniestro:dict) -> None:
    """Muestra los datos de un siniestro"""
    print(f"Modificando Siniestro Número: {siniestro['nro_siniestro']}")
    print(f" 1. Nro. Póliza: {siniestro['nro_poliza']}")
    print(f" 2. Descripción: {siniestro['descripcion']}")
    print(f" 3. Matrícula Contrario: {siniestro['matricula_contrario']}")
    print(f" 4. Compañía Contrario: {siniestro['compañia_contrario']}")
    print(f" 5. Nro. Póliza Contrario: {siniestro['nro_poliza_contrario']}")
    print(f" 6. Importe a Pagar: {siniestro['importe_pagar']}")
    print(f" 7. Estado Siniestro: {siniestro['estado_siniestro']}")
    print(f" 8. Fecha Abono: {siniestro['fecha_abono']}")
    print(f" 9. Estado Liquidación: {siniestro['estado_liquidacion']}")
    print(f"10. Fecha Liquidación: {siniestro['fecha_liquidacion']}")
    print(" 0 . Volver")

def generar_nro_siniestro(fecha:str) -> str:
    """Genera un identificador de siniestro único correlativo para un año dado."""
    año_s = fecha.split("/")[2]
    siniestro_año = []
    for siniestro in listaSiniestros:
        if siniestro["nro_siniestro"].split("-")[0] == año_s:
            siniestro_año.append(int(siniestro["nro_siniestro"].split("-")[1]))
    if siniestro_año:
        ultimo_siniestro = max(siniestro_año) + 1
    else:
        ultimo_siniestro = 0
    return f"{año_s}-{str(ultimo_siniestro).zfill(6)}"

def seleccionar_siniestro() -> dict:
    """Pide los datos de un siniestro y devuelve el siniestro si existe"""
    while True:
        try:
            año_siniestro = input("Introduce el año de siniestro: ")
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
    try:
        with open("siniestros.json", "r", encoding="utf-8") as archivo_siniestros:
            listaSiniestros = json.load(archivo_siniestros)
    except:
        print("Error al cargar los siniestros")

def guardar_siniestros() -> None:
    """Guarda los siniestros en el archivo siniestros.json"""
    try:
        with open("siniestros.json", "w", encoding="utf-8") as archivo_siniestros:
            json.dump(listaSiniestros, archivo_siniestros, ensure_ascii=False, indent=4)
    except:
        print("Error al guardar los siniestros")


def configurar_fecha_siniestro() -> str:
    """Pide la fecha del siniestro y la valida"""
    while True:
        fecha_siniestro = input("Introduce la fecha del siniestro (dd/mm/aaaa): ")
        fecha_siniestro = Utilidades.validar_fecha(fecha_siniestro)
        if fecha_siniestro:
            dia_s, mes_s, año_s = fecha_siniestro.split("/")
            return fecha_siniestro
        else:
            print("Fecha incorrecta")
    


def configurar_poliza_siniestro(fecha:str) -> str:
    """Pide el número de póliza del siniestro y lo valida"""
    dia_s, mes_s, año_s = fecha.split("/")
    while True:
        nro_poliza = input("Introduce el número de póliza: ")
        try:
            nro_poliza = str(int(nro_poliza)).zfill(12)
        except:
            print("El número de póliza debe ser un número")
            continue
        poliza_encontrada = False
        for poliza in Polizas.listaPolizas:
            if poliza["nro_poliza"] == nro_poliza:
                poliza_encontrada = True
                if poliza["estado_poliza"] == "Cobrada":
                    fecha_emision = poliza["fecha_emision"].split("/")
                    if int(año_s) <= int(fecha_emision[2]) and int(mes_s) <= int(fecha_emision[1]) and int(dia_s) <= int(fecha_emision[0]):
                        print("La póliza está caducada")
                    else:
                        return nro_poliza
                else:
                    print("La póliza no está activa")
                    confirmacion = input("¿Quieres introducir otro número de póliza? (s/n): ").upper()
                    if confirmacion == "N":
                        return "Caducada"
                    else:
                        continue
        if not poliza_encontrada:
            print("La póliza no existe")
            confirmacion = input("¿Quieres introducir otro número de póliza? (s/n): ").upper()
            if confirmacion == "N":
                return ""
            else:
                continue
        
def configurar_desc_siniestro() -> str:
    """Pide la descripción del siniestro, valida que no esté vacía y la devuelve"""
    while True:
        descripcion = input("Introduce la descripción del siniestro: ")
        if descripcion:
            return descripcion

def configurar_matricula_contrario() -> str:
    """Pide la matrícula del vehículo contrario, la valida y la devuelve"""
    while True:
        matricula_contrario = input("Introduce la matrícula del vehículo contrario: ")
        if Utilidades.validar_matricula(matricula_contrario):
            return matricula_contrario

def configurar_compañia_contrario() -> str:
    """Pide la compañía del vehículo contrario, la valida y la devuelve"""
    while True:
        compañia_contrario = input("Introduce la compañía del vehículo contrario: ")
        if compañia_contrario:
            return compañia_contrario

def configurar_nro_poliza_contrario() -> str:
    """Pide el número de póliza del vehículo contrario, lo valida y lo devuelve"""
    while True:
        nro_poliza_contrario = input("Introduce el número de póliza del vehículo contrario: ")
        if nro_poliza_contrario:
            return nro_poliza_contrario

def configurar_importe_pagar() -> float:
    """Pide el importe a pagar, lo valida y lo devuelve"""
    while True:
        importe_pagar = input("Introduce el importe a pagar: ")
        try:
            importe_pagar = float(importe_pagar)
            importe_pagar = round(importe_pagar, 2)
            return importe_pagar
        except ValueError:
            print("El importe debe ser un número")

def configurar_estado_siniestro() -> str:
    """Pide el estado del siniestro, lo valida y lo devuelve"""
    while True:
        estado_siniestro = input("Introduce el estado del siniestro (PC)Pendiente Confirmar,(C)Confirmado, (PP)Pendiente Pago ó (P)Pagado: ").upper()
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

def configurar_fecha_abono() -> str:
    """Pide la fecha de abono del siniestro, la valida y la devuelve"""
    while True:
        fecha_abono = input("Introduce la fecha de abono del siniestro (dd/mm/aaaa): ")
        if Utilidades.validar_fecha(fecha_abono):
            return fecha_abono

def configurar_estado_liquidacion() -> str:
    """Pide el estado de la liquidación, lo valida y lo devuelve"""
    while True:
        estado_liquidacion = input("Introduce el estado de la liquidación (P)Pendiente o (L)Liquidado: ").upper()
        if estado_liquidacion in ["P", "L", "PENDIENTE", "LIQUIDADO"]:
            if estado_liquidacion in ["P", "PENDIENTE"]:
                estado_liquidacion = "Pendiente"
            elif estado_liquidacion in ["L", "LIQUIDADO"]:
                estado_liquidacion = "Liquidado"
            return estado_liquidacion
        else:
            print("Opción incorrecta")

def configurar_fecha_liquidacion(estado_liquidacion:str) -> str:
    """Pide la fecha de liquidación del siniestro, la valida y la devuelve"""
    if estado_liquidacion == "Liquidado":
        while True:
            fecha_liquidacion = input("Introduce la fecha de liquidación del siniestro (dd/mm/aaaa): ")
            if Utilidades.validar_fecha(fecha_liquidacion):
                return fecha_liquidacion
    else:
        return ""
    

listaSiniestros = list()