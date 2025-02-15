import Tomadores
import Recibos
import Siniestros
import Utilidades
import json

def menu_polizas()-> None:
    """Menú bucle de pólizas. Permite crear, modificar y eliminar pólizas."""
    global listaPolizas
    opcion_polizas = "0"
    while (opcion_polizas != "9"):
        print("1. Crear póliza")
        print("2. Modificar póliza")
        print("3. Eliminar póliza")
        print("9. Salir")
        opcion_polizas = input("Introduce una opción: ")
        match opcion_polizas:
            case "1":
                crear_poliza()
            case "2":
                modificar_poliza()
            case "3":
                eliminar_poliza_menu()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")
    

def crear_poliza()-> None:
    """Crea una póliza. Pide al usuario los datos necesarios y los guarda en el archivo polizas.json."""
    print("Creando póliza")

    nro_poliza = generar_nro_poliza()
    print(f"El número de póliza es: {nro_poliza}")

    id_tomador = buscar_tomador()
    if id_tomador == "!salir":
        return
    
    datos_vehiculo = datosVehiculo()
    cobertura = configurarCobertura()
    id_conductor = configurarConductor(datos_vehiculo[1])


    # estado_poliza = configurarEstado()
    # Dejamos la póliza en estado de pendiente de cobro al crearla, se cambia al poner un recibo cobrado
    estado_poliza = "PteCobro"
    fecha_emision = configurarFecha()
    forma_pago = configurarPago()
    
    listaPolizas.append({"nro_poliza":nro_poliza, "id_tomador":id_tomador, "datos_vehiculo":datos_vehiculo, "cobertura":cobertura, "id_conductor":id_conductor, "estado_poliza":estado_poliza, "fecha_emision":fecha_emision, "forma_pago":forma_pago})
    print(f"Se ha creado la póliza {nro_poliza}")
    guardar_polizas()


def modificar_poliza()-> None:
    """Modifica una póliza. Pide al usuario el número de póliza a modificar y los datos a modificar."""
    global listaPolizas
    listar_polizas()
    
    poliza_edicion = seleccionar_nro_poliza()

    while True:
        listar_poliza(poliza_edicion)
        modificar_opcion = input("Introduce el número de la opción a modificar: ")
        match modificar_opcion:
            case "1":
                tomador = buscar_tomador()
                poliza_edicion["id_tomador"] = tomador if tomador != "!salir" else poliza_edicion["id_tomador"]
                del tomador
            case "2":
                poliza_edicion["datos_vehiculo"] = datosVehiculo()
            case "3":
                poliza_edicion["cobertura"] = configurarCobertura()
            case "4":
                poliza_edicion["id_conductor"] = configurarConductor(poliza_edicion["datos_vehiculo"][1])
            case "5":
                poliza_edicion["estado_poliza"] = configurarEstado()
            case "6":
                poliza_edicion["fecha_emision"] = configurarFecha()
            case "7":
                poliza_edicion["forma_pago"] = configurarPago()
            case "9":
                print("Volviendo al menú Polizas")
                break
            case _:
                print("Opción incorrecta")
        guardar_polizas()


def eliminar_poliza_menu()-> None:
    """Entra en el menú de eliminar Poliza, elegida una elimina una póliza si ésta no está vigente, es decir si está de baja.
    También elimina los recibos y siniestros asociados a la póliza en caso de efectuar la eliminación."""
    listar_polizas()
    poliza_elegida = seleccionar_nro_poliza()

    if comprobar_vigencia(poliza_elegida):
        print("La póliza está vigente, no se puede eliminar")
        return
        
    confirmacion = input("¿Está seguro de que desea eliminar la póliza? (s/n): ").lower()
    if confirmacion != "s":
        return
    
    eliminar_poliza(poliza_elegida)


