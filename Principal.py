import Polizas
import Tomadores
import Recibos
import Siniestros
import Liquidaciones
import Estadisticas
from Utilidades import limpiar_pantalla as limpiar_pantalla

if __name__ == "__main__":
    Polizas.cargar_polizas()
    Tomadores.cargar_tomadores()
    Recibos.cargar_recibos()
    Siniestros.cargar_siniestros()
    Liquidaciones.cargar_liquidaciones()
    Siniestros.guardar_siniestros()
    opcion = "0"
    while (opcion != "9"):
        limpiar_pantalla()
        print("1. Pólizas")
        print("2. Tomadores")
        print("3. Recibos")
        print("4. Siniestros")
        print("5. Liquidaciones")
        print("6. Estadisticas")
        print("9. Salir")
        opcion = input("Opción: ")
        match opcion:
            case "1":
                Polizas.menu_polizas()
            case "2":
                Tomadores.menu_tomadores()
            case "3":
                Recibos.menu_recibos()
            case "4":
                Siniestros.menu_siniestros()
            case "5":
                Liquidaciones.menu_liquidaciones()
            case "6":
                Estadisticas.menu_estadisticas()
            case "9":
                print("Cerrando aplicación")
            case _:
                print("Opción incorrecta")
