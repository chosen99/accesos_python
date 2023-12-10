with open('configs.cnf') as archivo:
    lineas = archivo.readlines()
archivo.close()

variables = {}
for linea in lineas:
    clave, valor = linea.strip().split("=")
    variables[clave] = valor
print(variables['server_ip'])
