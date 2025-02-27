#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ 
#########################
import sys
import os
from datetime import datetime
# from  .globalModulesShare.resources import *
from  .globalModulesShare.icono import *
from PyQt6 import  *
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QPixmap
# comment importamos concesionarios
from  .KenworthEste.Home_KWESTE import *
from  .KenworthEste.HomeContabilidad import *
#-----------
from  .globalModulesShare.ContenedorVariables import Variables
from  .ventanaspy.VPrincipal import Ui_VPrincipal 
from .globalModulesShare.documentos_json import creacion_json

class PrincipalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.ui = Ui_VPrincipal()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("Menu de Sucursales")
        # self.ui.centralwidget.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.ui.imgPrincipalMenu.setPixmap(QPixmap(":/Source/logo_analytics.png"))
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.btc_btc_cerrar.setIcon(QIcon(":Source/Icon_Close.png"))
        self.ui.btc_btc_minimizar.setIcon(QIcon(":Source/Icon_Minimize.png")) 
        self.ui.panel_encabezado.setStyleSheet("margin-top:5px;")
        
        self.ui.btn_btn_kweste.clicked.connect(self.abrirkweste)
        self.ui.btn_btn_ContabilidadKWESTE.clicked.connect(self.contabilidad_kweste)
        self.ui.btc_btc_cerrar.clicked.connect(self.cerrar)
        self.ui.btc_btc_minimizar.clicked.connect(self.minimizar)

        if not os.path.exists(Variables().help_directory):
            os.makedirs(Variables().help_directory, exist_ok=True)
        else:
            pass
        
    
    def cerrar(self):
        self.close()

    def abrirkweste(self):
        self.ventana = Home_KWESTE()
        self.ventana.show()
        
    def contabilidad_kweste(self):
        self.vUiContabilidad = VContabilidadKWESTE()
        self.vUiContabilidad.show()

    def minimizar(self):
        self.showMinimized()

    # EVENTOS DEL MOUSE
    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = PrincipalWindow()
    ventana_principal.show()
    sys.exit(app.exec())
