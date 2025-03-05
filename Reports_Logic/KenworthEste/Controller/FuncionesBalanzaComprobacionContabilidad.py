#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent, QStandardItemModel, QStandardItem, QRegularExpressionValidator
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRegularExpression
from PyQt6 import *
from ...globalModulesShare.resources import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...ventanaspy.V_CodigosCuentasBalanzaComprobacion import *
from ...globalModulesShare.documentos_json import*
from ...globalModulesShare.mensajes_alertas import *
from ...globalModulesShare.icono import *

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
        self.ui.btn_btn_LimpiarCampos.clicked.connect(self.limpiar)
        self.ui.btn_btn_buscar.clicked.connect(self.buscar)
        self.mostrar_datos_cuentas()
        self.documento_json = creacion_json(self.variables.help_directory,self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, None).comprobar_existencia
        
        #// VARIABLES GLOBALES
        self.excel = None
        self.id_elemento_eliminar = None
        # self.modelo_nuevos = None
        # self.modelo_existentes = None
        patron = r"^\d+(-\d+){3}$"
        
        regex = QRegularExpression(patron)
        validador = QRegularExpressionValidator(regex, self.ui.txt_numcuenta)
        self.ui.txt_numcuenta.setValidator(validador)
        
    def buscar(self):
        print(self.ui.cajaopciones_busca_cuenta_codigo.currentIndex())
        cuentas_existentes = pd.read_json(self.variables.bcc_codigos_vs_cuentas)
        dato_buscar = self.ui.txt_filtro.text().strip()
        if self.ui.cajaopciones_busca_cuenta_codigo.currentIndex() == 0:
            elemento_encontrado = cuentas_existentes[cuentas_existentes['Cuenta'] == dato_buscar]
            if not elemento_encontrado.empty:
                self.mostrar_datos_cuentas(elemento_encontrado)
            else:
                self.mostrar_datos_cuentas()
        elif self.ui.cajaopciones_busca_cuenta_codigo.currentIndex() == 1:
            elemento_encontrado = cuentas_existentes[cuentas_existentes['Codigo'] == dato_buscar]
            if not elemento_encontrado.empty:
                self.mostrar_datos_cuentas(elemento_encontrado)
            else:
                self.mostrar_datos_cuentas()
        
    def limpiar(self):
        self.ui.txt_codigo.clear()
        self.ui.txt_numcuenta.clear()
        self.ui.txt_filtro.clear()
        try:
            self.modelo_nuevos.clear()
        except:
            pass
        
    def guardar(self):
        cuenta = self.ui.txt_numcuenta.text().strip()
        codigo = self.ui.txt_codigo.text().strip()
        if self.ui.txt_numcuenta.hasAcceptableInput() and codigo != "":
            objeto = {
                'codigo' : codigo,
                'cuenta' : cuenta
            }
            creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, objeto).agregar_json
            
        if self.excel is not None:
            for fila in self.excel.values:
                objeto = {
                    'codigo' : str(fila[1]),
                    'cuenta' : str(fila[0])
                }
                creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, objeto).agregar_json
        else:
            Mensajes_Alertas(
                        "Error",
                        f"Los campos no contienen información para almacenar.",
                        QMessageBox.Icon.Warning,
                        None,
                        botones=[
                            ("Aceptar", self.Aceptar_callback)
                        ]
                    ).mostrar
        return
    
    def eliminar(self):
        if self.id_elemento_eliminar is None:
            Mensajes_Alertas(
                    "Eliminar",
                    f"Debes de seleccionar un elemento de la tabla de Datos Existentes para poder eliminar un registro.",
                    QMessageBox.Icon.Information,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
            return
        elemento_eliminar = {"id" : self.id_elemento_eliminar}
        creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, elemento_eliminar).eliminar_datos_json
        self.mostrar_datos_cuentas()
        return
    
    def actualizar(self):
        id = {"id" : self.id_elemento_eliminar}
        datos_anteriores = creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste,id).obtener_datos_json_por_id
        if datos_anteriores:
            if self.ui.txt_numcuenta.hasAcceptableInput():
                datos_nuevos = {
                    "id" : id["id"],
                    "Cuenta" : self.ui.txt_numcuenta.text().strip(),
                    "Codigo" : self.ui.txt_codigo.text().strip()
                }
                creacion_json(self.variables.help_directory, self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste,id).actualizar_datos(datos_nuevos)
                self.mostrar_datos_cuentas()
            else:
                Mensajes_Alertas(
                        "Error",
                        f"La cuenta debe cumplir con el estandar. x-x-x-x",
                        QMessageBox.Icon.Warning,
                        None,
                        botones=[
                            ("Aceptar", self.Aceptar_callback)
                        ]
                    ).mostrar
        return
    
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
            self.modelo_nuevos = QStandardItemModel()
            self.modelo_nuevos .setHorizontalHeaderLabels(self.excel.columns)
            for fila in self.excel.values:
                elementos = [QStandardItem(str(elemento)) for elemento in fila]
                self.modelo_nuevos.appendRow(elementos)
            self.ui.Tabla_DatosNuevos.setModel(self.modelo_nuevos)
        else:
            print("NO SE CARGO EL ARCHIVO")
            return
        return
    
    def mostrar_datos_cuentas(self, datos = None):
        if datos is not None:
            cunetas_existentes = datos
        else:
            cunetas_existentes = pd.read_json(self.variables.bcc_codigos_vs_cuentas)
        self.modelo_existentes = QStandardItemModel()
        self.modelo_existentes .setHorizontalHeaderLabels(cunetas_existentes.columns)
        for fila in cunetas_existentes.values:
            elementos = [QStandardItem(str(elemento)) for elemento in fila]
            self.modelo_existentes.appendRow(elementos)
        self.ui.Tabla_DatosExistentes.setModel(self.modelo_existentes)
        self.ui.Tabla_DatosExistentes.setColumnHidden(0, True)
        self.ui.Tabla_DatosExistentes.selectionModel().currentChanged.connect(self.obtenerIdEliminar)
        
    def obtenerIdEliminar(self, current, previus):
        if current.column() >= 0:
            indice_fila = current.row()
            self.id_elemento_eliminar = self.modelo_existentes.item(indice_fila, 0).text()
            cuenta = self.modelo_existentes.item(indice_fila, 1).text()
            codigo = self.modelo_existentes.item(indice_fila, 2).text()
            self.mostrar_datos_campos(cuenta, codigo)
    
    def mostrar_datos_campos(self, cuenta = None, codigo = None):
        self.ui.txt_numcuenta.setText(cuenta)
        self.ui.txt_codigo.setText(codigo)
        
    def Aceptar_callback(self):
        pass