import Polizas
import Tomadores
import Recibos
import Siniestros
import Liquidaciones
import Estadisticas
from Utilidades import limpiar_pantalla as limpiar_pantalla

def cargar_datos() -> None:
    """Carga los datos de los ficheros en las listas correspondientes de cada módulo.
    También revisa las polizas que estén vigentes y mira si los recibos caducaron, actualizando el estado si es necesario."""
    limpiar_pantalla()
    print("Iniciando carga de datos")
    Polizas.cargar_polizas()
    Tomadores.cargar_tomadores()
    Recibos.cargar_recibos()
    Siniestros.cargar_siniestros()
    Liquidaciones.cargar_liquidaciones()
    Polizas.actualizar_vigencia()
    input("Pulse <Enter> para continuar")

def mostrar_menu_principal() -> None:
    """Muestra el menú principal de la aplicación"""
    opcion = "0"
    while (opcion != "9"):
        limpiar_pantalla()
        print("Correduría Mi Coche Asegurado")
        print("Menú principal\n")
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
                Polizas.mostrar_menu_polizas()
            case "2":
                Tomadores.mostrar_menu_tomadores()
            case "3":
                Recibos.mostrar_menu_recibos()
            case "4":
                Siniestros.mostrar_menu_siniestros()
            case "5":
                Liquidaciones.mostrar_menu_liquidaciones()
            case "6":
                Estadisticas.mostrar_menu_estadisticas()
            case "9":
                print("Cerrando aplicación")
            case _:
                print("Opción incorrecta")
                input("Pulse <Enter> para continuar")

if __name__ == "__main__":
    cargar_datos()
    mostrar_menu_principal()
