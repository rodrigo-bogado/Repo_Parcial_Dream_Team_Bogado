'''
Primer Parcial - Dream Team
Alumno: Rodrigo Efraín Bogado Duarte
Div: E
'''
import os
import re
import json
import csv

########## FUNCIONES UTILITARIAS ##############

def leer_archivo() -> list:
    '''
    Usa el comando open() para abrir el archivo 'dt.json'
    en modo lectura y copia el contenido en un diccionario
    llamado 'diccionario_dream_team'. Luego Copia el contenido
    del key 'jugadores' en una lista llamada lista_jugadores
    '''

    ruta_archivo = r"C:\Users\Rod\Documents\Programación_entregas\Repo_Parcial_Dream_Team_Bogado\dt.json"
    
    with open(ruta_archivo, "r",encoding="utf-8") as dream_team_temp:
        diccionario_dream_team = json.load(dream_team_temp)

    lista_jugadores = diccionario_dream_team["jugadores"]

    return lista_jugadores

def solicitar_y_normalizar_seleccion() -> int:
    '''
    Solicita selección del menú.
    Guarda en la variable 'opcion'.
    Verifica que sea una opción válida con regex.
    En caso de serlo, normaliza la opción a integer.
    En caso contrario, se guarda "-1" en la variable.
    Retorna la variable 'opcion_normalizada' (int).
    '''

    opcion = input("\nIngrese opción: ")

    if re.search(r"[\d+]",opcion):
        opcion_normalizada = int(opcion)
    else:
        opcion_normalizada = -1

    return opcion_normalizada

def opcion_ingresada_incorrecta() -> bool:
    '''
    Solicita al usuario un caracter alfanumérico y retorna 'False' si 
    el caracter es 'x' o 'X' y retorna 'True' en caso contrario.
    Esta función se utiliza para para facilitar la navegación
    y evitar forzar al usuario a continuar si no lo desea.
    '''
    continuar_salir = input("\nLa opción ingresada no es válida.\n \nPresione ENTER para volver"
                            " a intentar o ingrese 'x' para volver al menú principal: ")
    if re.search(r"[xX]",continuar_salir):
        return False
    else:
        return True

def normalizar_texto(texto:str) -> str:
    '''
    Recibe un string 'texto' y reemplaza todos los guiones bajos "_"
    por espacios " " y capitaliza la primera letra del string.
    Retorna el string 'key_formateado_capitalizado' (str)
    '''

    key_formateado = re.sub("_"," ",texto)

    key_formateado_capitalizado = key_formateado.capitalize()

    return key_formateado_capitalizado

def guardar_archivo(nombre_archivo_guardar:str, contenido_a_copiar:str) -> bool:
    '''
    Guarda el contenido en un archivo CSV.

    Parametros:
        nombre_archivo_guardar (str): El nombre del archivo a guardar.
        contenido_a_copiar (str): El contenido a guardar en el archivo.

    Returns:
        bool: True si se guarda exitosamente, False si ocurre algún error.
    '''
    
    if os.path.isfile(nombre_archivo_guardar):
        mensaje_final = "\nSe sobreescribió el archivo {0}".format(nombre_archivo_guardar)
    else:
        mensaje_final = "\nSe creó el archivo {0}".format(nombre_archivo_guardar)

    lista_separada = contenido_a_copiar.split(",") # Convertir el string en una lista de líneas

    lista_separada_lineas = []

    for linea in lista_separada:

        linea_separada = linea.split(":") # Crear una lista de listas, donde cada lista contiene los elementos separados por ":"

        lista_separada_lineas.append(linea_separada)

    with open(nombre_archivo_guardar, "w+",newline="") as archivo:
        archivo_temporal = csv.writer(archivo)
        archivo_temporal.writerows(lista_separada_lineas)

    if os.path.isfile(nombre_archivo_guardar):
        print(mensaje_final)
        return True
    else:
        print("\nError al crear el archivo {0}".format(nombre_archivo_guardar))
        return False

def buscar_nombres_similares(nombre_ingresado:str, lista_jugadores:list) -> dict: 
    '''
    Recibe un string llamado nombre_ingresado y la lista_jugadores (list)
    Crea una lista_coincidencias (dict) y una variable vacía llamada
    indice_jugador_encontrado.
    Itera la 'lista_jugadores' con un FOR hasta encontrar con re.search()
    los valores de "nombre" que tengan similitudes con el valor de
    'nombre_ingresado' y los guarda junto a su respectivo número de índice
    en la 'lista_coincidencias' (key: Indice, Value: Nombre).
    Retorna nombre/s en 'diccionario_jugador_encontrado' (dict).
    Si no encuentra coincidencias retorna diccionario vacío.
    '''

    lista_coincidencias = {}

    for indice in range(0,len(lista_jugadores),1): # Itera lista desde 0

        nombre_jugador = lista_jugadores[indice]["nombre"] # Copia nombre en nombre_jugador

        if re.search(nombre_ingresado, nombre_jugador, re.IGNORECASE): # Compara nombre_jugador con nombre_ingresado

            lista_coincidencias[indice] = nombre_jugador # Si hay coincidencia se guarda en la lista_coincidencias

    if len(lista_coincidencias) == 1: # Si hay UNA sola coincidencia la muestra directamente

        os.system("cls")

        for indice,_ in lista_coincidencias.items():

            diccionario_jugador_encontrado = lista_jugadores[indice]

            return diccionario_jugador_encontrado # Retorna diccionario de jugador encontrado
        
    elif len(lista_coincidencias) > 1: # Si hay MAS de una coincidencia:

        while True: # Inicia bucle y sale únicamente cuando se especifica un jugador en base a su índice, reinicia bucle en caso contrario.

            os.system("cls")

            for indice,nombre in lista_coincidencias.items(): 

                print("{0}: {1}".format(indice,nombre)) # Muestra nombres similares encontrados junto a su nro. de índice

            print("\nMúltiples coincidencias encontradas. Ingrese índice del jugador buscado.\n")

            opcion_ingresada = solicitar_y_normalizar_seleccion() # Solicita numero de indice al usuario

            if opcion_ingresada in lista_coincidencias: # Si es válido sale del while
                os.system("cls")
                break
            elif opcion_ingresada_incorrecta(): # Si es inválido y decide volver a intentar reinicia el bucle
                continue
            else:
                app_dream_team(lista_jugadores) # Si el usuario decide salir vuelve al menú principal

        for indice,nombre in lista_coincidencias.items():

            if opcion_ingresada == indice: # Encuentra el índice ingresado en la lista de coincidencias

                diccionario_jugador_encontrado = lista_jugadores[indice] # Guarda todos los datos del jugador en diccionario

                return diccionario_jugador_encontrado # Retorna diccionario de jugador encontrado
            
    else: # Si no hay ninguna coincidencia se notifica al usuario y se le permite volver a intentar o volver al menú principal

        continuar_salir = input("\nNo se encontraron coincidencias.\n"
                                "Presione ENTER para volver a intentar o ingrese 'x' para volver al menú principal: ")
        
        if re.match(r"[xX]",continuar_salir):

            app_dream_team(lista_jugadores)
        else:

            diccionario_jugador_encontrado = {}

            return diccionario_jugador_encontrado # Retorna diccionario vacío