def listar_polizas()-> None:
    """Muestra todas las pólizas guardadas en el archivo polizas.json. Muestra el número de póliza, el tomador y el vehículo."""
    print(f"{'Nro Póliza':<13}{'Tomador':<10}{'Vehículo':<40}")
    for poliza in listaPolizas:
        print(f"{poliza['nro_poliza']:<13}{poliza['id_tomador']:<10}{poliza['datos_vehiculo']}")

def listar_poliza(poliza:dict)-> None:
    """Muestra los datos de una póliza dada. Con la infromación completa."""
    print(f"Nro Póliza: {poliza['nro_poliza']}")
    print(f"1. Tomador: {poliza['id_tomador']}")
    print(f"2. Vehículo: {poliza['datos_vehiculo'][0]}, {poliza['datos_vehiculo'][1]}, {poliza['datos_vehiculo'][2]}, {poliza['datos_vehiculo'][3]}, {poliza['datos_vehiculo'][4]}")
    print(f"3. Cobertura: {poliza['cobertura']}")
    print(f"4. Conductor: {poliza['id_conductor'][0]}, {poliza['id_conductor'][1]}, {poliza['id_conductor'][2]}, {poliza['id_conductor'][3]}")
    print(f"5. Estado: {poliza['estado_poliza']}")
    print(f"6. Fecha emisión: {poliza['fecha_emision']}")
    print(f"7. Forma de pago: {poliza['forma_pago']}")
    print("9. Volver atrás")


def generar_nro_poliza() -> str:
    """Genera el número de póliza siguiente al último guardado. Devuelve el número de póliza en formato de 12 dígitos."""
    if listaPolizas:
        ultima_poliza = max(int(poliza["nro_poliza"]) for poliza in listaPolizas) + 1
    else:
        ultima_poliza = 0
    return f"{ultima_poliza:012d}"

def seleccionar_nro_poliza()-> str:
    while True:
        nro_poliza = input("Introduce el número de póliza a modificar: ")
        try:
            numero = int(nro_poliza)
        except:
            print("El número de póliza debe ser un número")
            continue
        numero = f"{numero:012d}"
        for poliza in listaPolizas:
            if poliza["nro_poliza"] == numero:
                print(f"Modificando póliza {numero}")
                return poliza
        else:
            print("El número de póliza no existe")
            continue

def cargar_polizas() -> None:
    """Carga las pólizas guardadas en el archivo polizas.json."""
    global listaPolizas
    try:
        with open("polizas.json", "r", encoding="utf-8") as archivo_polizas:
            lista_polizas = json.load(archivo_polizas)
            for poliza in lista_polizas:
                datos_vehiculo = tuple(poliza["datos_vehiculo"])
                cobertura = tuple(poliza["cobertura"])
                id_conductor = tuple(poliza["id_conductor"])
                poliza["datos_vehiculo"] = datos_vehiculo
                poliza["cobertura"] = cobertura
                poliza["id_conductor"] = tuple(id_conductor)
                if len(poliza["forma_pago"])==2:
                    poliza["forma_pago"] = tuple(poliza["forma_pago"])
                else:
                    poliza["forma_pago"] = poliza["forma_pago"]
                listaPolizas.append(poliza)
            del lista_polizas
    except:
        print("No se han encontrado pólizas guardadas")

def guardar_polizas() -> None:
    """Guarda las pólizas en el archivo polizas.json."""
    try:
        with open("polizas.json", "w", encoding="utf-8") as archivo_polizas:
            json.dump(listaPolizas, archivo_polizas, ensure_ascii=False, indent=4)
    except:
        print(f"Error al guardar las pólizas")

def buscar_tomador()-> str:
    """Busca un tomador en la lista de tomadores. Devuelve el DNI, NIE o CIF del tomador si existe, se puede utilizar '!salir' para cancelar la operación."""
    while True:
        tomador_id = input("Introduce el DNI, NIE o CIF del tomador (!salir): ").upper()
        if tomador_id == "!salir":
            return tomador_id
        for tomador in Tomadores.listaTomadores:
            if tomador["id_tomador"] == tomador_id:
                print(f"Tomador: {tomador['id_tomador']} - {tomador['denominacion']}")
                return tomador['id_tomador']
        else:
            print("El tomador no existe")
            tomador_id = ""
            continue

