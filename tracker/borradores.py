 seguro = input(f"{ROJO}¿Quieres modificar el tipo de objetivo? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                while True:
                    tipo_valido = ["diario","semanal","mensual","anual"]
                    tipo_objetivo = input(f"Nuevo tipo (diario, semanal, mensual, anual): ")
                    tipo_objetivo = normalizar(tipo_objetivo)
                    if tipo_objetivo in tipo_valido:
                        contador +=1
                        break
                    else:
                        continue

            seguro = input(f"{ROJO}¿Quieres modificar el objetivo de horas? s/n: {RESET}")
            seguro = seguro.lower()
            
            if seguro in ("s","si"):
                while True:
                    objetivo_horas = input(f"Nuevo objetivo (HH:MM:SS): ")
                    if validar_horas(objetivo_horas):
                        contador +=1
                        break
                    else:
                        continue



def categorias_est(habitos, temporizadores, categorias):
    
        ahora = datetime.now()
        lineas = []
        
        for categoria in categorias:
            segundos_totales = 0
            for habito in habitos:
                if habito['id_categoria'] == categoria['id']:
                   # objetivo += int(habito['objetivo'])
                    for temporizador in temporizadores:
                        if temporizador['id_habito'] == habito['id']:
                            segundos_totales += horas_a_segundos(temporizador['tiempo'])

            # Icono de la categoría (💪, 🎮, 📖)
            
            emoticono_categoria = categoria['emoticono']
          
          #  try:
           #     porcentaje = (float(segundos_totales) / (float(objetivo)* 3600)) * 100
           # except ZeroDivisionError:
            #    porcentaje = 0
            linea = f"{emoticono_categoria} {categoria['categoria']} -> {numero_string_a_HHMM(segundos_totales)} horas"
            lineas.append(linea)

        return lineas
