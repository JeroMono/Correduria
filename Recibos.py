import Polizas
import Utilidades
import json

def mostrar_menu_recibos() -> None:
    """Menu de recibos, permite crear, modificar y eliminar recibos"""
    opcion_recibos = 0
    while (opcion_recibos != "9"):
        Utilidades.limpiar_pantalla()
        print("1. Crear recibo")
        print("2. Modificar recibo")
        print("3. Eliminar recibo")
        print("9. Volver")
        opcion_recibos = input("Introduce una opción: ")
        match opcion_recibos:
            case "1":
                mostrar_menu_crear_recibo()
            case "2":
                mostrar_menu_modificar_recibo()
            case "3":
                mostrar_menu_eliminar_recibo()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")

def mostrar_menu_crear_recibo() -> None:
    """ Pide la información necesaria para crear un recibo, la valida y lo añade a la lista de recibos"""
    global ultimo_recibo
    global listaRecibos
    Utilidades.limpiar_pantalla()
    id_recibo = generar_id_recibo()
    nro_poliza = configurar_nro_poliza()
    if nro_poliza == "":
        return

    fecha_inicio = configurar_fecha_inicio()
    duracion = configurar_duracion()
    importe_cobrar = configurar_importe_cobrar()
    fecha_cobro = configurar_fecha_cobro()
    estado_recibo = configurar_estado_recibo(nro_poliza, duracion, fecha_inicio)
    importe_pagar = configurar_importe_pagar()
    estado_liquidacion = "Pendiente"
    fecha_liquidacion = ""

    recibo = {"id_recibo":id_recibo,"nro_poliza":nro_poliza, "fecha_inicio":fecha_inicio, "duracion":duracion, "importe_cobrar":importe_cobrar, "fecha_cobro":fecha_cobro, "estado_recibo":estado_recibo, "importe_pagar":importe_pagar, "estado_liquidacion":estado_liquidacion, "fecha_liquidacion":fecha_liquidacion}
    
    while True:
        listar_recibo(recibo, True)
        confirmacion = input("¿Estás seguro de que quieres crear el recibo? (s/n): ")
        if confirmacion == "s":
            listaRecibos.append(recibo)
            ultimo_recibo = int(id_recibo)
            guardar_recibos()
            print("Recibo creado")
            for poliza in Polizas.listaPolizas:
                if poliza['nro_poliza'] == nro_poliza:
                    if Polizas.comprobar_vigencia(poliza):
                        poliza['estado_poliza'] = "Cobrada"
                        print(f"Vigente de la poliza {nro_poliza} actualizada, ahora está vigente")
                        Polizas.guardar_polizas()
                        break
            input("Pulse <Enter> para continuar")
            break
        elif confirmacion == "n":
            print("Operación cancelada")
            input("Pulse <Enter> para continuar")
            break


def guardar_recibos() -> None:
    """Guarda la lista de recibos en un archivo json"""
    try:
        with open("recibos.json", "w", encoding='utf-8') as archivo_recibos:
            json.dump({"ultimo_recibo":ultimo_recibo,"recibos":listaRecibos}, archivo_recibos, ensure_ascii=False, indent=4)
    except:
        print("Error al guardar los recibos")

def cargar_recibos() -> None:
    """Carga la lista de recibos desde un archivo json"""
    global listaRecibos
    global ultimo_recibo
    try:
        with open("recibos.json", "r", encoding='utf-8') as archivo_recibos:
            data = json.load(archivo_recibos)
            ultimo_recibo = data["ultimo_recibo"]
            listaRecibos = data["recibos"]
            print(f"{len(listaRecibos)} Recibos cargados")
    except:
        print("No existen recibos guardados")


def mostrar_menu_modificar_recibo() -> None:
    """Selecciona y entra en un menú para modificar los valores seleccionados"""
    global listaRecibos
    Utilidades.limpiar_pantalla()
    listar_recibos()
    recibo_eleccion = seleccionar_recibo()
    if recibo_eleccion == "":
        return

    while True:
        listar_recibo(recibo_eleccion)
        modificar_recibo = input("Introduce una opción: ")
        match modificar_recibo:
            case "1":
                recibo_eleccion['nro_poliza'] = configurar_nro_poliza(recibo_eleccion)
            case "2":
                recibo_eleccion['fecha_inicio'] = configurar_fecha_inicio(recibo_eleccion) 
            case "3":
                recibo_eleccion['duracion'] = configurar_duracion(recibo_eleccion)
            case "4":
                recibo_eleccion['importe_cobrar'] = configurar_importe_cobrar(recibo_eleccion)
            case "5":
                recibo_eleccion['fecha_cobro'] = configurar_fecha_cobro(recibo_eleccion)
            case "6":
                recibo_eleccion['estado_recibo'] = configurar_estado_recibo(recibo_eleccion['nro_poliza'], recibo_eleccion['duracion'], recibo_eleccion['fecha_inicio'], True, recibo_eleccion)
            case "7":
                recibo_eleccion['importe_pagar'] = configurar_importe_pagar(recibo_eleccion)
            case "9":
                break
            case _:
                print("Opción incorrecta")
        guardar_recibos()
        
