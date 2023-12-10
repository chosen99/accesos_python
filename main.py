import sys
import base64
import pyautogui
import PyQt5.QtCore
import requests
import json
import ctypes
import calendar
import datetime

from PyQt5 import QtWidgets, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout


def displaytime():
    # horario = PyQt5.QtCore.QTime.currentTime()
    fecha = PyQt5.QtCore.QDateTime.currentDateTime()
    displayText = fecha.toString('dddd d').upper() + ' de ' + fecha.toString('MMMM').upper() + ' de ' + fecha.toString(
        'yyyy hh:mm:ss')
    hora.setText(displayText)


def limpiar():
    timerl.stop()
    foto_alumno.clear()
    nombre_grupo.clear()

def bloquear(indice, items):
    # Se obtiene fecha en formato UNIX
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())
    # De la posicion encontrada comparamos el tiempo de bloqueo con el tiempo obtenido al leer la credebcial
    # si el tiempo obtenido actual es mayor regresamos "True" de lo contrario mandamos "False"
    if items[indice]['bloqueo'] <= utc_time:
        # Actualizamos el bloque de bloqueo para el alumno seleccionado y guradmaos informacion
        items[indice]['bloqueo'] = utc_time+600
        print(items[indice])
        # with open("alumnos.json", "w") as outfile:
        #     outfile.write(json.dumps(items, indent=4))
        # outfile.close()
        return True
    else:
        return False

def codigoM():
    global scaled, base64_img, verFoto, sets
    notificacion = False
    try:
        request = requests.get("https://www.google.com", timeout=80)
        if request.status_code == 200:
            notificacion = True
    except requests.RequestException as e:
        pass
    try:
        params = {'key': codigo.text()}
        res = requests.get('http://192.168.0.2/i.php', params, timeout=80)
        response = json.loads(res.text)
        if res.text == 'false':
            # if response is None:
            nombre_grupo.setText("Usuario no registration")
            base64_img = QPixmap("no_info.svg")
        elif response['Nombre'] == 'repetir':
            nombre_grupo.setText("Usuario repetido")
        else:
            nombre_grupo.setText("NOMBRE: " + response['AP'] + " " + response['AM'] + " " + response['Nombre'] +
                                 "\nGRUPO: " + response['Grupo'])
            if response['Foto'] is None:
                base64_img = QPixmap('error_pic.svg')
            else:
                base64_img = QPixmap()
                base64_img.loadFromData(base64.b64decode(response['Foto']))

            if notificacion:
                print("envia notificacion")
    except requests.RequestException:
        pass

    timerl.stop()
    timerl.start()
    codigo.clear()
    # ************************************************* DECOMENTAR *****************************************************

    # scaled = base64_img.scaled(foto_alumno.size(), Qt.Qt.KeepAspectRatio)
    # foto_alumno.setPixmap(scaled)
    # print(codigo.text())


app = QtWidgets.QApplication(sys.argv)
ventana = QtWidgets.QWidget()
ventana.setWindowFlag(PyQt5.QtCore.Qt.FramelessWindowHint)
width, height = pyautogui.size()
ventana.setGeometry(0, 0, width, height)
ventana.setStyleSheet("background-color: white;")
ventana.setWindowIcon(QIcon("repetir.svg"))
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Declaracion de tiempo para borrado de datos en pantalla
timerl = PyQt5.QtCore.QTimer(ventana)
timerl.setSingleShot(True)
timerl.setInterval(3000)
timerl.timeout.connect(limpiar)

# Carga config
with open('./cnf/configs.cnf') as archivo:
    lineas = archivo.readlines()
archivo.close()
variables = {}
for linea in lineas:
    clave, valor = linea.strip().split("=")
    variables[clave] = valor

# Creacion nombre planteles
planteles = variables['nombrecorto'] + '\n' + variables['nombrelargo']
escuela = QLabel(planteles, ventana)
escuela.setStyleSheet("""
        QLabel{
            font-size: 22px;
            color: rgb(201, 107, 6);
            font-weight: 900;
            background-color: rgb(255, 255, 255);
        }
        """)
escuela.setGeometry(0, 0, width, int((height * 10) / 100))
escuela.setAlignment(Qt.Qt.AlignCenter)

# Creacion estancia lentura codigo
ancho_columnas = int(width / 3)
# print(ancho_columnas, width)

# Matriculas
codigo = QLineEdit(ventana)
codigo.setStyleSheet("""
                QLineEdit{
                    color: rgb(255, 255, 255);
                    background-color: rgb(255, 255, 255);
                    border: none;
                }
                """)
codigo.setEchoMode(QLineEdit.EchoMode.NoEcho)
codigo.move(0, int((height * 10) / 100))
# editingFinished <- Fin de edicion de codigo, Cambio por Enter
codigo.returnPressed.connect(codigoM)

foto_alumno = QLabel('', ventana)
# Muestra foto alumno
foto_alumno.setStyleSheet("""
        QLabel{
            background-color: rgb(255, 255, 255);
        }
        """)
foto_alumno.setGeometry(int(ancho_columnas / 2), int((height * 10) / 100),
                        ancho_columnas * 2, int((height * 55) / 100))
foto_alumno.setAlignment(Qt.Qt.AlignCenter)

# Muestra nombre y grupo de alumno
nombre_grupo = QLabel('', ventana)
nombre_grupo.setStyleSheet("""
        QLabel{
            font-size: 22px;
            color: rgb(201, 107, 6);
            font-weight: 900;
            background-color: rgb(255, 255, 255);
        }
        """)
nombre_grupo.setGeometry(0, int((height * 65) / 100),
                         ancho_columnas * 3, int((height * 15) / 100))
nombre_grupo.setAlignment(Qt.Qt.AlignCenter)

# Barra hora
layout = QVBoxLayout()
hora = QLabel('', ventana)
hora.setStyleSheet("""
        QLabel{
            font-size: 22px;
            color: #ffffff;
            font-weight: 900;
            background-color: rgb(59, 82, 110);
        }
        """)
hora.setGeometry(0, int((height * 20) / 100) + int((height * 60) / 100), width, int((height * 10) / 100))
hora.setAlignment(Qt.Qt.AlignCenter)
layout.addWidget(hora)
# Identador Hora y Fecha
timer = PyQt5.QtCore.QTimer(ventana)
timer.timeout.connect(displaytime)
timer.start(1000)

# Pie de pagina
pie = QLabel('Imagenes', ventana)
pie.setStyleSheet("""
        QLabel{
            background-color: rgb(209, 183, 123);
        }
        """)
pie.setGeometry(0, int((height * 30) / 100) + int((height * 60) / 100) - 2, width, int((height * 10) / 100))
pie.setAlignment(Qt.Qt.AlignCenter)

ventana.show()
sys.exit(app.exec_())
