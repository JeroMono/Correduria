import Tomadores
import Recibos
import Siniestros
import Utilidades
import json

def mostrar_menu_polizas()-> None:
    """Menú bucle de pólizas. Permite enrar en los menus de crear, modificar y eliminar pólizas."""
    global listaPolizas
    opcion_polizas = "0"
    while (opcion_polizas != "9"):
        Utilidades.limpiar_pantalla()
        print("1. Crear póliza")
        print("2. Modificar póliza")
        print("3. Eliminar póliza")
        print("9. Salir")
        opcion_polizas = input("Introduce una opción: ")
        match opcion_polizas:
            case "1":
                mostrar_menu_crear_poliza()
            case "2":
                mostrar_menu_modificar_poliza()
            case "3":
                mostrar_menu_eliminar_poliza()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")

def mostrar_menu_crear_poliza()-> None:
    """Menú para crear una póliza. Pide al usuario los datos necesarios y los guarda en el archivo polizas.json."""
    Utilidades.limpiar_pantalla()
    print("Creando póliza")

    nro_poliza = generar_nro_poliza()
    print(f"El número de póliza es: {nro_poliza}")

    id_tomador = seleccionar_tomador()
    if id_tomador == "":
        return
    
    datos_vehiculo = configurar_datos_vehiculo()
    if datos_vehiculo == ():
        return
    
    matricula = datos_vehiculo[0]
    datos_vehiculo = datos_vehiculo[1:]
    
    cobertura = configurar_cobertura()

    id_conductor = configurar_conductor(datos_vehiculo[0])

    # Dejamos la póliza en estado de pendiente de cobro al crearla, se cambia al poner un recibo cobrado vigente
    estado_poliza = "PteCobro"

    fecha_emision = configurar_fecha_emision()

    forma_pago = configurar_pago()
    
    poliza = {"nro_poliza":nro_poliza, "id_tomador":id_tomador, "matricula":matricula, "datos_vehiculo":datos_vehiculo, "cobertura":cobertura, "id_conductor":id_conductor, "estado_poliza":estado_poliza, "fecha_emision":fecha_emision, "forma_pago":forma_pago}

    crear_poliza(poliza)

def crear_poliza(poliza:dict)-> None:
    """Crea una póliza con los datos dados y la guarda en el archivo polizas.json. Pide confirmación al usuario antes de guardar."""
    global listaPolizas, ultima_poliza
    while True:
        listar_poliza(poliza, True)
        confirmacion = input("¿Desea guardar la póliza? (s/n): ").lower()
        if confirmacion == "s":
            listaPolizas.append(poliza)
            print(f"Se ha creado la póliza {poliza['nro_poliza']}")
            ultima_poliza = int(poliza["nro_poliza"])
            guardar_polizas()
            break
        elif confirmacion == "n":
            print("Póliza no creada")
            break

def mostrar_menu_modificar_poliza()-> None:
    """Menú para modificar una póliza. Pide al usuario el número de póliza a modificar y luego permite elegir los datos a modificar."""
    global listaPolizas
    Utilidades.limpiar_pantalla()
    listar_polizas()
    
    poliza_edicion = seleccionar_nro_poliza()
    if poliza_edicion == "":
        return

    # Bucle de modificación de la póliza
    while True:
        listar_poliza(poliza_edicion)
        modificar_opcion = input("Introduce el número de la opción a modificar: ")
        match modificar_opcion:
            case "1":
                tomador = seleccionar_tomador()
                poliza_edicion["id_tomador"] = tomador if tomador != "!salir" else poliza_edicion["id_tomador"]
                del tomador
            case "2":
                datos = configurar_datos_vehiculo(poliza_edicion["id_conductor"], poliza_edicion)
                if datos == ():
                    continue
                poliza_edicion["matricula"] = datos[0]
                poliza_edicion["datos_vehiculo"] = datos[1:]
            case "3":
                poliza_edicion["cobertura"] = configurar_cobertura()
            case "4":
                datos = configurar_conductor(poliza_edicion["datos_vehiculo"][0],poliza_edicion)
                if datos == ():
                    continue
                poliza_edicion["id_conductor"] = datos
            case "5":
                poliza_edicion["estado_poliza"] = configurarEstado()
            case "6":
                poliza_edicion["fecha_emision"] = configurar_fecha_emision()
            case "7":
                poliza_edicion["forma_pago"] = configurar_pago()
            case "9":
                print("Volviendo al menú Polizas")
                break
            case _:
                print("Opción incorrecta")
        guardar_polizas()