def datosVehiculo()-> tuple:
    """Pide al usuario los datos del vehículo y los devuelve en una tupla."""    
    while True:
        tipos = {"1": "Ciclomotor", "2": "Moto", "3": "Turismo", "4": "Furgoneta", "5": "Camión"}
        for numero, tipo in tipos.items():
            print(f"{numero}. {tipo}")
        entrada = input("Introduce el tipo de vehículo(): ")
        if entrada in ["1", "2", "3", "4", "5"]:
            tipo = tipos[entrada]
            break

    while True:
        matricula = input("Introduce la matrícula del vehículo: ")
        if Utilidades.validar_matricula(matricula, tipo):
            break

    marca = input("Introduce la marca del vehículo: ")
    modelo = input("Introduce el modelo del vehículo: ")
    while True:
        funcionamientos = {"1": "Combustión", "2": "Eléctrico", "3": "Híbrido"}
        for numero, funcionamiento in funcionamientos.items():
            print(f"{numero}. {funcionamiento}")
        entrada = input("Introduce el funcionamiento del vehículo: ")
        if entrada in ["1", "2", "3"]:
            funcionamiento = funcionamientos[entrada]
            break

    return matricula, tipo, marca, modelo, funcionamiento


def configurarCobertura()-> tuple:
    """Configura las coberturas de la póliza. Devuelve una tupla con las coberturas seleccionadas.
    Si se selecciona la cobertura de todo riesgo, se pedirá el valor de la franquicia.
    Valores: RC: Responsabilidad Civil, RL: Rotura de lunas, INC: Incendio, RB: Robo, TR: Todo Riesgo"""
    cobertura = ["RC"]
    while True:
        coberturas = {"1": "RL", "2": "INC", "3": "RB", "4": "TR", "9": "Terminar"}
        print("La póliza tiene las siguientes coberturas:")
        for opcion in cobertura:
            print(opcion, end=" ")
        print()
        for numero, opcion in coberturas.items():
            print(f"{numero}. {opcion}")

        entrada = input("Introduce la cobertura a añadir o quitar: ")
        if entrada in ["1", "2", "3"]:
            if coberturas[entrada] in cobertura:
                print(coberturas[entrada])
                cobertura.remove(coberturas[entrada])
            else:
                cobertura.append(coberturas[entrada])
        elif entrada == "4":
            while True:
                valor_franquicia = input("Introduce el valor de la franquicia: ")
                try: 
                    valor_franquicia = float(valor_franquicia)
                    
                except ValueError:
                    print("El valor de la franquicia debe ser un número")
                    continue
                
                cobertura = ("RC",("TR", valor_franquicia))
                break
            return cobertura
        elif entrada == "9":
            break
    
    return tuple(cobertura)