def ordenar_por_estadisticas(lista_original:list,key:str,estadistica:str,asc_desc:bool) -> list:
    '''
    Esta función recibe una lista, un atributo (altura, peso, etc)
    y un booleano que representa ascendente (True) y descendente (False)
    Utiliza el algoritmo 'quicksort' para iterar el atributo especificado
    en la lista y ordernarlo según el valor de de asc_desc.
    Retorna la lista ordenada en 'lista_ordenada' (list).
    '''

    lista_derecha = []

    lista_izquierda = []


    
    if len(lista_original) <= 1: # Verifica lista armada o vacía

        return lista_original
    
    else:

        pivot = lista_original[0] # El pivot siempre es el primer valor

        for jugador in lista_original[1:]: #Itera la lista a partir del segundo índice

             #Guarda el valor para usar de pivot

            if key == "estadisticas":

                pivot_valor = pivot["estadisticas"][estadistica]

                valor_a_comparar = jugador["estadisticas"][estadistica]

            else:

                pivot_valor = pivot[key]

                valor_a_comparar = jugador[key]

            if asc_desc == True: # Verifica si asc_desc es True (Ascendente) o False (Descendente)

                if pivot_valor < valor_a_comparar: 
                    lista_derecha.append(jugador)   # Mayor al pivot -> lista izquierda
                else:
                    lista_izquierda.append(jugador) # Menor/igual al pivot -> lista derecha

            else: 

                if pivot_valor > valor_a_comparar: 
                    lista_derecha.append(jugador)   # Menor al pivot -> lista izquierda
                else:
                    lista_izquierda.append(jugador) # Mayor/igual al pivot -> lista derecha

    # Función recursiva para ordenar lista izquierda
    lista_izquierda_ordenada = ordenar_por_estadisticas(lista_izquierda,key,estadistica,asc_desc)

    # Función recursiva para ordenar lista izquierda
    lista_derecha_ordenada = ordenar_por_estadisticas(lista_derecha,key,estadistica,asc_desc)

    # Se concatenan las tres listas en "lista_ordenada"
    lista_ordenada = lista_izquierda_ordenada + [pivot] + lista_derecha_ordenada

    return lista_ordenada

def calcular_promedio_estadisticas(lista_jugadores:list,estadistica:str) -> float:
    '''
    Calcula el promedio de una estadística específica de la lista_jugadores.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        estadistica (str): La estadística para la cual se desea calcular el promedio.

    Returns:
        float: El promedio de la estadística para los jugadores en 'promedio'.
    '''

    suma_total = 0

    cantidad_total = len(lista_jugadores)

    for jugador in lista_jugadores:
        suma_total += jugador["estadisticas"][estadistica]

    promedio = float(suma_total) / float(cantidad_total)

    return promedio

def estadisticas_mayores_a_n(lista_jugadores:list,key:str,estadistica:str,asc_desc:bool) -> list:
    '''
    Devuelve una lista de jugadores cuya estadística específicada es mayor o igual a un valor de referencia.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        key (str): La clave del diccionario para ordenar los jugadores.
        estadistica (str): La estadística específica para comparar con el valor de referencia.
        asc_desc (str): El orden ascendente o descendente para ordenar la lista de jugadores.

    Returns:
        list: Una 'lista_estadisticas' de jugadores cuya estadística es mayor o igual al valor de referencia.
    '''

    os.system("cls")

    lista_original = []

    lista_estadisticas = []

    flag = True

    for jugador in lista_jugadores:

        lista_original.append(jugador)

    while True:

        estadistica_referencia = input("\nIngrese valor de referencia: ")

        if estadistica_referencia == "" or estadistica_referencia.isalpha():
            if opcion_ingresada_incorrecta():
                continue
            else:
                app_dream_team(lista_jugadores)
        else:
            estadistica_referencia = float(estadistica_referencia)
            break

    lista_ordenada = ordenar_por_estadisticas(lista_original,key,estadistica,asc_desc)

    if "porcentaje" in estadistica:
        final_mensaje = "%"
    else:
        final_mensaje = ""

    for jugador in lista_ordenada:

        estadisticas_jugador = jugador["estadisticas"][estadistica]

        nombre_jugador = jugador["nombre"]

        if estadisticas_jugador >= estadistica_referencia:

            lista_estadisticas.append("{0}: {1}{2}".format(nombre_jugador,estadisticas_jugador,final_mensaje))

    return lista_estadisticas

def mostrar_estadisticas_asc_desc(lista_jugadores:list,key:str,estadistica:str,asc_desc:bool): 
    '''
    Muestra las estadísticas de los jugadores en orden ascendente o descendente.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        key (str): La clave del diccionario para ordenar los jugadores.
        estadistica (str): La estadística específica a mostrar.
        asc_desc (str): El orden ascendente o descendente para mostrar las estadísticas.

    Returns:
        Muestra la información (nombres y estadisticas) directamente.
    '''

    lista_original = []

    for jugador in lista_jugadores:

        lista_original.append(jugador)

    lista_ordenada = ordenar_por_estadisticas(lista_original,key,estadistica,asc_desc)

    atributo_formateado = normalizar_texto(texto=estadistica)

    print("\nNombre | {0}\n".format(atributo_formateado))

    for jugador in lista_ordenada:

        nombre_jugador = jugador["nombre"]

        estadistica_a_mostrar = jugador["estadisticas"][estadistica]

        print("{0}: {1}".format(nombre_jugador,estadistica_a_mostrar))