def mostrar_menu_eliminar_poliza()-> None:
    """Entra en el menú de eliminar Poliza, elegida una elimina una póliza si ésta no está vigente, es decir si está de baja.
    También elimina los recibos y siniestros asociados a la póliza en caso de efectuar la eliminación."""
    Utilidades.limpiar_pantalla()
    listar_polizas()
    poliza_elegida = seleccionar_nro_poliza()
    if poliza_elegida == "":
        return

    if comprobar_vigencia(poliza_elegida):
        print("La póliza está vigente, no se puede eliminar")
        input("Pulse <Enter> para continuar")
        return
        
    confirmacion = input("¿Está seguro de que desea eliminar la póliza? (s/n): ").lower()
    if confirmacion != "s":
        return
    
    eliminar_poliza(poliza_elegida)
    print("Póliza eliminada")
    input("Pulse <Enter> para continuar")


def listar_polizas()-> None:
    """Muestra todas las pólizas guardadas en el archivo polizas.json. Muestra el número de póliza, el tomador, la vigencia y la matrícula vehículo."""
    print(f"{'Nro Póliza':<13}{'Tomador':<10}{'Vigencia':<11}{'Matricula':<10}")
    print("=" * 90)
    for poliza in listaPolizas:
        print(f"{poliza['nro_poliza']:<13}{poliza['id_tomador']:<10}{'Vigente' if comprobar_vigencia(poliza) else 'No Vigente':<11}{poliza['matricula']:<10}")


def listar_poliza(poliza:dict, creando:bool = False)-> None:
    """Muestra los datos de una póliza dada para modificarla, se necesitas los datos de la póliza y si se está creando o modificando."""
    Utilidades.limpiar_pantalla()

    print(f"Nro Póliza: {poliza['nro_poliza']}")
    print(f"1. Tomador: {poliza['id_tomador']}")
    print(f"2. Vehículo: {poliza['matricula']}, {poliza['datos_vehiculo'][0]}, {poliza['datos_vehiculo'][1]}, {poliza['datos_vehiculo'][2]}, {poliza['datos_vehiculo'][3]}")
    print(f"3. Cobertura: ", end="")
    if type(poliza['cobertura']) == str:
        print(poliza['cobertura'])
    elif type(poliza['cobertura']) == tuple:
        if type(poliza['cobertura'][1]) == tuple:
            print(f"{poliza['cobertura'][0]}, {poliza['cobertura'][1][0]} con franquicia de {poliza['cobertura'][1][1]}")
        else:
            for cobertura in poliza['cobertura'][:-1]:
                print(cobertura, end=" ")
            print(poliza['cobertura'][-1])

    print(f"4. Conductor: {poliza['id_conductor'][0]}, {poliza['id_conductor'][1]}, {poliza['id_conductor'][2]}, {poliza['id_conductor'][3]}")
    print(f"5. Estado: {poliza['estado_poliza']}")
    print(f"6. Fecha emisión: {poliza['fecha_emision']}")
    if len(poliza['forma_pago']) == 2:
        print(f"7. Forma de pago: {poliza['forma_pago'][0]}")
        print(f"   IBAN: {poliza['forma_pago'][1]}")
    else:
        print(f"7. Forma de pago: {poliza['forma_pago']}")
    if not creando:
        print("9. Volver atrás")


def generar_nro_poliza() -> str:
    """Genera el número de póliza siguiente al último guardado. Devuelve el número de póliza en formato de 12 dígitos."""
    return f"{int(ultima_poliza) + 1:012d}"

