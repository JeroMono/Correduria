import Utilidades
import Recibos
import Siniestros
import json

def menu_liquidaciones() -> None:
    """Menú de liquidaciones, permite crear, modificar y cerrar liquidaciones"""
    opcion_liquidaciones = "0"
    while (opcion_liquidaciones != "9"):
        print("1. Crear liquidación")
        print("2. Modificar liquidación")
        print("3. Eliminar liquidación")
        print("9. Volver")
        opcion_liquidaciones = input("Introduce una opción: ")
        match opcion_liquidaciones:
            case "1":
                crear_liquidacion()
            case "2":
                modificar_liquidacion()
            case "3":
                cerrar_liquidacion()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")

def crear_liquidacion() -> None:
    """Entra en el menu de creación de liquidaciones, solicita los datos necesarios y crea una liquidación"""
    global listaLiquidaciones
    print("Creando liquidación")
    
    fecha_liquidacion = configurar_fecha_liquidacion()

    nro_liquidacion = generar_nro_liquidacion(fecha_liquidacion)
    
    estado_liquidacion = "Abierta"

    importe_recibos_cobrados, lista_recibos_liquidar = calcular_recibos_cobrados(fecha_liquidacion)

    importe_recibos_baja, lista_recibos_baja = calcular_recibos_baja(fecha_liquidacion)

    importe_siniestros_pagados, lista_siniestros_liquidados = calcular_siniestros_pagados(fecha_liquidacion)

    importe_liquidacion = (importe_recibos_cobrados - importe_siniestros_pagados, importe_recibos_baja)

    listaLiquidaciones.append({"nro_liquidacion":nro_liquidacion, "fecha_liquidacion":fecha_liquidacion, "estado_liquidacion":estado_liquidacion, "importe_recibos_cobrados":importe_recibos_cobrados, "lista_recibos_liquidar":lista_recibos_liquidar, "importe_recibos_baja":importe_recibos_baja, "lista_recibos_baja":lista_recibos_baja, "importe_siniestros_pagados":importe_siniestros_pagados, "lista_siniestros_liquidados":lista_siniestros_liquidados, "importe_liquidacion":importe_liquidacion})
    guardar_liquidaciones()
    

def modificar_liquidacion() -> None:
    """Modifica una liquidación existente, permite cambiar la fecha de la liquidación y recalcula los importes de la liquidación"""
    global listaLiquidaciones
    listar_liquidaciones()
    liquidacion_modificar = seleccionar_liquidacion()

    if not liquidacion_modificar:
        return
    
    fecha_liquidacion = configurar_fecha_liquidacion()




def cerrar_liquidacion() -> None:
    """Cierra una liquidación y liquida los recibos y siniestros pendientes"""
    global listaLiquidaciones
    listar_liquidaciones()
    liquidacion_cerrar = seleccionar_liquidacion()

    if not liquidacion_cerrar:
        return
    
    if liquidacion_cerrar["estado_liquidacion"] == "Cerrada":
        print("La liquidación ya está cerrada")
        return
    
    liquidacion_cerrar["estado_liquidacion"] = "Cerrada"

    for recibos in liquidacion_cerrar["lista_recibos_liquidar"]:
        if recibos["estado_liquidacion"] == "Pendiente":
            recibos["estado_liquidacion"] = "Liquidado"
            recibos["fecha_liquidacion"] = liquidacion_cerrar["fecha_liquidacion"]
            print("Liquidado recibo", recibos["id_recibo"])
    
    for recibos in liquidacion_cerrar["lista_recibos_baja"]:
        if recibos["estado_liquidacion"] == "Pendiente":
            recibos["estado_liquidacion"] = "Liquidado"
            recibos["fecha_liquidacion"] = liquidacion_cerrar["fecha_liquidacion"]
            print("Liquidado recibo", recibos["id_recibo"])

    for siniestros in liquidacion_cerrar["lista_siniestros_liquidados"]:
        if siniestros["estado_liquidacion"] == "Pendiente":
            siniestros["estado_liquidacion"] = "Liquidado"
            siniestros["fecha_liquidacion"] = liquidacion_cerrar["fecha_liquidacion"]
            print("Liquidado siniestro", siniestros["nro_siniestro"])


    guardar_liquidaciones()
    Recibos.guardar_recibos()
    Siniestros.guardar_siniestros()