def buscar_min_max_estadistica(lista_jugadores:list,estadistica:str,min_max) -> list:
    '''
    Busca el valor mínimo o máximo de una estadística específica en la lista de jugadores.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        estadistica (str): La estadística específica para buscar el valor mínimo o máximo.
        min_max (str): El tipo de búsqueda, puede ser "menor" o "mayor".

    Returns:
        list: Una'lista_valor_nombres_min_max'que contiene el valor mínimo o máximo 
        de la estadística y los nombres de los jugadores correspondientes.
    '''

    valor_min_max = None
    lista_valor_nombres_min_max = []
    flag_primera_vuelta = True

            
    for jugador in lista_jugadores: # Guarda como referencia la estadistica y el nombre en cada iteracion

        estadistica_jugador = float(jugador["estadisticas"][estadistica]) 

        nombre_jugador = jugador["nombre"]

        if min_max == "menor": # Busca el valor mas bajo

            if flag_primera_vuelta == True or estadistica_jugador < float(valor_min_max): # Verifica si es primera vuelta o compara si es menor
                                                                                          # al valor mas bajo encontrado hasta ahora
                valor_min_max = estadistica_jugador

                nombre_mayor = nombre_jugador

                flag_primera_vuelta = False # Siempre guarda el primer valor en la primera vuelta

        elif min_max == "mayor": # Busca el valor mas alto

                if flag_primera_vuelta == True or estadistica_jugador > float(valor_min_max):# Verifica si es primera vuelta o compara si es mayor
                                                                                             # al valor mas alto encontrado hasta ahora
                    valor_min_max = estadistica_jugador

                    nombre_mayor = nombre_jugador

                    flag_primera_vuelta = False # Siempre guarda el primer valor en la primera vuelta

    if valor_min_max.is_integer(): # Si es entero lo convierte de float a int

        valor_min_max = int(valor_min_max)

    lista_valor_nombres_min_max.append(valor_min_max) # Primero guarda el valor en la lista

    lista_valor_nombres_min_max.append(nombre_mayor) # Luego agrega el nombre en la lista

    for jugador in lista_jugadores: # Verifica que no haya más jugadores con el mismo valor para agregar a la lista

        estadistica_jugador = float(jugador["estadisticas"][estadistica])

        nombre_jugador = jugador["nombre"]

        if estadistica_jugador == valor_min_max and nombre_mayor != jugador["nombre"]: # Verifica que no se agregue el mismo nombre

            lista_valor_nombres_min_max.append(nombre_jugador) # Se agrega a la lista si tiene el mismo valor

    return lista_valor_nombres_min_max 

########## FUNCIONES PRINCIPALES ##############

def listar_jugadores_por_nombre_y_posicion(lista_jugadores:list): # 1
    '''
    Lista los jugadores por nombre y posición en orden ascendente.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.

    Returns:
        Muestra la lista de nombres y posiciones directamente
    '''

    os.system("cls")

    lista_original = lista_jugadores

    lista_ordenada = ordenar_por_estadisticas(lista_original,key="nombre",estadistica="",asc_desc=True)

    print("Selección de baloncesto de Estados Unidos 1992 'Dream Team'\n")

    print("Nombre - Posición\n")

    for jugador in lista_ordenada:
        nombre_jugador = jugador["nombre"]
        posicion_jugador = jugador["posicion"]
        print("{0} - {1}".format(nombre_jugador,posicion_jugador))

def mostrar_estadisticas_jugador_por_indice(lista_jugadores:list): # 2
    '''
    Muestra los jugadores y sus índices correspondientes.
    Luego utiliza la función solicitar_y_normalizar_seleccion() y guarda el dato ingresado por
    el usuario en 'indice_seleccionado' (int). 
    Verifica que sea una opción válida y guarda el contenido del key 'estadisticas' del jugador 
    correspondiente en 'estadisticas_jugador'.
    En caso de ingresar una opción incorrecta se usa la función opcion_ingresada_incorrecta()
    para que el usuario elija reintentar o volver al menú principal.
    Con la función normalizar_texto() se reemplazan los guiones por espacios y capitaliza 
    la primera letra del key. 
    Muestra en consola el nombre del jugador y a sus estadísticas.
    '''

    while True:
         
        os.system("cls")

        for indice in range(0,len(lista_jugadores),1):
            nombre_jugador = lista_jugadores[indice]["nombre"]
            print("{0} - {1}".format(indice,nombre_jugador))

        indice_seleccionado = solicitar_y_normalizar_seleccion()

        global buffer_indice_global

        buffer_indice_global = indice_seleccionado

        if indice_seleccionado >= 0 and indice_seleccionado < len(lista_jugadores):
            estadisticas_jugador =  lista_jugadores[indice_seleccionado]["estadisticas"]
            break
        else:
            if opcion_ingresada_incorrecta():
                continue
            else:
                app_dream_team(lista_jugadores)
    
    os.system("cls")

    nombre_jugador_seleccionado = lista_jugadores[indice_seleccionado]["nombre"]

    print("\nEstadísticas de {0}\n".format(nombre_jugador_seleccionado))    

    for key,value in estadisticas_jugador.items():
        key_formateado_capitalizado = normalizar_texto(texto=key)
        print("{0}: {1}".format(key_formateado_capitalizado,value))
    