def configurarConductor(tipo:str)-> tuple:
    """Configura el conductor de la póliza. Pide al usuario los datos del conductor y los devuelve en una tupla.
    Los datos son el DNI o NIE del conductor, la fecha de nacimiento, el tipo de carnet de conducir y la fecha de expedición del carnet.
    Valores de tipo: Ciclomotor, Moto, Turismo, Furgoneta, Camión
    Valores de carnet: A1, A2, A, B, B+E, C1, C1+E, C, C+E, D1, D1+E, D, D+E, AM, BTP
    El tipo de carnet de conducir debe ser válido para el tipo de vehículo. Puede tener varios carnets separados por comas o espacios."""
    while True:
        id = input("Introduce el DNI o NIE del conductor: ").upper()
        if Utilidades.comprobar_dni(id)[0]:
            if Utilidades.comprobar_dni(id)[0]:
                break
            else:
                print("No puede ser un CIF, ha de ser persona física")
        else:
            print("DNI o NIE incorrecto")
    
    while True:
        fecha_nacimiento = input("Introduce la fecha de nacimiento del conductor dd/mm/aaaa: ")
        fecha_nacimiento = Utilidades.validar_fecha(fecha_nacimiento)
        if fecha_nacimiento:
            break
    
    while True:
        tipo_carnet = input("Introduce el tipo de carnet del conductor (Separado por comas o espacios p.e.: B+E, AM): ")
        if Utilidades.validar_carnet_conducir(tipo_carnet, tipo):
            break
        else:
            print("El carnet no es válido para el tipo de vehículo")
            confirmacion = input("¿Desea cancelar la poliza? (s/n): ")
            if confirmacion == "s":
                return
    
    while True:
        fecha_carnet = input("Introduce la fecha de expedición del carnet dd/mm/aaaa: ")
        fecha_carnet = Utilidades.validar_fecha(fecha_carnet)
        if fecha_carnet:
            break
    
    return (id, fecha_nacimiento, tipo_carnet, fecha_carnet)

def configurarEstado()-> str:
    """Configura el estado de la póliza: Cobrada, Pendiente de cobro o de Baja. Devuelve el estado de la póliza."""
    while True:
        estado_poliza = input("Introduce el estado de la póliza ((C)obrada, (P)teCobro, (B)aja): ").upper()
        if estado_poliza in ["COBRADA", "PTECOBRO", "BAJA", "C", "P", "B"]:
            if estado_poliza in ["C", "COBRADA"]:
                estado_poliza = "Cobrada"
            elif estado_poliza in ["P", "PTECOBRO"]:
                estado_poliza = "PteCobro"
            elif estado_poliza in ["B", "BAJA"]:
                estado_poliza = "Baja"
            return estado_poliza

def configurarFecha()-> str:
    """Configura la fecha de emisión de la póliza. Devuelve la fecha en formato dd/mm/aaaa."""
    while True:
        fecha_emision = input("Introduce la fecha de emisión de la póliza dd/mm/aaaa: ")
        fecha_emision = Utilidades.validar_fecha(fecha_emision)
        if fecha_emision:
            return fecha_emision

def configurarPago()-> str:
    """Configura la forma de pago de la póliza: Efectivo o Transferencia Bancaria. Devuelve la forma de pago y el IBAN si es por banco."""
    while True:
        forma_pago = input('Introduce la forma de pago de la póliza [(E)fectivo o (B)anco]: ').upper()
        if forma_pago in ["E", "B", "EFECTIVO", "BANCO"]:
            if forma_pago in ["E", "EFECTIVO"]:
                forma_pago = "Efectivo"
            elif forma_pago in ["B", "BANCO"]:
                forma_pago = "Banco"

        if forma_pago == "Banco":
            while True:
                iban = input("Introduce el IBAN de la cuenta: ")
                if Utilidades.validar_cuenta_bancaria(iban):
                    forma_pago = (forma_pago, iban)
                    opcion_banco = ""
                    break
                else:
                    print("IBAN incorrecto")
                    opcion_banco = input("¿Desea volver atrás? (s/n): ").lower()
                    if opcion_banco == "s":
                        break
            if opcion_banco == "s":
                continue
            return forma_pago
        else:
            return forma_pago