def seleccionar_nro_poliza()-> str:
    """Busca un número de póliza en la lista de pólizas (no es necesario poner los ceros del formato, con poner 1 busca la 000000000001). Devuelve la póliza si existe, se puede utilizar '' para cancelar la operación."""
    while True:
        nro_poliza = input("Introduce el número de póliza: ")
        if nro_poliza == "":
            confirmacion = input("¿Desea cancelar la operación? (s/n): ").lower()
            if confirmacion == "s":
                return ""
            continue
        try:
            numero = int(nro_poliza)
        except:
            print("El número de póliza debe ser un número")
            continue
        numero = f"{numero:012d}"
        for poliza in listaPolizas:
            if poliza["nro_poliza"] == numero:
                print(f"Seleccionada póliza {numero}")
                return poliza
        else:
            print("El número de póliza no existe")
            continue

def cargar_polizas() -> None:
    """Carga las pólizas guardadas en el archivo polizas.json en la lista de pólizas."""
    global listaPolizas, ultima_poliza
    try:
        with open("polizas.json", "r", encoding="utf-8") as archivo_polizas:
            data = json.load(archivo_polizas)
            ultima_poliza = data["ultima_poliza"]
            lista_polizas = data["polizas"]
            for poliza in lista_polizas:
                datos_vehiculo = tuple(poliza["datos_vehiculo"])
                if poliza["cobertura"]=="RC":
                    cobertura = "RC" 
                else:
                    cobertura = tuple(poliza["cobertura"])
                    if type(cobertura[1]) == list:
                        cobertura = (cobertura[0], tuple(cobertura[1]))
                id_conductor = tuple(poliza["id_conductor"])
                poliza["datos_vehiculo"] = datos_vehiculo
                poliza["cobertura"] = cobertura
                poliza["id_conductor"] = tuple(id_conductor)
                if len(poliza["forma_pago"]) == 2:
                    poliza["forma_pago"] = tuple(poliza["forma_pago"])
                else:
                    poliza["forma_pago"] = poliza["forma_pago"]
                listaPolizas.append(poliza)
            del lista_polizas
            print(f"{len(listaPolizas)} Polizas cargadas correctamente")
    except:
        print("No se han encontrado pólizas guardadas")
        ultima_poliza = 0

def guardar_polizas() -> None:
    """Guarda la lista de pólizas en el archivo polizas.json."""
    global ultima_poliza
    try:
        with open("polizas.json", "w", encoding="utf-8") as archivo_polizas:
            json.dump({"ultima_poliza": ultima_poliza, "polizas": listaPolizas}, archivo_polizas, ensure_ascii=False, indent=4)
    except:
        print(f"Error al guardar las pólizas")

def seleccionar_tomador()-> str:
    """Busca un tomador en la lista de tomadores. Devuelve el DNI, NIE o CIF del tomador si existe, se puede utilizar '' para cancelar la operación."""
    while True:
        tomador_id = input("Introduce el DNI, NIE o CIF del tomador: ").upper()
        if tomador_id == "":
            confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
            if confirmacion == "s":
                return tomador_id
            continue
        for tomador in Tomadores.listaTomadores:
            if tomador["id_tomador"] == tomador_id:
                print(f"Tomador: {tomador['id_tomador']} - {tomador['denominacion']}")
                return tomador['id_tomador']
        else:
            print("El tomador no existe")
            tomador_id = ""
            continue