def guardar_archivo_por_indice(lista_jugadores:list): # 3
    '''
    Busca el índice del último jugador visto en el punto 2 y guarda su información en un CSV. 
    Si no se eligió un índice previamente se notifica al usuario y se vuelve al menú.
    El archivo CSV contiene los siguientes campos: nombre, posición, temporadas, 
    puntos totales, promedio de puntos por partido, rebotes totales, promedio de 
    rebotes por partido, asistencias totales, promedio de asistencias por partido, 
    robos totales, bloqueos totales, porcentaje de tiros de campo, porcentaje de 
    tiros libres y porcentaje de tiros triples.
    Notifica si se guardó el archivo correctamente.
    '''

    os.system("cls")

    global buffer_indice_global

    if buffer_indice_global == None:

        print("\nPrimero debe seleccionar el jugador que desea guardar con la opción Nro. 2\n")

        input("Presione ENTER para continuar...")

        app_dream_team(lista_jugadores)

    nombre_personaje = ""

    nombre_personaje = lista_jugadores[buffer_indice_global]["nombre"]

    contenido_a_copiar = "Nombre:{0},".format(nombre_personaje)

    for estadistica,valor in lista_jugadores[buffer_indice_global]["estadisticas"].items():

        estadistica_formateada = normalizar_texto(texto=estadistica)

        contenido_a_copiar += "{0}:{1},".format(estadistica_formateada,valor)

    nombre_personaje_formateado = re.sub(" ","_",nombre_personaje)

    nombre_personaje_formateado = nombre_personaje_formateado.lower()

    nombre_archivo_guardar = "estadisticas_{0}.csv".format(nombre_personaje_formateado)

    opcion_guardar = input("\nEstá seguro de guardar las estadísticas del jugador {0} en un archivo .csv? (y/n): ".format(nombre_personaje))

    opcion_guardar = opcion_guardar.lower()

    match opcion_guardar:
        case "y":
            guardar_archivo(nombre_archivo_guardar, contenido_a_copiar)
        case "n":
            app_dream_team(lista_jugadores)
        case _:
            if opcion_ingresada_incorrecta(): # True: Reintentar, False: Salir
                guardar_archivo_por_indice(lista_jugadores)
            else:
                app_dream_team(lista_jugadores)

def buscar_logros_de_jugador_por_nombre(lista_jugadores:list): # 4
    '''
    Busca y muestra los logros de un jugador por su nombre.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.

    Returns:
        Muestra directamente lista con nombre y logros.
    '''

    os.system("cls")

    nombre_ingresado = input("\nIngrese nombre del jugador a buscar: ")

    if nombre_ingresado == "":
        if opcion_ingresada_incorrecta():
            buscar_logros_de_jugador_por_nombre(lista_jugadores)
        else:
            app_dream_team(lista_jugadores)

    diccionario_jugador_encontrado = buscar_nombres_similares(nombre_ingresado, lista_jugadores)

    if len(diccionario_jugador_encontrado) > 0:

        nombre_jugador_encontrado = diccionario_jugador_encontrado["nombre"]

        logros_jugador_encontrado = diccionario_jugador_encontrado["logros"]

        print("\nNombre: {0}\n \nLogros:\n".format(nombre_jugador_encontrado))

        for logros in logros_jugador_encontrado:
                        print("- {0}".format(logros))
    else:
        buscar_logros_de_jugador_por_nombre(lista_jugadores)

def mostrar_promedio_total_estadistica(lista_jugadores:list,key:str,estadistica:str,asc_desc): # 5
    '''
    Muestra las estadísticas de los jugadores ordenados y el promedio total de una estadística específica.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        key (str): La clave utilizada para ordenar la lista de jugadores.
        estadistica (str): La estadística específica para mostrar y calcular el promedio.
        asc_desc (bool): Indica si se muestra en orden ascendente o descendente. (opcional, valor predeterminado: True)

    Returns:
        Muestra directamente el promedio de la estadistica especificada.
    '''

    os.system("cls")
                
    mostrar_estadisticas_asc_desc(lista_jugadores,key,estadistica,asc_desc)

    promedio = calcular_promedio_estadisticas(lista_jugadores,estadistica)

    estadistica_formateada = normalizar_texto(texto=estadistica)

    print("\n{0} del equipo completo: {1}".format(estadistica_formateada,round(promedio,2)))

def buscar_miembro_salon_de_la_fama(lista_jugadores:list): # 6
    '''
    Busca si un jugador es miembro del Salón de la Fama del Baloncesto.
    Utiliza la función buscar_nombres_similares().

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.

    Returns:
        Muestra directamente si el jugador buscado se encuentra o no en el salón de la fama.

    '''

    os.system("cls")

    flag_miembro_encontrado = False

    patron_busqueda = "Miembro del Salon de la Fama del Baloncesto"

    diccionario_jugador_encontrado = {}

    nombre_ingresado = input("\nIngrese nombre a buscar: ")

    if nombre_ingresado == "" or nombre_ingresado.isnumeric(): # Verifica que se ingrese un nombre correcto
        if opcion_ingresada_incorrecta():
            buscar_logros_de_jugador_por_nombre(lista_jugadores)
        else:
            app_dream_team(lista_jugadores)

    diccionario_jugador_encontrado = buscar_nombres_similares(nombre_ingresado, lista_jugadores) # Busca los nombres similares

    if len(diccionario_jugador_encontrado) > 0: # Verifica que la lista de coincidencias no esté vacía

        nombre_jugador = diccionario_jugador_encontrado["nombre"]

        for logros in diccionario_jugador_encontrado["logros"]: # Busca en el diccionario de jugador si el patrón de búsqueda existe

            if logros == patron_busqueda:  

                print("El jugador {0} es miembro del Salon de la Fama del Baloncesto".format(nombre_jugador)) # Si existe lo notifica

                flag_miembro_encontrado = True # Flag que verifica si hubo coincidencia con el patrón de busqueda

        if flag_miembro_encontrado == False: # Si no hubo coincidencia se notifica al usuario

            print("El jugador {0} NO es miembro del Salon de la Fama del Baloncesto".format(nombre_jugador))

    else:
        buscar_miembro_salon_de_la_fama(lista_jugadores)
                