def listar_liquidaciones() -> None:
    """Muestra un listado de las liquidaciones existentes"""
    print("Listado de liquidaciones")
    print(listaLiquidaciones)
    for liquidacion in listaLiquidaciones:
        print(f"Nro Liquidación:{liquidacion['nro_liquidacion']}, Fecha Liquidación:{liquidacion['fecha_liquidacion']}, Estado Liquidación:{liquidacion['estado_liquidacion']}")    

def generar_nro_liquidacion(fecha:str) -> str:
    """Genera un identificador de liquidaciones único correlativo para un año dado"""
    año = fecha.split("/")[2]
    liquidaciones_año = []
    for liquidacion in listaLiquidaciones:
        if liquidacion["nro_liquidacion"][:4] == str(año):
            liquidaciones_año.append(int(liquidacion["nro_liquidacion"][5:]))
    if liquidaciones_año:
        nro_liquidacion = max(liquidaciones_año) + 1
    else:
        nro_liquidacion = 0
    return f"{año}-{nro_liquidacion:06}"

def seleccionar_liquidacion() -> dict:
    """Devuelve una liquidación de la lista de liquidaciones"""
    while True:
        try:
            año_liquidacion = input("Introduce el año de la liquidación: ")
            año_liquidacion = int(año_liquidacion)
        except:
            print("Año no válido")
            continue
        if año_liquidacion < Utilidades.AÑO_LIMITE_INFERIOR or año_liquidacion > Utilidades.AÑO_LIMITE_SUPERIOR:
            print("Año no válido")
            continue
        año_liquidacion = str(año_liquidacion)
        numeros_liquidacion_año = []
        liquidaciones_año = []
        for liquidacion in listaLiquidaciones:
            if liquidacion["nro_liquidacion"][:4] == año_liquidacion:
                numeros_liquidacion_año.append(liquidacion["nro_liquidacion"])
                liquidaciones_año.append(liquidacion)
        if not liquidaciones_año:
            print("No hay liquidaciones para ese año")
            continue

        while True:
            numero_liquidacion = input("Introduce el número de la liquidación: ")
            try:
                numero_liquidacion = str(int(numero_liquidacion))
            except:
                print("Número no válido")
                continue
            if not f"{año_liquidacion}-{numero_liquidacion:06}" in numeros_liquidacion_año:
                print("El numero de liquidación no existe")
                continue
            for liquidacion in liquidaciones_año:
                if liquidacion["nro_liquidacion"] == f"{año_liquidacion}-{numero_liquidacion:06}":
                    return liquidacion




def cargar_liquidaciones() -> None:
    """Carga las liquidaciones desde el archivo Liquidaciones.json"""
    global listaLiquidaciones
    try:
        with open("Liquidaciones.json", "r") as f:
            lista_liquidaciones = json.load(f)
            # Convert lists back to tuples
            for liquidacion in lista_liquidaciones:
                liquidacion["lista_recibos_liquidar"] = tuple(liquidacion["lista_recibos_liquidar"])
                liquidacion["lista_recibos_baja"] = tuple(liquidacion["lista_recibos_baja"])
                liquidacion["lista_siniestros_liquidados"] = tuple(liquidacion["lista_siniestros_liquidados"])
                liquidacion["importe_liquidacion"] = tuple(liquidacion["importe_liquidacion"])
            listaLiquidaciones = lista_liquidaciones
    except:
        print("No se ha encontrado el archivo Liquidaciones.json")
    
def guardar_liquidaciones() -> None:
    """"Guarda las liquidaciones en el archivo Liquidaciones.json"""
    try:
        with open("Liquidaciones.json", "w", encoding = "utf-8") as archivo_liquidaciones:
            json.dump(listaLiquidaciones, archivo_liquidaciones, indent=4)
    except:
        print("Error al guardar las liquidaciones")