def mostrar_menu_eliminar_recibo() -> None:
    """Selecciona y elimina un recibo de la lista de recibos"""
    global listaRecibos
    Utilidades.limpiar_pantalla()
    listar_recibos()
    recibo_eleccion = seleccionar_recibo()

    if recibo_eleccion == "":
        return
    
    if recibo_eleccion['estado_recibo'] != "Baja":
        print("No se puede eliminar un recibo que no esté dado de baja")
    else:
        confirmacion = input("¿Estás seguro de que quieres borrar el recibo? (s/n): ")
        if confirmacion == "s":
            listaRecibos.remove(recibo_eleccion)
            guardar_recibos()
            print("Recibo eliminado")
        else:
            print("Operación cancelada")
    input("Pulse <Enter> para continuar")

def listar_recibos() -> None:
    """Muestra una lista con los recibos"""
    print(f"{'ID':<13}{'Póliza':<13}{'Fecha_inicio':<13}{'Duración':<11}{'Importe_cobrar':<15}{'Fecha_cobro':<12}{'Estado_recibo':<17}{'Importe_pagar':<14}{'Estado_liquidación':<19}{'Fecha_liquidación':<20}")
    for recibo in listaRecibos:
        print(f"{recibo['id_recibo']:<13}{recibo['nro_poliza']:<13}{recibo['fecha_inicio']:<13}{recibo['duracion']:<11}{recibo['importe_cobrar']:<15}{recibo['fecha_cobro']:<12}{recibo['estado_recibo']:<17}{recibo['importe_pagar']:<14}{recibo['estado_liquidacion']:<19}{recibo['fecha_liquidacion']:<20}")

def listar_recibo(recibo:dict, creando:bool = False) -> None:
    """Muestra la información de un recibo"""
    Utilidades.limpiar_pantalla()
    if creando:
        print(f"Creando recibo: {recibo['id_recibo']}")
    else:
        print(f"Modificando recibo: {recibo['id_recibo']}")
    print(f"1. Número de póliza: {recibo['nro_poliza']}")
    print(f"2. Fecha de inicio: {recibo['fecha_inicio']}")
    print(f"3. Duración: {recibo['duracion']}")
    print(f"4. Importe a cobrar: {recibo['importe_cobrar']}")
    print(f"5. Fecha de cobro: {recibo['fecha_cobro']}")
    print(f"6. Estado del recibo: {recibo['estado_recibo']}")
    print(f"7. Importe a pagar: {recibo['importe_pagar']}")
    print(f"-> Estado de la liquidación: {recibo['estado_liquidacion']}")
    print(f"-> Fecha de liquidación: {recibo['fecha_liquidacion']}")
    if not creando:
        print("9. Salir")

def generar_id_recibo() -> str:
    """Genera un ID único correlativo para un recibo"""
    return f"{int(ultimo_recibo)+1:012d}"

def seleccionar_recibo() -> str:
    """Pide seleccionar un recibo y devuelve el recibo seleccionado"""
    while True:
        id_recibo = input("Introduce el ID del recibo: ")
        if id_recibo == "":
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
            continue
        try:
            id_recibo = int(id_recibo)
        except:
            print("El ID debe ser un número")
            if id_recibo == "!salir":
                return id_recibo
            continue
        id_recibo = f"{id_recibo:012d}"
        for recibo in listaRecibos:
            if recibo['id_recibo'] == id_recibo:
                return recibo
        else:
            print("El recibo no existe")

