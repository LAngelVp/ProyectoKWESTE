#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import shutil
from ..globalModulesShare.resources import *
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QBrush, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from webbrowser import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..globalModulesShare.Inicio_FechaMovimiento import *
from .KenworthConnect import *
from ..globalModulesShare.InicialClassObjetivos import *
from ..ventanaspy.V_ProcesadorGeneral import Ui_V_ProcesadorGeneral
from ..globalModulesShare.Home_rutas import *
from .Controller.FuncionesBalanzaComprobacionContabilidad import *
from ..globalModulesShare.mensajes_alertas import Mensajes_Alertas
from ..globalModulesShare.icono import *
from ..globalModulesShare.documentos_json import *
import subprocess

class VContabilidadKWESTE(QMainWindow):
    closed = pyqtSignal()
    CREAR_JSON_CODIGOS_BCC = pyqtSignal()
    def __init__(self):
        super(VContabilidadKWESTE,self).__init__()
        self.variables = Variables()
        self.ui = Ui_V_ProcesadorGeneral()
        self.ui.setupUi(self)
        # variables a las rutas de los iconos e imagenes
        Icon_Cerrar = QIcon(":/Source/Icon_Close.png")
        Icon_Minimizar = QIcon(":/Source/Icon_Minimize.png")
        Icon_Help = QIcon(":/Source/Icon_Help.png")
        Icon_Delete = QIcon(":/Source/Icon_Delete.png")
        Icon_Proccess = QIcon(":/Source/Icon_Proccess.png")
        Icon_Upload = QIcon(":/Source/Icon_Upload.png")
        # logo_KWESTE = QPixmap(":/Source/KWESTE.png")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        _translate = QtCore.QCoreApplication.translate
        self.ui.lblLogo.setText(_translate("VentanaProcesador", 
    "<html><head/><body><p align=\"center\"><span style=\"font-size:14pt; font-weight:700;\">CONTABILIDAD </span>"
    "<img src=\":/Source/IconContabilidad.png\" width=\"40\" height=\"35\"/></p></body></html>"))
        #// VARIABLES
        # llamamos el metodo de creacion de carpetas
        self.Creacion_Carpetas()
        # quitamos la barra superior
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Crear la instancia de la ventana y configurarla
        
        
        # colocar los iconos e imagenes en su correspondiente elemento.
        # self.ui.lblLogoKWESTE.setPixmap(logo_KWESTE)
        self.ui.btc_btc_Cerrar.setIcon(Icon_Cerrar)
        self.ui.btc_btc_Minimizar.setIcon(Icon_Minimizar)
        self.ui.btn_btn_Ayuda.setIcon(Icon_Help)
        self.ui.btn_btn_Eliminar.setIcon(Icon_Delete)
        self.ui.btn_btn_Eliminar.setIconSize(QtCore.QSize(24, 24))
        self.ui.btn_btn_Comenzar.setIcon(Icon_Proccess)
        self.ui.btn_btn_Comenzar.setIconSize(QtCore.QSize(24, 24))
        self.ui.btn_btn_Subir.setIcon(Icon_Upload)
        self.ui.btn_btn_Subir.setIconSize(QtCore.QSize(24, 24))
        # creamos el hilo
        self.Hilo = trabajohilo()
        #conexiones de los botones
        self.ui.btn_btn_Subir.clicked.connect(self.Cargar)
        self.ui.btn_btn_Comenzar.clicked.connect(self.ComenzarProceso)
        self.ui.btn_btn_Eliminar.clicked.connect(self.RemoveProcessed)
        self.ui.btn_btn_Ayuda.clicked.connect(self.Ayuda)
        self.ui.btc_btc_Cerrar.clicked.connect(self.Cerrar)
        self.ui.btc_btc_Minimizar.clicked.connect(self.Minimizar)
        self.ui.btn_btn_Errores.clicked.connect(self.abrir_ruta_errores)
        self.ui.btn_btn_Originales.clicked.connect(self.abrir_ruta_originales)
        self.ui.btn_btn_Procesados.clicked.connect(self.abrir_ruta_procesados)
        self.CREAR_JSON_CODIGOS_BCC.connect(self.comprobar_existencia_archivos_configuracion)
        
        self.menu = QMenuBar()
        self.menu_documento = self.menu.addMenu("Opciones")
        # MENU DE OPCIONES
        # self.ui.actionObjetivos_Mensuales_PagosClientes.triggered.connect(self.ObjetivosPagoClientes)
        self.ui.actionFechaMovimiento.triggered.connect(self.FechaMovimiento)
        self.ui.actionCodigosCuentas.triggered.connect(self.CodigosCuentas)
        self.ui.actionDireccionesDeEnvio.triggered.connect(self.direcciones_envio)
        # self.ui.actionDepartamentos.triggered.connect(self.departamentos_vendedores)
        

        # señales del hilo
        self.Hilo.signal.connect(self.mensajeTrabajoTerminado)
        self.Hilo.signalDocumentosErroneos.connect(self.mensajeArchivoErroneo)
        self.Hilo.signalNombreArchivo.connect(self.nombreArchivoTrabajando)
        self.Hilo.signalShowTrabajos.connect(self.Show_Data_Trabajos)
        self.Hilo.signalShowProcesados.connect(self.Show_Data_Procesado)
        

        
        self.variables.actualizar_fecha_movimiento()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
        
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()

    def Aceptar_callback(self):
        pass
    def Ayuda_callback(self):
        open_new(self.variables.pdf)
        
    def CodigosCuentas(self):
        self.v_CodigosCuentas = FuncionesBComprobacionContabilidad()
        self.CREAR_JSON_CODIGOS_BCC.emit()
        self.v_CodigosCuentas.MOSTRAR_DATOS_EXISTENTES.connect(self.v_CodigosCuentas.mostrar_datos_cuentas)
        self.v_CodigosCuentas.MOSTRAR_DATOS_EXISTENTES.emit()
        self.v_CodigosCuentas.show()

    def comprobar_existencia_archivos_configuracion(self):
        creacion_json(self.variables.help_directory,self.variables.codigos_cuentas_balanza_comprobacion_contabilidad_kweste, None).comprobar_existencia
        
    # def departamentos_vendedores(self):
    #     self.ventana_departamentos = Vendedores()
    #     self.ventana_departamentos.show()

    def direcciones_envio(self):
        self.ventana_rutas = rutas()
        self.ventana_rutas.show()

    # def ObjetivosPagoClientes(self):
    #     self.ventana_obj = ClassPrincipalObjPagos()
    #     self.ventana_obj.show()

    def FechaMovimiento(self):
        self.ventana_obj = Home_DateMovement()
        self.ventana_obj.show()

    def abrir_ruta_errores(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_errores_kwe, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_originales(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_original_kwe, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_procesados(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_exitosos_kwe, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar

        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def mensajeTrabajoTerminado(self):
        Mensajes_Alertas(
            "Trabajos Terminados",
            "Todos los trabajos que se comenzaron fueron insertados por el proceso lógico del sistema.",
            QMessageBox.Icon.Information,
            None,
            botones=[
                ("Aceptar", self.Aceptar_callback)
            ]
        ).mostrar
        textoVacio =""
        self.nombreArchivoTrabajando(textoVacio)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#-------------------------------------------------


    def mensajeArchivoErroneo(self, mensaje):
        Mensajes_Alertas(
            "Errores durante el proceso",
            f'Los documentos que no se lograron procesar son:\n{mensaje}\nLa ruta de los errores es:\n {self.variables.ruta_errores_kwe}',
            QMessageBox.Icon.Critical,
            "Cuando el sistema muestra un error como este, existen algunos factores que se tienen que tomar en cuenta:\n1.- El nombre del documento no tiene la nomenclatura correcta.\n2.- El documento original no contiene las columnas a trabajar o su contendo es incorrecto.\n3.- EL documento no es el correcto o esta corrupto.",
            botones=[
                ("Aceptar", self.Aceptar_callback)
            ]
        ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
# MOSTRAR NOMBRE DEL DOCUMENTO QUE SE ESTA TRABAJANDO
    def nombreArchivoTrabajando(self, nombre):
        if (nombre != ""):
            self.ui.lbl_TrabajandoCon.setText(f'Trabajando Con:')
            self.ui.lbl_NombreReporte.setText(f'{nombre}')
        else:
            self.ui.lbl_TrabajandoCon.setText(f'TERMINADO')
            self.ui.lbl_NombreReporte.setText(f'')
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#--------------------------------------------
#-------------------------------------------------------
# EVENTOS DEL MOUSE
    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())
    # Apartado de funciones
    #-------------------------
    # mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Trabajos(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_Trabajos_kwe)
        self.ui.Tabla_cola.setRowCount(len(archivos_para_mostrar))
        self.ui.Tabla_cola.setColumnCount(1)
        self.ui.Tabla_cola.setHorizontalHeaderLabels(["Nombre del archivo"])
        self.ui.Tabla_cola.setStyleSheet("color:#000000;")
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QBrush(QColor(0, 0, 0)))
            self.ui.Tabla_cola.setItem(fila, 0, elemento)
        header = self.ui.Tabla_cola.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("background-color:#4096d8; color:#FFFFFF;")

        verticalHeader = self.ui.Tabla_cola.verticalHeader()
        verticalHeader.setStyleSheet("background-color:#4096d8; color:#FFFFFF;")

    # mostrar el contenido de la carpeta en la tabla de trabajos.
    def Show_Data_Procesado(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_exitosos_kwe)
        self.ui.Tabla_Procesados.setRowCount(len(archivos_para_mostrar))
        self.ui.Tabla_Procesados.setColumnCount(1)
        self.ui.Tabla_Procesados.setHorizontalHeaderLabels(["Nombre del archivo"])
        self.ui.Tabla_Procesados.setStyleSheet("color:#000000;")
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QBrush(QColor(0, 0, 0)))
            self.ui.Tabla_Procesados.setItem(fila, 0, elemento)
        header = self.ui.Tabla_Procesados.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("background-color:#4096d8; color:#FFFFFF;")
        verticalHeader = self.ui.Tabla_Procesados.verticalHeader()
        verticalHeader.setStyleSheet("background-color: #4096d8; color:#FFFFFF;")

    def Creacion_Carpetas(self):
        # Rutas de las carpetas que se deben verificar/crear
        rutas_a_verificar = [
            self.variables.ruta_Trabajos_kwe,
            self.variables.ruta_original_kwe,
            self.variables.ruta_errores_kwe,
            self.variables.ruta_exitosos_kwe,
        ]
        
        # Verificar si todas las carpetas ya existen
        todas_existen = all(os.path.exists(ruta) for ruta in rutas_a_verificar)
        
        if todas_existen:
            pass
        else:
            # Crear las carpetas que no existan
            for ruta in rutas_a_verificar:
                if not os.path.exists(ruta):
                    os.makedirs(ruta, exist_ok=True)
            
    # cerrar la ventana
    def Cerrar(self):
        self.close()
    # minimizar la ventana
    def Minimizar(self):
        self.showMinimized()
    # mostrar la data en las tablas
    
    # cargar los archivos a la carpeta de trabajo
    def Cargar(self):
        self.Creacion_Carpetas()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
        ubicacion_carga = os.chdir(self.variables.root_directory_system)
        options = QFileDialog().options()
        # options |= QFileDialog.DontUseNativeDialog  # Evitar el uso del diálogo nativo del sistema operativo (opcional)
        options |= QFileDialog.Option.ReadOnly  # Permite abrir los archivos solo en modo lectura (opcional)
        options |= QFileDialog.Option.HideNameFilterDetails  # Ocultar detalles del filtro (opcional)
        options |= QFileDialog.Option.DontResolveSymlinks  # No resolver enlaces simbólicos (opcional)

        selected_filter = "Hojas de Excel (*.xlsx);;Todos los archivos (*)"
        
        if os.path.isdir(self.variables.ruta_Trabajos_kwe) == True:
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_kwe)
            except:
                pass
        else:
            os.makedirs(self.variables.ruta_Trabajos_kwe)
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_kwe)
            except:
                pass
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
#----------------------------------------        
    # REALIZAR PROCESO
    # HILO DEL TRABAJO DE " KWESTE "
    def ComenzarProceso(self):
        if self.Hilo.isRunning():
            self.Hilo.requestInterruption()
        else:
            self.Hilo.start()

    def eliminar(self):
        carpeta_contenido_eliminar = os.listdir(self.variables.ruta_exitosos_kwe)
        for archivo in carpeta_contenido_eliminar:
            if (len(carpeta_contenido_eliminar) != 0):
                try:
                    archivo_completo = os.path.join(self.variables.ruta_exitosos_kwe, archivo)
                    os.remove(archivo_completo)
                except:
                    pass
            else:
                pass

    # eliminamos los trabajos realizados de la carpeta de exitosos.
    def RemoveProcessed(self):
        self.Creacion_Carpetas()
        ruta_trabajos_procesados = os.listdir(self.variables.ruta_exitosos_kwe)
        if (len(ruta_trabajos_procesados) == 0):
            Mensajes_Alertas(None,None,None,None,botones=[("Aceptar", self.Aceptar_callback)]).Eliminar_vacio
        else:
            Mensajes_Alertas(None,None,None,None,botones=[("Eliminar", self.eliminar)]).Eliminar_lleno
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()


    def Ayuda(self):
        Mensajes_Alertas(
            "Información de Ayuda",
            'Si tienes problemas con la aplicación debido a que no sabes como guardar tus archivos de excel para que puedan ser transformados.\nPuedes ver el manual de usuario dando click en el boton de "Ver"',
            QMessageBox.Icon.Information,  # Aquí se pasa el tipo de ícono
            None,
            botones = [
                ("Aceptar", self.Aceptar_callback),
                ("Ver", self.Ayuda_callback)
            ]
        ).Apartado_Ayuda
        
        