def configurar_datos_vehiculo(conductor_modificando:tuple = (), poliza_edicion:dict = {})-> tuple:
    """Pide al usuario los datos del vehículo y los devuelve en una tupla."""    
    # Tipo de vehículo
    while True:
        tipos = {"1": "Ciclomotor", "2": "Moto", "3": "Turismo", "4": "Furgoneta", "5": "Camión"}
        for numero, tipo in tipos.items():
            print(f"{numero}. {tipo}")
        entrada = input("Introduce el tipo de vehículo(): ")
        if entrada == "" and poliza_edicion:
            tipo = poliza_edicion["datos_vehiculo"][0]
            break
        if entrada in ["1", "2", "3", "4", "5"]:
            if not conductor_modificando:
                tipo = tipos[entrada]
                break
            else:
                if Utilidades.validar_carnet_conducir(conductor_modificando[2], tipos[entrada]):
                    tipo = tipos[entrada]
                    break
                else:
                    print("El carnet no es válido para el tipo de vehículo")
                    confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
                    if confirmacion == "s":
                        return ()

    # Matrícula, se valida según el tipo de vehículo
    while True:
        matricula = input("Introduce la matrícula del vehículo: ").upper()
        if matricula == "" and poliza_edicion:
            matricula = poliza_edicion["matricula"]
            if Utilidades.validar_matricula(matricula, tipo):
                break
            else:
                print("Matrícula incorrecta")
                confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
                if confirmacion == "s":
                    return ()
            continue
        if Utilidades.validar_matricula(matricula, tipo):
            break
        else:
            print("Matrícula incorrecta")
            confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
            if confirmacion == "s":
                return ()

    # Marca
    while True:
        marca = input("Introduce la marca del vehículo: ")
        if marca == "" and poliza_edicion:
            marca = poliza_edicion["datos_vehiculo"][1]
            break
        if marca == "":
            confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
            if confirmacion == "s":
                return ()
            continue
        break
    
    # Modelo
    while True:
        modelo = input("Introduce el modelo del vehículo: ")
        if modelo == "" and poliza_edicion:
            modelo = poliza_edicion["datos_vehiculo"][2]
            break
        if modelo == "":
            confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
            if confirmacion == "s":
                return ()
            continue
        break
    
    # Funcionamiento del vehículo
    while True:
        funcionamientos = {"1": "Combustión", "2": "Eléctrico", "3": "Híbrido"}
        for numero, funcionamiento in funcionamientos.items():
            print(f"{numero}. {funcionamiento}")
        entrada = input("Introduce el funcionamiento del vehículo: ")
        if entrada == "" and poliza_edicion:
            funcionamiento = poliza_edicion["datos_vehiculo"][3]
            break
        if entrada in ["1", "2", "3"]:
            funcionamiento = funcionamientos[entrada]
            break
    
    # Confirmación de los datos
    while True:
        print(f"Datos del vehículo: {matricula}, {tipo}, {marca}, {modelo}, {funcionamiento}")
        confirmacion = input("¿Son correctos los datos? (s/n): ").lower()
        if confirmacion == "n":
            return ()
        elif confirmacion == "s":
            return matricula, tipo, marca, modelo, funcionamiento


def configurar_cobertura()-> tuple:
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
        # Si se elige el todo riesgo, se pide el valor de la franquicia, y no se utilizan otras coberturas, solo la RC
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
    if cobertura == ["RC"]:
        return "RC"
    return tuple(cobertura)

def configurar_conductor(tipo:str, poliza_edicion:dict = {})-> tuple:
    """Configura el conductor de la póliza. Pide al usuario los datos del conductor y los devuelve en una tupla.
    Los datos son el DNI o NIE del conductor, la fecha de nacimiento, el tipo de carnet de conducir y la fecha de expedición del carnet.
    Valores de tipo: Ciclomotor, Moto, Turismo, Furgoneta, Camión
    Valores de carnet: A1, A2, A, B, B+E, C1, C1+E, C, C+E, D1, D1+E, D, D+E, AM, BTP
    El tipo de carnet de conducir debe ser válido para el tipo de vehículo. Puede tener varios carnets separados por comas o espacios."""
    # DNI o NIE
    while True:
        id = input("Introduce el DNI o NIE del conductor: ").upper()
        # Si estamos modificando y dejamos vacío, tomamos el valor existente
        if id == "" and poliza_edicion:
            id = poliza_edicion["id_conductor"][0]
            break
        if Utilidades.comprobar_dni(id)[0]:
            if Utilidades.comprobar_dni(id)[1]:
                break
            else:
                print("No puede ser un CIF, ha de ser persona física")
        else:
            print("DNI o NIE incorrecto")
        confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
        if confirmacion == "s":
            return ()
    
    while True:
        fecha_nacimiento = input("Introduce la fecha de nacimiento del conductor dd/mm/aaaa: ")
        # Si estamos modificando y dejamos vacío, tomamos el valor existente
        if fecha_nacimiento == "" and poliza_edicion:
            fecha_nacimiento = poliza_edicion["id_conductor"][1]
            break
        fecha_nacimiento = Utilidades.validar_fecha(fecha_nacimiento)
        if fecha_nacimiento:
            break
    
    while True:
        print("Los tipos de carnet válidos son: AM, A1, A2, A, B, B+E, C1, C1+E, C, C+E")
        tipo_carnet = input("Introduce el tipo de carnet del conductor (Separado por comas o espacios p.e.: B+E, AM): ")
        # Si estamos modificando y dejamos vacío, tomamos el valor existente
        if tipo_carnet == "" and poliza_edicion:
            tipo_carnet = poliza_edicion["id_conductor"][2]
            break
        if Utilidades.validar_carnet_conducir(tipo_carnet, tipo):
            break
        else:
            print("El carnet no es válido para el tipo de vehículo")
            confirmacion = input("¿Desea cancelar la poliza? (s/n): ").lower()
            if confirmacion == "s":
                return
    
    while True:
        fecha_carnet = input("Introduce la fecha de expedición del carnet dd/mm/aaaa: ")
        # Si estamos modificando y dejamos vacío, tomamos el valor existente
        if fecha_carnet == "" and poliza_edicion:
            fecha_carnet = poliza_edicion["id_conductor"][3]
            break
        fecha_carnet = Utilidades.validar_fecha(fecha_carnet)
        if fecha_carnet:
            break

    while True:
        print(f"Datos del conductor: {id}, {fecha_nacimiento}, {tipo_carnet}, {fecha_carnet}")
        confirmacion = input("¿Son correctos los datos? (s/n): ").lower()
        if confirmacion == "n":
            return ()
        elif confirmacion == "s":
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

