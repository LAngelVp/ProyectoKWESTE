#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent, QStandardItemModel, QStandardItem
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
        self.mostrar_datos_cuentas()
        self.documento_json = creacion_json(self.variables.help_directory,self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, None).comprobar_existencia
        
    def guardar(self):
        cuenta = self.ui.txt_numcuenta.text().strip()
        codigo = self.ui.txt_codigo.text().strip()
        if cuenta != "" or codigo != "":
            objeto = {
                'codigo' : codigo,
                'cuenta' : cuenta
            }
            creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, objeto).agregar_json
            

        
        Mensajes_Alertas(
                    "Error",
                    f"Los campos no contienen información para almacenar.",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
    
    def eliminar(self):
        pass
    
    def actualizar(self):
        pass
    
    def cargar_excel(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivo Excel (*.xlsx *.xls)")
        if archivo:
            try:
                self.excel = pd.read_excel(archivo)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al cargar el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
            modelo_nuevos = QStandardItemModel()
            modelo_nuevos .setHorizontalHeaderLabels(self.excel.columns)
            for fila in self.excel.values:
                elementos = [QStandardItem(str(elemento)) for elemento in fila]
                modelo_nuevos.appendRow(elementos)
            self.ui.Tabla_DatosNuevos.setModel(modelo_nuevos)
            self.ui.Tabla_DatosNuevos.resizeColumnsToContents()
        else:
            print("NO SE CARGO EL ARCHIVO")
        return
    
    
    def mostrar_datos_cuentas(self):
        codigos = pd.read_json(self.variables.bcc_codigos_vs_cuentas)
        modelo_existentes = QStandardItemModel()
        modelo_existentes .setHorizontalHeaderLabels(codigos.columns)
        for fila in codigos.values:
            elementos = [QStandardItem(str(elemento)) for elemento in fila]
            modelo_existentes.appendRow(elementos)
        self.ui.Tabla_DatosExistentes.setModel(modelo_existentes)
        self.ui.Tabla_DatosExistentes.resizeColumnsToContents()
        
    def Aceptar_callback(self):
        pass