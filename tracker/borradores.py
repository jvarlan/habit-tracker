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
