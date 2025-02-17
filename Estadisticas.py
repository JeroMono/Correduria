import Polizas
import Liquidaciones
import Siniestros
import Recibos
from Utilidades import limpiar_pantalla as limpiar_pantalla

def mostrar_menu_estadisticas() -> None:
    """Menu de estadisticas, permite selecionar ver la información de una póliza o de una liquidación"""
    opcion_estadistica = "0"
    while (opcion_estadistica != "9"):
        limpiar_pantalla()
        print("1. Información de póliza")
        print("2. Información de liquidación")
        
        print("9. Volver")
        opcion_estadistica = input("Introduce una opción: ")
        match opcion_estadistica:
            case "1":
                mostrar_menu_informacion_poliza()
            case "2":
                mostrar_menu_informacion_liquidacion()
            case "9":
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")


def mostrar_menu_informacion_poliza() -> None:
    """Pide seleccionar una póliza y muestra su información"""
    limpiar_pantalla()
    Polizas.listar_polizas()
    poliza = Polizas.seleccionar_nro_poliza()
    if poliza == "":
        return
    limpiar_pantalla()
    print("Información de la póliza")
    print(f"Número de póliza: {poliza['nro_poliza']}")
    print(f"Tomador: {poliza['id_tomador']}")
    print(f"Matricula: {poliza['matricula']}")
    print(f"Tipo: {poliza['datos_vehiculo'][0]}, Marca: {poliza['datos_vehiculo'][1]}, Modelo: {poliza['datos_vehiculo'][2]}, Tipo de funcionamiento: {poliza['datos_vehiculo'][3]}")
    print(f"Cobertura: ", end="")
    if type(poliza['cobertura']) == str:
        print(poliza['cobertura'])
    elif type(poliza['cobertura']) == tuple:
        if type(poliza['cobertura'][1]) == tuple:
            print(f"{poliza['cobertura'][0]}, {poliza['cobertura'][1][0]} con franquicia de {poliza['cobertura'][1][1]}")
        else:
            for cobertura in poliza['cobertura'][:-1]:
                print(cobertura, end=" ")
            print(poliza['cobertura'][-1])

    print(f"Estado: {poliza['estado_poliza']}")
    print(f"Fecha de emisión: {poliza['fecha_emision']}")
    if len(poliza['forma_pago']) == 2:
        print(f"Forma de pago: {poliza['forma_pago'][0]}")
        print(f"   IBAN: {poliza['forma_pago'][1]}")
    else:
        print(f"Forma de pago: {poliza['forma_pago']}")
    print("Vigencia: ",end="")
    print('Vigente' if Polizas.comprobar_vigencia(poliza) else 'No Vigente')
    print("Recibos asociados:")
    for recibo in Recibos.listaRecibos:
        if recibo["nro_poliza"] == poliza["nro_poliza"]:
            print(f"  Número de recibo: {recibo['id_recibo']}, Fecha de inicio: {recibo['fecha_inicio']}, Estado: {recibo['estado_recibo']}")
    print("Siniestros asociados:")
    for siniestro in Siniestros.listaSiniestros:
        if siniestro["nro_poliza"] == poliza["nro_poliza"]:
            print(f"  Número de siniestro: {siniestro['nro_siniestro']}, Importe siniestro: {siniestro['importe_pagar']}, Descrición: {siniestro['descripcion']}")
    input("Pulse <Enter> para continuar")

def mostrar_menu_informacion_liquidacion() -> None:
    """Pide seleccionar una liquidación y muestra su información"""
    limpiar_pantalla()
    Liquidaciones.listar_liquidaciones()
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
    input("Pulse <Enter> para continuar")