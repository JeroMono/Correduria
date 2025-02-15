import Polizas
import Liquidaciones

def menu_estadisticas() -> None:
    """Menu de estadisticas, permite selecionar ver la información de una póliza o de una liquidación"""
    opcion_estadistica = "0"
    while (opcion_estadistica != "9"):
        print("1. Información de póliza")
        print("2. Información de liquidación")
        
        print("9. Volver")
        opcion_estadistica = input("Introduce una opción: ")
        match opcion_estadistica:
            case "1":
                informacion_poliza()
            case "2":
                informacion_liquidacion()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")


def informacion_poliza() -> None:
    """Pide seleccionar una póliza y muestra su información"""
    poliza = Polizas.seleccionar_nro_poliza()
    if poliza == "":
        return
    print("Información de la póliza")
    print(f"Número de póliza: {poliza['nro_poliza']}")
    print(f"Tomador: {poliza['id_tomador']}")
    print(f"Datos del vehiculo:")
    print(f"Matricula: {poliza['datos_vehiculo'][0]}")
    print(f"Tipo: {poliza['datos_vehiculo'][1]}")
    print(f"Marca: {poliza['datos_vehiculo'][2]}")
    print(f"Modelo: {poliza['datos_vehiculo'][3]}")
    print(f"Tipo de funcionamiento: {poliza['datos_vehiculo'][4]}")
    print(f"Cobertura: {poliza['cobertura']}")
    print(f"Estado: {poliza['estado_poliza']}")
    print(f"Fecha de emisión: {poliza['fecha_emision']}")
    if type(poliza["forma_pago"])== list:
        print(f"Forma de pago: {poliza['forma_pago'][0]}")
        print(f"Numero de cuenta: {poliza['forma_pago'][1]}")
    else:
        print(f"Forma de pago: {poliza['forma_pago']}")



    

def informacion_liquidacion() -> None:
    """Pide seleccionar una liquidación y muestra su información"""
    liquidacion = Liquidaciones.seleccionar_liquidacion()
    if liquidacion == "":
        return
    
    print("Información de la liquidación")
    print(f"Número de liquidación: {liquidacion['nro_liquidacion']}")
    print(f"Fecha de liquidación: {liquidacion['fecha_liquidacion']}")
    print(f"Estado: {liquidacion['estado_liquidacion']}")
    print(f"Importe recibos de baja: {liquidacion['importe_recibos_baja']}")
    print(f"Importe recibos cobrados: {liquidacion['importe_recibos_cobrados']}")
    print(f"Importe siniestros pagados: {liquidacion['importe_siniestros_pagados']}")
    print(f"Recibos de baja:")
    for recibo in liquidacion['lista_recibos_baja']:
        print(f"  Poliza: {recibo[0]}, Recibo: {recibo[1]}")
    print(f"Recibos cobrados:")
    for recibo in liquidacion['lista_recibos_liquidar']:
        print(f"  Poliza: {recibo[0]}, Recibo: {recibo[1]}")
    print(f"Siniestros pagados:")
    for siniestro in liquidacion['lista_siniestros_liquidados']:
        print(f"  Poliza: {siniestro[0]}, Siniestro: {siniestro[1]}")
    print(f"Importe liquidación:")
    print(f"  A cobrar {liquidacion['importe_liquidacion'][0]} €")
    print(f"  A pagar {liquidacion['importe_liquidacion'][1]} €")    