def configurar_fecha_emision()-> str:
    """Configura la fecha de emisión de la póliza. Devuelve la fecha en formato dd/mm/aaaa."""
    while True:
        fecha_emision = input("Introduce la fecha de emisión de la póliza dd/mm/aaaa: ")
        fecha_emision = Utilidades.validar_fecha(fecha_emision)
        if fecha_emision:
            return fecha_emision

def configurar_pago()-> str:
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
    ultimo_recibo_fecha = [1900,1,1]
    ultimo_recibo = None

    # Buscamos el último recibo cobrado
    for recibo in Recibos.listaRecibos:
        if recibo["nro_poliza"] == poliza["nro_poliza"] and recibo != recibo_omitido and recibo['estado_recibo'] in ["Cobrado","Cobrado_Banco"]:
            fecha_recibo = list(map(int,recibo["fecha_inicio"].split("/")))[::-1]
            if ultimo_recibo_fecha < fecha_recibo:
                ultimo_recibo_fecha = fecha_recibo
                ultimo_recibo = recibo
    if ultimo_recibo_fecha == [1900,1,1]:
        return False
    duracion = ultimo_recibo["duracion"]
    dia_recibo = ultimo_recibo_fecha[2]
    mes_recibo = ultimo_recibo_fecha[1]
    año_recibo = ultimo_recibo_fecha[0]

    valores_duracion = {"Anual": 12, "Semestral": 6, "Trimestral": 3, "Mensual": 1}
    # Al último recibo le sumamos la duracion y comprobamos si queda en fecha

    valor_duracion = valores_duracion[duracion]
    mes = (mes_recibo + valor_duracion ) % 12
    año = año_recibo + ((mes_recibo + valor_duracion - 1) // 12)
    ultimo_recibo_fecha = [año, mes if mes != 0 else 12, dia_recibo]

    fecha_actual = Utilidades.fecha_actual()
    fecha_actual = list(map(int,fecha_actual.split("/")))

    # Ahora sí podemos comparar la fecha actual con la fecha del último recibo más el plazo de vigencia
    if fecha_actual > ultimo_recibo_fecha:
        return False
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

def actualizar_vigencia()-> None:
    """Comprueba que las polizas cobradas al momento de iniciar el programa estén vigentes, si están cobradas pero ya no hay recibos vigentes las cambia a pendientes de cobro."""
    global listaPolizas
    print("Comprobando vigencia de las pólizas a día de hoy")
    for poliza in listaPolizas:
        if not comprobar_vigencia(poliza):
            if poliza["estado_poliza"] == "Cobrada":
                poliza["estado_poliza"] = "PteCobro"
                print(f"La póliza {poliza['nro_poliza']} ha pasado a estar pendiente de cobro")
    guardar_polizas()

listaPolizas = list()