# CLASE DEL HILO----------------------
class trabajohilo(QThread):
# agregamos una variable de tipo señal
    signal = pyqtSignal()
    signalDocumentosErroneos = pyqtSignal(str)
    signalShowTrabajos = pyqtSignal()
    signalShowProcesados = pyqtSignal()
    signalNombreArchivo =  pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.variables = Variables()

    def run(self):
        array_errores = []
        #---------------------------------------
        # diccionario de los archivos.
        diccionario_archivos = {
            "BCC.xlsx" : KenworthConnect().BalanzaComprobacion,
        }
        #-----------------------------------------------
        while True:
            carpeta_de_trabajos = os.listdir(self.variables.ruta_Trabajos_kwe)
            if not carpeta_de_trabajos:
                nombre_documento = ""
                self.signalNombreArchivo.emit(nombre_documento)
                return
            else:
                for nombre_archivo in carpeta_de_trabajos:
                    if (nombre_archivo in diccionario_archivos):
                        try:
                            self.signalNombreArchivo.emit(nombre_archivo)
                            Metodo = diccionario_archivos[nombre_archivo]
                            Metodo()
                            self.Comprobacion_Originales(nombre_archivo)
                            self.signalShowTrabajos.emit()
                            self.signalShowProcesados.emit()
                        except Exception as e:
                            array_errores.append(nombre_archivo)
                            self.Comprobacion_Errores(nombre_archivo)
                            self.signalShowTrabajos.emit()
                            self.signalShowProcesados.emit()
                            continue
                    else:
                        nombre_archivo_error = nombre_archivo
                        array_errores.append(nombre_archivo_error)
                        self.Comprobacion_Errores(nombre_archivo)
                        self.signalShowTrabajos.emit()
                        self.signalShowProcesados.emit()
                        continue
                self.signalShowTrabajos.emit()
                self.signalShowProcesados.emit()
            if array_errores:
                mensaje = ""
                x = 1
                for i in array_errores:
                    mensaje += f'{x}.-{i}\n'
                    x += 1
                self.signalDocumentosErroneos.emit(mensaje)
                continue
            self.signalShowTrabajos.emit()
            self.signalShowProcesados.emit()

#--------------------------------------------------
# COMPROBAR SI EXISTE EL DOCUMENTO ORIGINAL EN EL DESTINO
    def Comprobacion_Originales(self, file_name):
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_kwe, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_original_kwe, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_original_kwe)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_original_kwe)
#--------------------------------------------------
#--------------------------------------------------
# COMPRROBAR SI EXISTE EL DOCUMENTO ERRONEO EN EL DESTINO
    def Comprobacion_Errores(self, file_name):
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_kwe, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_errores_kwe, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_errores_kwe)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_errores_kwe)
#--------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ventana = VContabilidadKWESTE()
    Ventana.show()
    sys.exit(app.exec())