def configurar_fecha_liquidacion() -> str:
    """Solicita una fecha al usuario, la valida y la retorna en formato dd/mm/aaaa"""
    while True:
        fecha_liquidacion = input("Introduce la fecha de la liquidación (dd/mm/aaaa): ")
        fecha_liquidacion = Utilidades.validar_fecha(fecha_liquidacion)
        if fecha_liquidacion:
            return fecha_liquidacion
        else:
            print("Fecha no válida")

def configurar_estado_liquidacion() -> str:
    """Permite cambiar manualmente el estado de la liquidación"""
    while True:
        estado_liquidacion = input("Introduce el estado de la liquidación (A)bierta o (C)errada: ").upper()
        if estado_liquidacion in ["A", "C", "ABIERTA", "CERRADA"]:
            if estado_liquidacion in ["A", "ABIERTA"]:
                estado_liquidacion = "Abierta"
            elif estado_liquidacion in ["C", "CERRADA"]:
                estado_liquidacion = "Cerrada"
            break
    
    estado_liquidacion = "Abierta"

def calcular_recibos_cobrados(fecha_liquidacion:str) -> tuple:
    """Calcula el importe de los recibos cobrados hasta la fecha de liquidación y los devuelve con la lista de los recibos a liquidar"""
    importe_recibos_cobrados = 0.0
    lista_recibos_liquidar = []
    fecha_liquidacion = fecha_liquidacion.split("/")
    for recibo in Recibos.listaRecibos:
        if (recibo["estado_recibo"] in ["Cobrado", "Cobrado_Banco"]) and recibo["estado_liquidacion"] == "Pendiente":
            fecha_cobro = recibo["fecha_cobro"].split("/")
            if fecha_cobro[0]<= fecha_liquidacion[0] and fecha_cobro[1]<= fecha_liquidacion[1] and fecha_cobro[2]<= fecha_liquidacion[2]:
                importe_recibos_cobrados += recibo["importe_cobrar"]
                lista_recibos_liquidar.append((recibo["nro_poliza"],recibo["id_recibo"]))
    return importe_recibos_cobrados, lista_recibos_liquidar

def calcular_recibos_baja(fecha_liquidacion:str) -> tuple:
    """Calcula el importe de los recibos dados de baja hasta la fecha de liquidación y los devuelve con la lista de los recibos a liquidar"""
    importe_recibos_baja = 0.0
    lista_recibos_baja = []
    fecha_liquidacion = fecha_liquidacion.split("/")
    for recibo in Recibos.listaRecibos:
        if recibo["estado_recibo"] == "Baja":
            fecha_cobro = recibo["fecha_cobro"].split("/")
            if fecha_cobro[0]<= fecha_liquidacion[0] and fecha_cobro[1]<= fecha_liquidacion[1] and fecha_cobro[2]<= fecha_liquidacion[2]:
                importe_recibos_baja += recibo["importe_cobrar"]
                lista_recibos_baja.append((recibo["nro_poliza"],recibo["id_recibo"]))
    return importe_recibos_baja, lista_recibos_baja

def calcular_siniestros_pagados(fecha_liquidacion:str) -> tuple:
    """Calcula el importe de los siniestros pagados hasta la fecha de liquidación y los devuelve con la lista de los siniestros a liquidar"""
    importe_siniestros_pagados = 0.0
    lista_siniestros_liquidados = []
    fecha_liquidacion = fecha_liquidacion.split("/")
    for siniestro in Siniestros.listaSiniestros:
        if siniestro["estado_siniestro"] == "Pagado" and siniestro["estado_liquidacion"] == "Pendiente":
            fecha_abono = siniestro["fecha_abono"].split("/")
            if fecha_abono[0]<= fecha_liquidacion[0] and fecha_abono[1]<= fecha_liquidacion[1] and fecha_abono[2]<= fecha_liquidacion[2]:
                importe_siniestros_pagados += siniestro["importe_pagar"]
                lista_siniestros_liquidados.append((siniestro["nro_poliza"],siniestro["nro_siniestro"]))
    return importe_siniestros_pagados, lista_siniestros_liquidados

listaLiquidaciones = []