def jugador_con_mayor_menor_estadistica(lista_jugadores:list,estadistica:str,min_max:str): # 7 # 8 # 9 # 13 # 14 # 19
    '''
    Busca el jugador con la mayor o menor estadística específica.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        estadistica (str): La estadística para la cual se desea buscar el jugador.
        min_max (str): Indica si se busca el mayor ("mayor") o el menor ("menor") valor de la estadística.

    Returns:
        Muestra directamente el nombre del jugador, estadistica y valor de la estadistica mayor o menor.

    '''

    os.system("cls")
        
    lista_valor_nombres_min_max = buscar_min_max_estadistica(lista_jugadores,estadistica,min_max) # Busca valor min_max y nombre/s

    nombres_min_max = ""

    for i in range(0,len(lista_valor_nombres_min_max),1): # Itera todo el largo de la lista, sea cual sea

        if i == 0: # El primer valor siempre se guarda en 'valor_min_max'

            valor_min_max = lista_valor_nombres_min_max[i]

        elif i == 1: # El segundo valor de la lista es el nombre min_max, se concatena en 'nombres_min_max' (str)

            nombres_min_max += str(lista_valor_nombres_min_max[i])

        elif i == len(lista_valor_nombres_min_max) - 1: # En casi de haber dos o más nombres se separan los dos últimos con "y"

            nombres_min_max += " y " + str(lista_valor_nombres_min_max[i])

        elif i > 1: # En caso de haber tres o más nombres se separan los primeros con ","

            nombres_min_max += ", " + str(lista_valor_nombres_min_max[i])

    estadistica_formateada = re.sub("_"," ",estadistica) # se reemplazan los guiones de 'estadística' por por espacios 

    if re.search(r"promedio",estadistica): # Se formatea el texto según el tipo de estadística para que tenga sentido gramaticalmente
            
        estadistica_formateada = re.sub("promedio","promedio de",estadistica_formateada)

        final_texto = "."

    elif re.search(r"porcentaje",estadistica):

        estadistica_formateada = re.sub("porcentaje","porcentaje de",estadistica_formateada)

        final_texto = "%"

    else:

        estadistica_formateada = "cantidad de {0}".format(estadistica_formateada)

        final_texto = "."

    if len(lista_valor_nombres_min_max) > 2:

        comienzo_texto = "Los jugadores"

        es_son = "son"

    else:

        comienzo_texto = "El jugador"

        es_son = "es"

    # Finalmente se concatenan todas las variables formateadas en el mensaje final

    print("\n{0} con {1} {2} {3} {4} con {5}{6}".format(comienzo_texto,min_max,estadistica_formateada,es_son,nombres_min_max,valor_min_max,final_texto))

def buscar_jugadores_estadisticas_mayores_a_n(lista_jugadores:list,key:str,estadistica:str,asc_desc): # 10 # 11 # 12 # 15 # 18
    '''
    Busca jugadores cuya estadística especificada es mayor a un valor dado.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        key (str): Clave para ordenar la lista de jugadores.
        estadistica (str): La estadística para la cual se desea buscar los jugadores.
        asc_desc (bool, optional): Indica si la lista debe ordenarse en forma ascendente o descendente. Por defecto, es True (ascendente).

    Returns:
        Muestra directamente la lista de jugadores con valor mayor al especificado.
    '''

    lista_promedios = estadisticas_mayores_a_n(lista_jugadores,key,estadistica,asc_desc)

    estadistica_normalizada = normalizar_texto(texto=estadistica)

    if len(lista_promedios) == 0:
        print("\nNo hay jugadores con estadísticas mayores a la especificada.")
    else:

        print("\nNombre | {0}\n".format(estadistica_normalizada))

        for jugador in lista_promedios:

            print(jugador)

def promedio_total_estadistica_excluyendo_valor_menor(lista_jugadores:list,estadistica:str,min_max:str): # 16
    '''
    Calcula el promedio de una estadística específica para el equipo completo, excluyendo al jugador con el valor menor de esa estadística.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        estadistica (str): La estadística para la cual se desea calcular el promedio.
        min_max (str): Indica si se debe excluir el valor menor ("menor") o mayor ("mayor") de la estadística.

    Returns:
        Muestra directamente el promedio total del equipo excluyendo al jugador con menor valor.
    '''

    lista_valor_nombres_min_max = buscar_min_max_estadistica(lista_jugadores,estadistica,min_max)

    lista_jugadores_sin_menor = []

    jugador_excluido = ""

    for nombre in lista_valor_nombres_min_max[1:]:  

        jugador_excluido += nombre

    for jugador in lista_jugadores:

        if jugador["nombre"] not in lista_valor_nombres_min_max:

            lista_jugadores_sin_menor.append(jugador)

    promedio = calcular_promedio_estadisticas(lista_jugadores=lista_jugadores_sin_menor,estadistica=estadistica)

    print("\nPromedio de puntos por partido del equipo excluyendo al jugador "
                      "con menor cantidad de puntos por partido ({0}): {1}".format(jugador_excluido,round(promedio,2)))

def jugador_con_mas_logros(lista_jugadores:list): # 17
    '''
    Encuentra al jugador con la mayor cantidad de logros en la lista de jugadores.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.

    Returns:
        Muestra directamente al jugador con mas logros y la cantidad.
    '''

    os.system("cls")

    flag_primera_vuelta = True

    cantidad_logros_mayor = None

    for jugador in lista_jugadores:

        nombre_jugador = jugador["nombre"]

        cantidad_logros_jugador = len(jugador["logros"])

        if flag_primera_vuelta == True or cantidad_logros_jugador > cantidad_logros_mayor:

            nombre_jugador_mas_logros = nombre_jugador

            cantidad_logros_mayor = cantidad_logros_jugador

            flag_primera_vuelta = False

    print("\nEl jugador con mas logros es {0} con {1} logros en total.".format(nombre_jugador_mas_logros,cantidad_logros_mayor))

def ordenar_jugadores_estadisticas_mayores_a_n_por_posicion(lista_jugadores:list,key:str,estadistica:str,asc_desc): # 20
    '''
    Ordena y muestra los jugadores con estadísticas mayores a un valor específico, organizados por posición.

    Parametros:
        lista_jugadores (list): Lista de jugadores, donde cada jugador es un diccionario.
        key (str): Clave para ordenar los jugadores por posición.
        estadistica (str): Estadística a evaluar.
        asc_desc (bool): Indica si se debe ordenar de forma ascendente o descendente (True para ascendente, False para descendente). Por defecto, es True.

    Returns:
        Muestra la lista de jugadores ordenados por posición junto a los valores de estadistica mayores al especificado.
    '''

    lista_original = []

    for jugador in lista_jugadores:

        lista_original.append(jugador)

    lista_ordenada_posicion = ordenar_por_estadisticas(lista_original,key="posicion",estadistica="",asc_desc=True)

    lista_estadisticas_mayores_a_n  = estadisticas_mayores_a_n(lista_jugadores,key,estadistica,asc_desc)

    estadistica_formateada = normalizar_texto(texto=estadistica)

    if len(lista_estadisticas_mayores_a_n) == 0:
        print("\nNo hay jugadores con estadísticas mayores a la especificada.")
    else:

        print("\nPosicion | Nombre | {0}\n".format(estadistica_formateada))

        for jugador_posicion in lista_ordenada_posicion:

            nombre_posicion = jugador_posicion["nombre"]

            posicion = jugador_posicion["posicion"]

            for jugador_estadistica in lista_estadisticas_mayores_a_n:

                if nombre_posicion in jugador_estadistica:

                    print("{0} - {1}".format(posicion,jugador_estadistica))

