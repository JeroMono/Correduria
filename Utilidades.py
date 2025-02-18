import datetime
import os

def comprobar_dni(dni:str) -> tuple[bool, bool]:
    """ Comprueba si un DNI, NIE o CIF es correcto.
    El primer valor es si es correcto, el segundo si es un CIF."""
    LETRAS_NIF = "TRWAGMYFPDXBNJZSQVHLCKE"
    LETRAS_NIE = "XYZ"
    LETRAS_CIF = "ABCDEFGHJNPQRSUVW"
    LETRAS_CONTROL = "JABCDEFGHI"
    # Validación de CIF
    if len(dni) == 9 and dni[0].upper() in LETRAS_CIF:
        if(((dni[0].isalpha()) and dni[1:-1].isdigit())):
            cif = dni.upper().strip()

            if len(cif) != 9 or not cif[1:8].isdigit():
                return False
            
            letra = cif[0]
            numeros = list(map(int, cif[1:8]))
            control = cif[8]

            # Cálculo del dígito de control
            suma_pares = sum(numeros[1::2])
            suma_impares = 0
            for digito in numeros[0::2]:
                suma_impares += (2 * digito // 10) + (2 * digito % 10)
            total = suma_pares + suma_impares
            digito_control = (10 - (total % 10)) % 10
            # Dependiendo del tipo de entidad, el control puede ser número o letra
            if letra in "PQRSNW":
                return (control == LETRAS_CONTROL[digito_control], False)
            elif letra in "ABEH":
                return (control == str(digito_control), False)
            else:
                return ((control == str(digito_control) or control == LETRAS_CONTROL[digito_control]), False)  # Ambos posibles
        else:
            return (False, False)
    
    elif len(dni) == 9 and dni[-1].isalpha():
        # Validación de NIE
        if((dni[0].upper() in LETRAS_NIE) and dni[1:-1].isdigit()):
            combinado = int(str(LETRAS_NIE.index(dni[0])) + dni[1:-1])
            if (dni[-1] == LETRAS_NIF[(combinado%23)]):
                return (True, True)
        # Validación de NIF
        elif (dni[:-1].isdigit()):
            if dni[-1] == LETRAS_NIF[(int(dni[:-1]) % 23)]:
                return (True, True)
        else:
            return (False, False)
    return (False, False)


def iban_a_numero(iban:str) -> int:
    """Convierte un IBAN en un número para la verificación."""
    iban = iban.replace(" ", "").upper()
    iban = iban[4:] + iban[:4]
    
    # Tabla de conversión de letras a números
    ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    iban_numerico = ""
    for char in iban:
        if char.isalpha():
            iban_numerico += str(ALFABETO.index(char) + 10)
        else:
            iban_numerico += char
    
    return int(iban_numerico)

def validar_cuenta_bancaria(iban:str) -> bool:
    """Calcula si el IBAN es válido usando el módulo 97."""
    if len(iban) != 24:
        return False
    iban_numerico = iban_a_numero(iban)
    return iban_numerico % 97 == 1

def validar_fecha(fecha:str) -> str:
    """Comprueba si una fecha es válida."""
    fecha = fecha.split("/")
    if len(fecha) == 3:
        try:
            dia = int(fecha[0])
            mes = int(fecha[1])
            año = int(fecha[2])
        except:
            return ""
        else:
            # Validación de la fecha que sea real
            if 1 <= dia <= 31 and 1 <= mes <= 12 and (AÑO_LIMITE_INFERIOR <= año <= AÑO_LIMITE_SUPERIOR):
                if mes in [4, 6, 9, 11] and dia > 30:
                    return ""
                elif (mes == 2 and ((año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)) and dia > 29) or (mes == 2 and dia > 28 and (año % 4 != 0 or (año % 100 == 0 and año % 400 != 0))):
                    return ""
                else:
                    # Formateamos la fecha para que siempre tenga 2 dígitos
                    return f"{dia:02d}/{mes:02d}/{año}"
            else:
                return ""
    else:
        return ""
    
def validar_email(email:str) -> bool:
    """Comprueba si un email es válido."""
    partes = email.split('@')
    if len(partes) != 2:
        return False
    
    nombre_usuario, dominio_completo = partes
    dominio_partes = dominio_completo.split('.')
    
    # Validar nombre de usuario
    caracteres_validos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    if nombre_usuario[0] == '.' or nombre_usuario[-1] == '.' or '..' in nombre_usuario:
        return False
    
    for i in range(len(nombre_usuario)):
        if nombre_usuario[i] not in caracteres_validos:
            return False
        if nombre_usuario[i] in "._-" and (i == len(nombre_usuario) - 1 or nombre_usuario[i + 1] in "._-"):
            return False
    
    # Validar dominio
    if len(dominio_partes) < 2:
        return False
    
    for parte in dominio_partes:
        if not parte or parte[0] == '-' or parte[-1] == '-' or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in parte):
            return False
    # Validar extensión
    extension = dominio_partes[-1]
    if len(extension) < 2:
        return False
    
    return True


