#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.resources import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..ventanaspy.V_CodigosCuentasBalanzaComprobacion import *
from ..globalModulesShare.documentos_json import*
from ..globalModulesShare.mensajes_alertas import *
from ..globalModulesShare.icono import *

class FuncionesBComprobacionContabilidad(QWidget):
    def __init__(self):
        super(FuncionesBComprobacionContabilidad, self).__init__()
        self.variables = Variables()
        self.ui = Ui_Formulario_BusquedaCuetasCodigos_BalanzaComprobacion()
        self.ui.setupUi(self)
        self.setWindowTitle("Control de cuentas y codigos")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        
        self.ui.btn_btn_Guadar.clicked.connect(self.guardar)
        self.ui.btn_btn_Eliminar.clicked.connect(self.eliminar)
        self.ui.btn_btn_Actualizar.clicked.connect(self.actualizar)
        self.ui.btn_btn_CargarExcel.clicked.connect(self.cargar_excel)
        
        self.documento_json = creacion_json(self.variables.help_directory,self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, None).comprobar_existencia
        
    def guardar(self):
        cuenta = self.ui.txt_numcuenta.text().strip()
        codigo = self.ui.txt_codigo.text().strip()
        
        objeto = {
            'codigo' : codigo,
            'cuenta' : cuenta
        }
        
        creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, objeto).agregar_json
    
    def eliminar(self):
        pass
    
    def actualizar(self):
        pass
    
    def cargar_excel(self):
        pass