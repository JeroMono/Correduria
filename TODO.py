# REVISAR siniestros a la hora de crear que este vigente la poliza

#Comentarios y revisar definiciones de funciones

# Revisar modificar tuplas, que cuando este modificando
# si no se pone valor no modifique y pase al siguiente

# Coberturas polizas al editar, que lea las que tiene

# LIQUIDACIONES SINIESTROS -> CAMBIAR ESTADOS AL LIQUIDAR?


# DUDAS:
"""
Estado vigente del siniestro:
Porque los valores son Pendiente confirmar, Confirmado, pendiente pago y pagado
Yo puse mientras esté pendiente de confirmar
"""
import Utilidades
listaRecibos=[
        {
            "id_recibo": "000000000000",
            "nro_poliza": "000000000000",
            "fecha_inicio": "12/2/2023",
            "duracion": "Semestral",
            "importe_cobrar": 250.0,
            "fecha_cobro": "20/2/2024",
            "estado_recibo": "Pendiente_Banco",
            "importe_pagar": 500.0,
            "estado_liquidacion": "Pendiente",
            "fecha_liquidacion": ""
        },
        {
            "id_recibo": "000000000001",
            "nro_poliza": "000000000002",
            "fecha_inicio": "25/11/2024",
            "duracion": "Anual",
            "importe_cobrar": 250.0,
            "fecha_cobro": "30/11/2024",
            "estado_recibo": "Cobrado",
            "importe_pagar": 250.0,
            "estado_liquidacion": "Pendiente",
            "fecha_liquidacion": ""
        },
        {
            "id_recibo": "000000000002",
            "nro_poliza": "000000000003",
            "fecha_inicio": "25/12/2024",
            "duracion": "Semestral",
            "importe_cobrar": 265.0,
            "fecha_cobro": "30/12/2024",
            "estado_recibo": "Cobrado",
            "importe_pagar": 235.0,
            "estado_liquidacion": "Pendiente",
            "fecha_liquidacion": ""
        },
        {
            "id_recibo": "000000000004",
            "nro_poliza": "000000000000",
            "fecha_inicio": "12/12/2021",
            "duracion": "Anual",
            "importe_cobrar": 250.0,
            "fecha_cobro": "12/12/2021",
            "estado_recibo": "Cobrado_Banco",
            "importe_pagar": 250.0,
            "estado_liquidacion": "Pendiente",
            "fecha_liquidacion": ""
        },
        {
            "id_recibo": "000000000006",
            "nro_poliza": "000000000000",
            "fecha_inicio": "24/6/2024",
            "duracion": "Semestral",
            "importe_cobrar": 300.0,
            "fecha_cobro": "30/2/2024",
            "estado_recibo": "Cobrado_Banco",
            "importe_pagar": 300.0,
            "estado_liquidacion": "Pendiente",
            "fecha_liquidacion": ""
        }
    ]

poliza = {
            "nro_poliza": "000000000000",
            "id_tomador": "43491650F",
            "matricula": "TF9652BX",
            "datos_vehiculo": [
                "Turismo",
                "Seat",
                "Cordoba",
                "Combustión"
            ],
            "cobertura": [
                "RC",
                "RL",
                "INC",
                "RB"
            ],
            "id_conductor": [
                "43491650F",
                "14/06/1990",
                "B+E",
                "15/06/2008"
            ],
            "estado_poliza": "PteCobro",
            "fecha_emision": "28/07/2009",
            "forma_pago": [
                "Banco",
                "ES6621000418401234567891"
            ]
        }

# PENDIENTE:

def comprobar_vigencia(poliza:dict, recibo_omitido:dict = {})-> bool:
    """Comprueba si una póliza está vigente o no. Devuelve True si está vigente, False si no lo está."""
    # Compobramos el ultimo recibo y verificamos que esté en fecha según la duración del pago
    if poliza["estado_poliza"] == "Baja":
        return False
    ultimo_recibo_fecha = [1900,1,1]
    ultimo_recibo = None

    # Buscamos el último recibo cobrado
    for recibo in listaRecibos:
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
    valor_duracion = valores_duracion[duracion]
    mes = (mes_recibo + valor_duracion ) % 12
    año = año_recibo + ((mes_recibo + valor_duracion - 1) // 12)
    ultimo_recibo_fecha = [año, mes if mes != 0 else 12, dia_recibo]


    print(ultimo_recibo_fecha)
    fecha_actual = Utilidades.fecha_actual()
    fecha_actual = list(map(int,fecha_actual.split("/")))

    # Ahora sí podemos comparar la fecha actual con la fecha del último recibo más el plazo de vigencia
    if fecha_actual > ultimo_recibo_fecha:
        return False
    return True

#print(comprobar_vigencia(poliza))

año_recibo = 2024
dia_recibo = 30
for mes_recibo in range(1, 13):
    for valor_duracion in (1, 3, 6, 12):
        print(f"[{año_recibo}/{mes_recibo}/{dia_recibo}]",end=" ")
        mes = (mes_recibo + valor_duracion ) % 12
        año = año_recibo + ((mes_recibo + valor_duracion - 1) // 12)
        ultimo_recibo_fecha = [año, mes if mes != 0 else 12, dia_recibo]
        print(valor_duracion, ultimo_recibo_fecha)