def validar_telefono(telefono:str) -> bool:
    """Comprueba si un teléfono es válido."""
    if len(telefono) == 9:
        return telefono.isdigit()
    return False

def validar_matricula(matricula:str, tipo_vehiculo:str) -> bool:
    """Comprueba si una matrícula es válida."""
    # Formato de matrícula actual (desde el 2000): 4 números, 3 letras para turismos, furgonetas, motos y camiones
    matricula = matricula.replace(" ", "").upper()
    matricula = matricula.replace("-", "")
    LETRAS_VALIDAS = "BCDFGHJKLMNPRSTVWXYZ"
    if tipo_vehiculo in ["Turismo", "Furgoneta", "Moto", "Camión"]:
        if len(matricula) == 7 and matricula[:4].isdigit() and matricula[4:].isalpha():
            if all(letra in LETRAS_VALIDAS for letra in matricula[4:]):
                return True
        
        # Formato de matrícula antigua (hasta el 2000): 1-2 letras, hasta 4 números, 1-2 letras finales
        partes = matricula[:2], matricula[2:6], matricula[6:]
        prefijo, numeros, sufijo = partes
        if (1 <= len(prefijo) <= 2 and prefijo.isalpha() and
            1 <= len(numeros) <= 4 and numeros.isdigit() and
            1 <= len(sufijo) <= 2 and sufijo.isalpha()):
            return True
    # Formato de matrícula para ciclomotores: C + 1 número + 4 números + 2 letras
    elif tipo_vehiculo == "Ciclomotor":
        print("Ciclomotor", matricula)
        if len(matricula) != 8:
            return False
        
        if not matricula[0] == 'C' or not matricula[1].isdigit():
            return False
        
        if not(matricula[2:5].isdigit() and all(letra in LETRAS_VALIDAS for letra in matricula[5:])):
            return False
        
        return True
    return False

def validar_carnet_conducir(tipos_carnet:str, tipo_vehiculo:str) -> bool:
    """Comprueba si un carnet de conducir es válido para un tipo de coche.
    tipos_carnet: Cadena con los tipos de carnet separados por comas o espacios.
    Opciones válidas: AM, A1, A2, A, B, B+E, C1, C1+E, C, C+E
    tipo_coche: Tipo de coche a comprobar (Ciclomotor, Moto, Turismo, Furgoneta, Camión)
    """
    TIPOS_VALIDOS = {
        "Ciclomotor": {"AM"},
        "Moto": {"A1", "A2", "A"},
        "Turismo": {"B", "B+E"},
        "Furgoneta": {"B", "B+E"},
        "Camión": {"C1", "C1+E", "C", "C+E"}
    }
    
    # Aquí separamos los carnets por espacios y comas
    tipos_carnet = " ".join(tipos_carnet.replace(",", " ").split()).split()

    # Comprobamos si alguno de los carnets es válido para el tipo de coche    
    for carnet in tipos_carnet:
        if carnet in TIPOS_VALIDOS[tipo_vehiculo]:
            return True

    # Si no se ha encontrado ningún carnet válido
    return False

def fecha_actual() -> str:
    """Devuelve la fecha actual en formato aaaa/mm/dd."""
    return datetime.datetime.now().strftime("%Y/%m/%d")

def limpiar_pantalla() -> None:
    """Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")

# Ajustes de fechas
AÑO_LIMITE_SUPERIOR = 2100
AÑO_LIMITE_INFERIOR = 1900
