#importa modulos
import funciones_sql as f_sql
import funciones_main as f_main

if __name__ == '__main__':

    f_sql.create_database() # funcion que crea la base de datos

    hay_tickers, l_tickers = f_sql.check_tickers() # se consulta la base de datos, dentro de hay_tickers se guarda un booleano y l_tickers la lista de tickers existentes en la base

    key_api = 'HOzRroodgM7p6haWXE4GSZgtn5jhzZC2' # se hardcodea el key que se usa para la api, para futuras versiones se planea levantar la key desde api_plygon.txt para que el usuario pueda introducir su propia key

    while True:
        entrada = input('Introduzca un comando ("Info", "Pedir datos", "Resumen", "Tabla", "Graficar","Cerrar"): ').lower() #se pide comando a usario, llevando todo a minuscula para evitar errore de case sensitivity

        match entrada: # se usa la estructura match case con la entrada para decidir el outcome
            case "cerrar": # se cierra la aplicacion
                break

            case "info": # print simple donde se detalla que hace cada comando
                print('''\nPuede usar los siguientes comandos:\n
        Pedir Datos: Se introduce la acción y las fechas que se quiere consultar y se guarda la información en una base de datos.\n
        Resumen: Devuelve información de los datos existentes dentro de la base de datos.\n
        Tabla: Se introduce el ticker de una acción y devuelve la información de la acción en formato tabla.\n
        Graficar: Se introduce el ticker de una acción y grafica los datos de la misma que existan en la base de datos.\n 
        Cerrar: Cierra la aplicación.
                    ''')
        
            case "pedir datos": # entra en el bloque de pedir datos a la api de polygon
                tick = input("Escriba el ticker a buscar (ejemplo: AAPL): ").upper() #para el tick tambien se usa un metodo de string en este caso para transformar todo a mayuscula, ya que es necesario para interactuar con la api
                desde = input("Escriba la fecha inicial a buscar (formato YYYY-MM-DD): ")
                hasta = input("Escriba la fecha final a buscar (formato YYYY-MM-DD): ")  
                
                print('Pidiendo datos...\n') #print de estatus del programa
                
                dicc = f_main.get_stock_prices(tick,desde,hasta,key_api) # se guarda en un diccionario el json resultante del request a la api
                df_request = f_main.clean_request(dicc) #se guarda en un dataframe los datos transformados desde el diccionario anterior

                f_sql.temp_table(df_request) # crea tabla temporaria en base para incluir los datos que se solicitaron
                df_comp = f_sql.compare() #compara datos nuevos con los que estan dentro de la base y guarda en un dataframe solo los datos que no se encuentran en la base

                f_sql.append_entries(df_comp) #escribe los datos nuevos en base de datos

                hay_tickers, l_tickers = f_sql.check_tickers() # se vuelve a correr la funcion check_tickers para actualizar el booleano y la lista de tickers
                print('Se guardaron los datos correctamente.\n') # print de estatus del programa

            case "resumen": # comando para imprimir el resumen de los ticker existentes en la base
                if hay_tickers: # aqui el booleano creado en la linea 9 o actualizado en la linea 44 hace que se entre en el codigo que imprimime el resumen o muestre un mensaje de error
                    print('\n')
                    f_sql.print_summary() # funcion que imprime el resumen de los tickers
                    print('\n')
                else: # si no hay ningun ticker en la base se imprime el mensaje que se debe usar primero el comando para pedir datos a la api
                    print('\nTodavía no se guardaron datos dentro de la base de datos.\nUse el comando "Pedir datos" para empezar a agregar datos que pueda visualizar\n')

            case "tabla": # comando para imprimir una tabla con los datos del ticker solicitado
                if hay_tickers: # aqui el booleano creado en la linea 9 o actualizado en la linea 44 hace que se entre en el codigo que imprimime la tabla o muestre un mensaje de error
                    tick_v = input('Ingrese el ticker a consultar:').upper() # se pide el ticker, tambien llevando a mayuscula
                    if tick_v in l_tickers:                                  # se chequea si el ticker existe en la base
                        print(f'\nLos datos de {tick_v} son los siguientes:\n') 

                        print(f_sql.query_ticker(tick_v)) # si existe, se imprime la tabla con los datos presentes en la base de datos
                    else:                                 # si no existe, se imprime un mensaje que se debe pedir datos del ticker solicitado 
                        print('\nEl ticker solicitado no se encuentra en la base de datos, solicite los datos con el comando "Pedir datos"\n')
                else:     # si no hay ningun ticker en la base se imprime el mensaje que se debe usar primero el comando para pedir datos a la api
                    print('\nTodavía no se guardaron datos dentro de la base de datos.\nUse el comando "Pedir datos" para empezar a agregar datos que pueda visualizar\n')           
                
            case "graficar":
                if hay_tickers: # aqui el booleano creado en la linea 9 o actualizado en la linea 44 hace que se entre en el codigo que grafica o muestre un mensaje de error
                    tick_v = input('Ingrese el ticker a graficar: ').upper() # se pide el ticker, tambien llevando a mayuscula
                    if tick_v in l_tickers:   # se chequea si el ticker existe en la base
                        
                        df_viz = f_sql.query_ticker(tick_v) # si existe, se grafican los datos presentes en la base de datos
                        
                        f_main.visualize_df(df_viz,tick_v)  # si existe, se grafican los datos presentes en la base de datos
                    else:                                   # si no existe, se imprime un mensaje que se debe pedir datos del ticker solicitado 
                        print('\nEl ticker solicitado no se encuentra en la base de datos, solicite los datos con el comando "Pedir datos"\n')

                else: # si no hay ningun ticker en la base se imprime el mensaje que se debe usar primero el comando para pedir datos a la api
                    print('\nTodavía no se guardaron datos dentro de la base de datos.\nUse el comando "Pedir datos" para empezar a agregar datos que pueda visualizar\n')
            
            case default: # en el caso de que el usuario introduzca un comando no aceptado, se imprime un mensaje que vuelve a detallar los unicos comandos aceptados
                print('No es un comando aceptado - debe ser "Info", "Pedir datos", "Resumen", "Tabla", "Graficar","Cerrar".\n')