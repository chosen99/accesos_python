import sys
import PyQt5.QtCore
from PyQt5 import QtWidgets, Qt


app = QtWidgets.QApplication(sys.argv)
ventana = QtWidgets.QWidget()
# ventana.setWindowFlag(PyQt5.QtCore.Qt.FramelessWindowHint)

ventana.show()
sys.exit(app.exec_())