def guardar_ranking_jugadores(lista_jugadores:list): # 23 Extra 0
    '''
    Guarda el ranking de jugadores en un archivo CSV y muestra el ranking en pantalla.

    Parámetros:
        - lista_jugadores (list): Lista de jugadores con su información.

    '''

    os.system("cls")

    lista_original = lista_jugadores

    lista_ordenada_puntos = ordenar_por_estadisticas(lista_original,key="estadisticas",estadistica="puntos_totales",asc_desc=False)
    lista_ordenada_rebotes = ordenar_por_estadisticas(lista_original,key="estadisticas",estadistica="rebotes_totales",asc_desc=False)
    lista_ordenada_asistencias = ordenar_por_estadisticas(lista_original,key="estadisticas",estadistica="asistencias_totales",asc_desc=False)
    lista_ordenada_robos = ordenar_por_estadisticas(lista_original,key="estadisticas",estadistica="robos_totales",asc_desc=False)

    lista_nombres_rank = []

    lista_nombres_rank_mostrar = []

    lista_nombres_rank.append("Jugador:Puntos:Rebotes:Asistencias:Robos")

    lista_nombres_rank_mostrar.append("\nJugador            Puntos Rebotes Asistencias Robos")

    for jugador in lista_jugadores:

        nombre_jugador = jugador["nombre"]

        for indice,nombre in enumerate(lista_ordenada_puntos):

            if nombre_jugador == nombre["nombre"]:

                rank_puntos = indice + 1

        for indice,nombre in enumerate(lista_ordenada_rebotes):

            if nombre_jugador == nombre["nombre"]:

                rank_rebotes = indice + 1
                
        for indice,nombre in enumerate(lista_ordenada_asistencias):

            if nombre_jugador == nombre["nombre"]:

                rank_asistencias = indice + 1

        for indice,nombre in enumerate(lista_ordenada_robos):

            if nombre_jugador == nombre["nombre"]:

                rank_robos = indice + 1

        lista_nombres_rank.append("{0}:{1}:{2}:{3}:{4}".format(nombre_jugador,rank_puntos,rank_rebotes,rank_asistencias,rank_robos))

        nombre_jugador_just = nombre_jugador.ljust(18," ")

        rank_puntos_just = str(rank_puntos).ljust(5," ")

        rank_rebotes_just = str(rank_rebotes).ljust(5," ")

        rank_asistencias_just = str(rank_asistencias).ljust(5," ")

        rank_robos_just = str(rank_robos).ljust(5," ")

        lista_nombres_rank_mostrar.append("{0}    {1} {2} {3} {4}".format(nombre_jugador_just,rank_puntos_just,rank_rebotes_just,rank_asistencias_just,rank_robos_just))

    contenido_a_copiar = ",".join(lista_nombres_rank)

    nombre_archivo_guardar = "ranking_dream_team.csv"

    for fila in lista_nombres_rank_mostrar:

        print(fila)

    guardar_archivo(nombre_archivo_guardar,contenido_a_copiar)

def cantidad_de_jugadores_por_posicion(lista_jugadores:list): # 24 Extra 1
    '''
    Recibe una lista de jugadores y muestra la cantidad de jugadores que hay por cada posición.

    Parámetros:
    - lista_jugadores (list): Lista de jugadores con sus respectivas posiciones.

    Return:
    - Muestra posiciones y cantidad de jugadores directamente.
    '''

    os.system("cls")

    set_posiciones = set()

    contador_posiciones = {}

    for jugador in lista_jugadores: # Se arma el set de posiciones

        posicion_jugador = jugador["posicion"]

        set_posiciones.add(posicion_jugador)
    
    for posicion in set_posiciones: # Se inicializa el diccionario con los datos del set y valores en 0

        contador_posiciones[posicion] = 0

    for jugador in lista_jugadores: # Se itera la lista de jugadores

        posicion_jugador = jugador["posicion"]
        
        contador_posiciones[posicion_jugador] += 1 # Se suma 1 a la posición que coincide con la del jugador

    print("\nPosición | Cantida de jugadores\n")

    for posicion,cantidad in contador_posiciones.items():

        print("{0}: {1}".format(posicion, cantidad))

def ordenar_jugadores_por_all_star(lista_jugadores:list): # 25 Extra 2
    '''
    Recibe lista de jugadores, ordena y muestra los jugadores según la cantidad de All-Stars que han obtenido.

    Parámetros:
    - lista_jugadores (list): Lista de jugadores con sus respectivos logros.

    Return:
    - Muestra lista de jugadores y la cantidad de All-Stars de forma descendente.
    '''

    os.system("cls")

    lista_jugadores_all_stars = []

    for jugador in lista_jugadores:

        diccionario_all_stars = {}

        nombre_jugador = jugador["nombre"]

        for logro in jugador["logros"]:

            if "All-Star" in logro:

                cantidad_all_star = re.findall(r"\d+",logro) # guarda un diccionario con el valor numerico encontrado

                diccionario_all_stars["nombre"] = nombre_jugador

                diccionario_all_stars["cantidad_all_stars"] = int(cantidad_all_star[0]) # guarda el valor numerico como string

                lista_jugadores_all_stars.append(diccionario_all_stars)

    lista_original = lista_jugadores_all_stars

    lista_ordenada = ordenar_por_estadisticas(lista_original,key="cantidad_all_stars",estadistica="",asc_desc=False)

    print("\nNombre | Cantidad de All-Stars\n")

    for jugador in lista_ordenada:

        print("{0}: {1}".format(jugador["nombre"],jugador["cantidad_all_stars"]))