def comprobar_vigencia(poliza:dict, recibo_omitido:dict = {})-> bool:
    """Comprueba si una póliza está vigente o no. Devuelve True si está vigente, False si no lo está."""
    # Compobramos el ultimo recibo y verificamos que esté en fecha según la duración del pago
    if poliza["estado_poliza"] == "Baja":
        return False
    ultimo_recibo_fecha = [00,00,0000]
    ultimo_recibo = ''
    for recibo in Recibos.listaRecibos:
        if recibo["nro_poliza"] == poliza["nro_poliza"] and recibo != recibo_omitido and recibo['estado_recibo'] == "Cobrado":
            if ultimo_recibo_fecha[2] >= int(recibo["fecha_inicio"][2]):
                if ultimo_recibo_fecha[2] >= int(recibo["fecha_inicio"][2]):
                    if ultimo_recibo_fecha[1] >= int(recibo["fecha_inicio"][1]):
                        ultimo_recibo_fecha = map(int,recibo["fecha_inicio"].split("/"))
                        ultimo_recibo = recibo
    if ultimo_recibo_fecha == [00,00,0000]:
        return False
    duracion = ultimo_recibo["duracion"]
    dia_recibo = ultimo_recibo_fecha[0]
    mes_recibo = ultimo_recibo_fecha[1]
    año_recibo = ultimo_recibo_fecha[2]
    if duracion == "Anual":
        ultimo_recibo_fecha = [dia_recibo, mes_recibo, año_recibo + 1]
    elif duracion == "Semestral":
        mes, resto = (mes_recibo + 6) % 12, (mes_recibo + 6) // 12
        año = año_recibo + resto
        ultimo_recibo_fecha = [dia_recibo, mes, año]
    elif duracion == "Trimestral":
        mes, resto = (mes_recibo + 3) % 12, (mes_recibo + 3) // 12
        año = año_recibo + resto
        ultimo_recibo_fecha = [dia_recibo, mes, año]
    elif duracion == "Mensual":
        mes, resto = (mes_recibo + 1) % 12, (mes_recibo + 1) // 12
        año = año_recibo + resto
        ultimo_recibo_fecha = [dia_recibo, mes, año]
    
    fecha_actual = Utilidades.fecha_actual()
    fecha_actual = list(map(int,fecha_actual.split("/")))

    if fecha_actual[2] > ultimo_recibo_fecha[2]:
        return False
    elif fecha_actual[2] <= ultimo_recibo_fecha[2]:
        if fecha_actual[1] > ultimo_recibo_fecha[1]:
            return False
        elif fecha_actual[1] <= ultimo_recibo_fecha[1]:
            if fecha_actual[0] > ultimo_recibo_fecha[0]:
                return False
    
    # if poliza["estado_poliza"] == "PteCobro":
    #     return False
    # if poliza["estado_poliza"] == "Cobrada":
    #     return True
    return True


def eliminar_poliza(poliza_eliminacion:dict)-> None:
    global listaPolizas
    recibos_eliminacion = []
    for recibo in Recibos.listaRecibos:
        if recibo["nro_poliza"] == poliza_eliminacion["nro_poliza"]:
            Recibos.listaRecibos.remove(recibo)
            recibos_eliminacion.append(recibo['id_recibo'])

    if recibos_eliminacion:
        print("Se han eliminado los siguientes recibos asociados a la póliza:")
        for recibo in recibos_eliminacion:
            print(recibo)
    
    siniestros_eliminacion = []
    for siniestro in Siniestros.listaSiniestros:
        if siniestro["nro_poliza"] == poliza_eliminacion["nro_poliza"]:
            Siniestros.listaSiniestros.remove(siniestro)
            siniestros_eliminacion.append(siniestro['nro_siniestro'])

    if siniestros_eliminacion:
        print("Se han eliminado los siguientes siniestros asociados a la póliza:")
        for siniestro in siniestros_eliminacion:
            print(siniestro)

    listaPolizas.remove(poliza_eliminacion)
    print(f"Se ha eliminado la póliza {poliza_eliminacion['nro_poliza']} con {len(recibos_eliminacion)} recibos y {len(siniestros_eliminacion)} siniestros asociados")
    guardar_polizas()
    Recibos.guardar_recibos()
    Siniestros.guardar_siniestros()


listaPolizas = list()
ultima_poliza = 0
