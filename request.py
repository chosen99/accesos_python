import requests
import json
# import sqlite3
# # Vaciar tabla
# con = sqlite3.connect("caeta")
# cur = con.cursor()
# cur.execute("DELETE FROM alumnos")
# con.commit()

params = {'key': 'get_alumnos'}
res = requests.post('https://reconstruccioncae.grupoipmexico.com/api/api.php', params)
with open("alumnos.json", "w") as outfile:
    outfile.write(json.dumps(json.loads(res.content), indent=4))
print('Se descargaron ' + str(len(json.loads(res.content))) + ' alumnos')


# for iterable in json_object:
#     i+=1
#     sql = "INSERT INTO alumnos (Nombre, AP, AM, Grupo, Foto, FecHora, Codigo) VALUES (?,?,?,?,?,?,?)"
#     val = (iterable['Nombre'], iterable['AP'], iterable['AM'], iterable['Grupo'], iterable['Foto'], "5", "6")
#     cur.execute(sql, val)
#     con.commit()
#     print(i)

#con.close()