def mostrar_mayores_estadisticas_con_nombre(lista_jugadores:list): # 26 Extra 3
    '''
    3. Determinar qué jugador tiene las mejores estadísticas en cada valor. 
    La salida por pantalla debe tener un formato similar a este:

    Mayor cantidad de temporadas: Karl Malone (19)
    Mayor cantidad de puntos totales: Karl Malon (36928)

    Recibe lista de jugadores y muestra las mayores estadísticas junto 
    con los nombres de los jugadores correspondientes.

    Parámetros:
    - lista_jugadores (list): Lista de jugadores con sus respectivas estadísticas.

    Return: 
    - Muestra lista de estadisticas junto al nombre del jugador sin ningun orden en particular.

    '''

    os.system("cls")

    lista_estadisticas = lista_jugadores[0]["estadisticas"]

    print("\nJugadores con mejores valores por estadística: \n")

    for estadistica,_ in lista_estadisticas.items():

        estadistica_formateada = re.sub("_"," ",estadistica)

        lista_valor_nombre_max = buscar_min_max_estadistica(lista_jugadores,estadistica,min_max="mayor")

        valor_max = lista_valor_nombre_max[0]

        nombres_max = lista_valor_nombre_max[1:]

        nombres_max_formateado = ""

        for i in range(0,len(nombres_max)):

            if i == 0:

                nombres_max_formateado += nombres_max[i]
            
            elif i > 0:

                nombres_max_formateado += ", " + str(nombres_max[i])

        if "promedio" in estadistica:

            comienzo_mensaje = "Mayor promedio de {0}".format(estadistica_formateada[9:])

        elif "porcentaje" in estadistica:

            comienzo_mensaje = "Mayor porcentaje de {0}".format(estadistica_formateada[11:])
        else:

            comienzo_mensaje = "Mayor cantidad de {0}".format(estadistica_formateada)

        print("{0}: {1} ({2})".format(comienzo_mensaje,nombres_max_formateado,valor_max))

def ordenar_jugadores_por_ranking_estadisticas(lista_jugadores:list):
    '''
    Ordena la lista de jugadores por ranking de estadísticas.

    Parámetros:
    - lista_jugadores (list): Lista de jugadores con sus respectivas estadísticas.

    Retorna:
    - lista_ordenada (list): Lista de jugadores ordenados por ranking de estadísticas.
    '''
    
    lista_original = lista_jugadores

    lista_ordenada = []

    for estadistica in lista_original[0]["estadisticas"]:

        lista_ordenada = ordenar_por_estadisticas(lista_original,key="estadisticas",estadistica=estadistica,asc_desc=False)

        for indice,jugador in enumerate(lista_ordenada):

            jugador["estadisticas"][estadistica] = indice + 1

    return lista_ordenada
   
def mostrar_jugador_con_mejores_estadisticas(lista_jugadores:list): # 27 Extra 4
    '''
    Recibe lista de jugadores y usa la función 'ordenar_jugadores_por_ranking_estadisticas()' 
    para buscar al jugador que lidera el ranking y muestra su nombre.
    Luego muestra ranking de estadísticas totales.
    '''

    os.system("cls")

    lista_ordenada = []

    lista_ranking_total = []

    lista_ordenada = ordenar_jugadores_por_ranking_estadisticas(lista_jugadores)

    for jugador in lista_ordenada:

        suma_estadisticas = 0

        diccionario_ranking = {}

        for _,valor in jugador["estadisticas"].items():

            valor_estadistica = int(valor)

            suma_estadisticas += valor_estadistica

        diccionario_ranking = {"Nombre":jugador["nombre"],"Rank":suma_estadisticas}

        lista_ranking_total.append(diccionario_ranking)

        diccionario_ranking.clear

    lista_ranking_total_ordenada = ordenar_por_estadisticas(lista_original=lista_ranking_total,key="Rank",estadistica="",asc_desc=True)

    flag_primera_vuelta = True

    rank_mayor = None
    
    for jugador in lista_ranking_total:

        nombre = jugador["Nombre"]

        rank = int(jugador["Rank"])

        if flag_primera_vuelta == True or rank < rank_mayor:

            rank_mayor = rank

            nombre_top_rank = nombre

            flag_primera_vuelta = False

    print("\nEl jugador con mejores estadísticas es {0} liderando el ranking de estadísticas totales:\n".format(nombre_top_rank))

    for indice,jugador in enumerate(lista_ranking_total_ordenada):

        print("{0} - {1}".format(indice+1, jugador["Nombre"]))
    
def mostrar_menu():
    '''
    Limpia la consola y muestra el menú de selección.
    '''
    os.system("cls")

    menu = ("\nMenu principal:\n"
            "\n1. Mostrar la lista de todos los jugadores del Dream Team y sus posiciones\n"
            "2. Mostrar estadisticas de un jugador por índice.\n"
            "3. Guardar estadísticas de último jugador accedido.\n"
            "4. Buscar logros de jugador por nombre\n"
            "5. Mostrar promedio de puntos por partido del equipo en forma ascendente. \n"
            "6. Buscar miembro del Salón de la Fama del Baloncesto por nombre.\n"
            "7. Mostrar jugador con la mayor cantidad de rebotes totales.\n"
            "8. Mostrar jugador con el mayor porcentaje de tiros de campo.\n"
            "9. Mostrar jugador con la mayor cantidad de asistencias totales.\n"
            "10. Buscar jugadores con promedio de puntos por partido mayor a X.\n"
            "11. Buscar jugadores con rebotes totales por partido mayor a X.\n"
            "12. Buscar jugadores con promedio de asistencias por partido mayor a X.\n"
            "13. Mostrar el jugador con la mayor cantidad de robos totales.\n"
            "14. Mostrar el jugador con la mayor cantidad de bloqueos totales.\n"
            "15. Buscar jugadores con porcentaje de tiros libres mayor a X.\n"
            "16. Mostrar el promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido.\n"
            "17. Mostrar el jugador con la mayor cantidad de logros obtenidos\n"
            "18. Buscar jugadores con porcentaje de tiros triples mayor a X.\n"
            "19. Mostrar el jugador con la mayor cantidad de temporadas jugadas\n"
            "20. Buscar jugadores con porcentaje de tiros de campo mayor a X ordenados por posición.\n"
            "23. Bonus: Mostrar ranking de jugadores por estadisticas en y guardar en archivo csv.\n"
            "24. Bonus: Mostrar cantidad de jugadores en cada posición\n"
            "25. Bonus: Ordenar jugadores por número de 'All-Star' de forma descendente\n"
            "26. Bonus: Mostrar jugador con mayor valor por estadística \n"
            "27. Bonus: Mostrar jugador con las mejores estadísticas de todos\n"
            "0. Salir \n")
    
    return menu

