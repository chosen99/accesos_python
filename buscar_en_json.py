import json
import calendar
import datetime
# print(items[0])
# items[0]['Nombre'] = 'prueba'
# print(items)
# Define a function to search the item
def search_code(codigos):
    with open('alumnos.json', 'r') as openfile:
        items = json.load(openfile)
    openfile.close()
    i=0
    # Leemos todos los items de json y comparamos el codigo con la posición codigo de cada item
    for keyval in items:
        # Si encuetra coincidencia con alguno de los 3 campos de acceso
        if codigos == keyval['Codigo'] or codigos == keyval['CodigoStick'] or codigos == keyval['CodigoKey']:
            # Verifica si tiene permitido el acceso (por bloqueo de 10 min)
            if bloquear(i, items):
                # Retorna la informacion completa del alumno en la posicion encontrada
                return keyval
            else:
                return 'bloqueado'
        i+=1

def bloquear(indice, items):
    # Se obtiene fecha en formato UNIX
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    # De la posicion encontrada comparamos el tiempo de bloqueo con el tiempo obtenido al leer la credebcial
    # si el tiempo obtenido actual es mayor regresamos "True" de lo contrario mandamos "False"
    if items[indice]['bloqueo'] <= utc_time:
        # Actualizamos el bloque de bloqueo para el alumno seleccionado y guradmaos informacion
        items[indice]['bloqueo'] = utc_time+600
        with open("alumnos.json", "w") as outfile:
            outfile.write(json.dumps(items, indent=4))
        outfile.close()
        return True
    else:
        return False
# Check the return value and print message
while True:
    # Input the item name that you want to search
    code = input("Enter an item name:\n")
    data = search_code(code)
    if data is not None:
        print(data)
    else:
        print("Item is not found")
