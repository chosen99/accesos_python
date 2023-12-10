import json
import requests
import sqlite3
from pytictoc import TicToc


con = sqlite3.connect("caeta")
cur = con.cursor()
cur.execute("DELETE FROM alumnos")
con.commit()

params = {'key': 'get_alumnos'}
res = requests.post('https://reconstruccioncae.grupoipmexico.com/api/api.php', params)
items = json.loads(res.content)

print('Comienza conteo insercion')
t = TicToc()
t.tic()
for sec in items:
    sql = "INSERT INTO alumnos (Codigo, CodigoStick, CodigoKey, Nombre, AP, AM, Grupo, Foto, Semestre, Bloqueo, Push) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    val = (sec['Codigo'], sec['CodigoStick'], sec['CodigoKey'], sec['Nombre'], sec['AP'], sec['AM'], sec['Grupo'], sec['Foto'], sec['Semestre'], sec['Bloqueo'], sec['Push'])
    cur.execute(sql, val)
    con.commit()
t.toc()
con.close()