def configurar_nro_poliza(recibo_modificar:dict = {}) -> str:
    """Pide el número de póliza, lo valida y lo retorna"""
    while True:
        nro_poliza = input("Introduce el número de póliza: ")

        if nro_poliza == "" and recibo_modificar:
            return recibo_modificar['nro_poliza']
        if nro_poliza == "":
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
            continue
        try:
            nro_poliza = int(nro_poliza)
        except:
            print("El número de póliza debe ser un número")
            continue
        nro_poliza = f"{nro_poliza:012d}"
        for poliza in Polizas.listaPolizas:
            if poliza['nro_poliza'] == nro_poliza:
                return nro_poliza
        else:
            print("La póliza no existe")
            confirmacion = input("¿Quieres cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
    
def configurar_fecha_inicio(recibo_modificar:dict = {}) -> str:
    """Pide la fecha de inicio del recibo, la valida y la retorna"""
    while True:
        fecha = input("Introduce la fecha de inicio del recibo: ")
        if fecha == "" and recibo_modificar:
            return recibo_modificar['fecha_inicio']
        if Utilidades.validar_fecha(fecha):
            return fecha

def configurar_duracion(recibo_modificar:dict = {}) -> str:
    """Pide la duración del recibo, la valida y la retorna"""
    while True:
        print("Introduce la duración del recibo:")
        entrada = input("(A)nual, (S)emestral, (T)rimestral, (M)ensual: ").upper()
        if entrada == "" and recibo_modificar:
            return recibo_modificar['duracion']
        if entrada in ["A", "S", "T", "M","ANUAL", "SEMESTRAL", "TRIMESTRAL", "MENSUAL"]:
            if entrada in ["A", "ANUAL"]:
                entrada = "Anual"
            elif entrada in ["S", "SEMESTRAL"]:
                entrada = "Semestral"
            elif entrada in ["T", "TRIMESTRAL"]:
                entrada = "Trimestral"
            elif entrada in ["M", "MENSUAL"]:
                entrada = "Mensual"
            else:
                print("Opción incorrecta")
            return entrada

def configurar_importe_cobrar(recibo_modificar:dict = {}) -> float:
    """Pide el importe del recibo, lo valida y lo retorna"""
    while True:
        importe_cobrar = input("Introduce el importe del recibo: ")
        if importe_cobrar == "" and recibo_modificar:
            return recibo_modificar['importe_cobrar']
        try:
            importe_cobrar = float(importe_cobrar)
            importe_cobrar = round(importe_cobrar, 2)
            return importe_cobrar
        except:
            print("El importe debe ser un número")

def configurar_fecha_cobro(recibo_modificar:dict = {}) -> str:
    """Pide la fecha de cobro del recibo, la valida y la retorna"""
    while True:
        entrada = input("Introduce la fecha de cobro del recibo (dd/mm/aaaa): ")
        if entrada == "" and recibo_modificar:
            return recibo_modificar['fecha_cobro']
        if Utilidades.validar_fecha(entrada):
            return entrada


def configurar_estado_recibo(poliza_nro:str, duracion_:str, fecha_:str, modificando:bool = False, recibo_modificando:dict = {}) -> str:
    """Pide el estado del recibo, lo valida y lo retorna"""
    while True:
        estado_recibo = input("Introduce el estado del recibo (P)endiente, (C)obrado, (B)aja: ").upper()
        if estado_recibo == "" and recibo_modificando:
            return recibo_modificando['estado_recibo']
        if estado_recibo in ["P", "C", "B", "PENDIENTE", "COBRADO", "BAJA"]:
            if estado_recibo in ["P","PENDIENTE"]:
                for poliza in Polizas.listaPolizas:
                    if poliza['nro_poliza'] == poliza_nro:
                        if poliza['forma_pago'] == "Efectivo":
                            estado_recibo = "Pendiente"
                        else:
                            estado_recibo = "Pendiente_Banco"
                        if poliza['estado_poliza'] == "Cobrada" and modificando:
                            if Polizas.comprobar_vigencia(poliza, recibo_modificando):
                                poliza['estado_poliza'] = "PteCobro"
                        break
            elif estado_recibo in ["C", "COBRADO"]:
                for poliza in Polizas.listaPolizas:
                    if poliza['nro_poliza'] == poliza_nro:
                        if poliza['forma_pago'] == "Efectivo":
                            estado_recibo = "Cobrado"
                        else:
                            estado_recibo = "Cobrado_Banco"
                        break
            elif estado_recibo in ["B", "BAJA"]:
                estado_recibo = "Baja"
            return estado_recibo

def configurar_importe_pagar(recibo_modificar:dict = {}) -> float:
    """Pide el importe a pagar, lo valida y lo retorna"""
    while True:
        importe = input("Introduce el importe a pagar: ")
        if importe == "" and recibo_modificar:
            return recibo_modificar['importe_pagar']
        try:
            importe = float(importe)
            importe = round(importe, 2)
            return importe
        except:
            print("El importe debe ser un número")

listaRecibos = list()