def app_dream_team(lista_jugadores:list):
    '''
    Función principal del programa.
    Inicia un bucle con salida opcional ("0" en menú principal).
    Mestra el menú con la función mostrar_menu().
    Solicita selección del menú con solicitar_y_normalizar_seleccion()
    Se hace la validación y normalización de la opción seleccionada.
    Se ejecutan las funciones del menú en base a la selección realizada. 
    '''

    while True:

        os.system("cls")
        
        print(mostrar_menu())

        opcion_normalizada = solicitar_y_normalizar_seleccion()

        match opcion_normalizada:
            case 1: # Mostrar lista completa de jugadores.

                listar_jugadores_por_nombre_y_posicion(lista_jugadores)
                
                input("\nPresione ENTER para continuar...")
                continue
            case 2: # Mostrar estadisticas de un jugador por índice.
                
                mostrar_estadisticas_jugador_por_indice(lista_jugadores)
                
                input("\nPresione ENTER para continuar...")
                continue
            case 3: # Guardar estadísticas de último jugador accedido.

                guardar_archivo_por_indice(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue
            case 4: # Buscar logros de jugador por nombre.
                
                buscar_logros_de_jugador_por_nombre(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue
            case 5: # Mostrar promedio de puntos por partido de forma ascendente.
                
                mostrar_promedio_total_estadistica(lista_jugadores,key="estadisticas",estadistica="promedio_puntos_por_partido",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 6: # Buscar miembro del Salón de la Fama del Baloncesto por nombre.
    
                buscar_miembro_salon_de_la_fama(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue
            case 7: # Mostrar jugador con la mayor cantidad de rebotes totales.

                jugador_con_mayor_menor_estadistica(lista_jugadores,estadistica="rebotes_totales",min_max="mayor")

                input("\nPresione ENTER para continuar...")
                continue
            case 8: # Mostrar jugador con el mayor porcentaje de tiros de campo.

                jugador_con_mayor_menor_estadistica(lista_jugadores,estadistica="porcentaje_tiros_de_campo",min_max="mayor")

                input("\nPresione ENTER para continuar...")
                continue
            case 9: # Mostrar jugador con la mayor cantidad de asistencias totales.
                
                jugador_con_mayor_menor_estadistica(lista_jugadores,estadistica="asistencias_totales",min_max="mayor")

                input("\nPresione ENTER para continuar...")
                continue
            case 10: # Buscar jugadores con promedio de puntos por partido mayor a X.
                
                buscar_jugadores_estadisticas_mayores_a_n(lista_jugadores,key="estadisticas",estadistica="promedio_puntos_por_partido",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 11: # Buscar jugadores con rebotes totales por partido mayor a X.

                buscar_jugadores_estadisticas_mayores_a_n(lista_jugadores,key="estadisticas",estadistica="rebotes_totales",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 12: # Buscar jugadores con promedio de asistencias por partido mayor a X.
                
                buscar_jugadores_estadisticas_mayores_a_n(lista_jugadores,key="estadisticas",estadistica="promedio_asistencias_por_partido",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 13: # Calcular y mostrar el jugador con la mayor cantidad de robos totales.
                                
                jugador_con_mayor_menor_estadistica(lista_jugadores,estadistica="robos_totales",min_max="mayor")

                input("\nPresione ENTER para continuar...")
                continue     
            case 14: # Calcular y mostrar el jugador con la mayor cantidad de bloqueos totales.

                jugador_con_mayor_menor_estadistica(lista_jugadores,estadistica="bloqueos_totales",min_max="mayor")

                input("\nPresione ENTER para continuar...")
                continue        
            case 15: # Permitir al usuario ingresar un valor y mostrar los jugadores que hayan 
                     # tenido un porcentaje de tiros libres superior a ese valor.
            
                buscar_jugadores_estadisticas_mayores_a_n(lista_jugadores,key="estadisticas",estadistica="porcentaje_tiros_libres",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 16: # Calcular y mostrar el promedio de puntos por partido del equipo excluyendo al 
                     # jugador con la menor cantidad de puntos por partido.

                promedio_total_estadistica_excluyendo_valor_menor(lista_jugadores,estadistica="promedio_puntos_por_partido",min_max="menor")

                input("\nPresione ENTER para continuar...")
                continue
            case 17: # Calcular y mostrar el jugador con la mayor cantidad de logros obtenidos
                
                jugador_con_mas_logros(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue
            case 18: # Permitir al usuario ingresar un valor y mostrar los jugadores que hayan tenido 
                     # un porcentaje de tiros triples superior a ese valor.
                
                buscar_jugadores_estadisticas_mayores_a_n(lista_jugadores,key="estadisticas",estadistica="porcentaje_tiros_triples",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 19: # Calcular y mostrar el jugador con la mayor cantidad de temporadas jugadas
                
                jugador_con_mayor_menor_estadistica(lista_jugadores,estadistica="temporadas",min_max="mayor")              

                input("\nPresione ENTER para continuar...")
                continue
            case 20: # Permitir al usuario ingresar un valor y mostrar los jugadores , ordenados por posición 
                     # en la cancha, que hayan tenido un porcentaje de tiros de campo superior a ese valor.

                ordenar_jugadores_estadisticas_mayores_a_n_por_posicion(lista_jugadores,key="estadisticas",estadistica="porcentaje_tiros_de_campo",asc_desc=True)

                input("\nPresione ENTER para continuar...")
                continue
            case 23:

                guardar_ranking_jugadores(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue                
            case 24:

                cantidad_de_jugadores_por_posicion(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue                
            case 25:

                ordenar_jugadores_por_all_star(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue       
            case 26:

                mostrar_mayores_estadisticas_con_nombre(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue
            case 27:

                mostrar_jugador_con_mejores_estadisticas(lista_jugadores)

                input("\nPresione ENTER para continuar...")
                continue                
            case -1:

                input("\nOpción ingresada no es válida, presione ENTER para volver a intentar.")
                continue
            case 0:

                quit()
            case _:

                input("\nOpción ingresada no es válida, presione ENTER para volver a intentar.")
                continue

buffer_indice_global = None

lista_jugadores = leer_archivo()

os.system("cls")

app_dream_team(lista_jugadores)

