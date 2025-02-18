#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
import json
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class PagoClientes(Variables):
    def __init__(self):
        super().__init__()
        #obtenemos el parth.
        #leemos el documento.
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.ruta = self.variables.customerPaymentGoals
        

        self.columnas_objetivo = []
        self.objetivos = pd.DataFrame()
        self.nombre_doc = 'PCE.xlsx'

        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        #copiamos la data para no afectar la original.
        #df1 = df.copy()

        #Eliminamos las columnas que no se van a ocupar.
        df.drop({'Hora Pago', 'Referencia', 'Días Plazo', 'DocumentoMSC', 'Observaciones Pago', 'Referencia Forma de Pago', 'Sucursal Responsable', 'Folio Interno Factura'}, axis=1, inplace=True)
        df = df.rename(columns={'Tipo Docto.':'Tipo Docto'})

        # damos formato a todas las cabeceras de las columnas.
        # recordar volver a la normalidad.
        df.columns = df.columns.str.replace(' ', '_')

        #insertamos columna de "Fecha Movimiento" y "Mes"
        df.insert(
            loc=4,
            column='Fecha_Movimiento',
            value=self.variables.date_movement_config_document(),
            allow_duplicates=True
        )
        df.insert(
            loc=5,
            column='Mes',
            value= self.variables.nombre_mes(),
            allow_duplicates=True
        )

        for i in df.columns:
            nombre_columna = i
            if (df[nombre_columna].dtypes == "object") and (nombre_columna == "Usuario_Aplicó"):
                self.objetivos[nombre_columna] = ['DANIA VARGAS ROSAS']
            elif (df[nombre_columna].dtypes == "object") and (nombre_columna == "Vendedor"):
                self.objetivos[nombre_columna] = ['Objetivo KWESTE']
            elif (df[nombre_columna].dtypes == "int64"):
                self.objetivos[nombre_columna] = ['0']
            elif (df[nombre_columna].dtypes == "float64"):
                self.objetivos[nombre_columna] = ['0.0']
            elif (nombre_columna == "Mes"):
                self.objetivos[nombre_columna] = self.variables.nombre_mes()
            elif (df[nombre_columna].dtypes == "datetime64[ns]") and (nombre_columna == "Fecha_Pago") or (nombre_columna == "Fecha_Movimiento"):
                self.objetivos[nombre_columna] = [self.variables.date_movement_config_document()]
            else:
                self.objetivos[nombre_columna] = ['']
                
        
        DataFrameConObjetivo = pd.concat([df, self.objetivos], join="inner")

        for column_name in DataFrameConObjetivo.columns:
                if "fecha" in column_name.lower():
                    DataFrameConObjetivo = self.variables.global_date_format_america(DataFrameConObjetivo, column_name)
                    DataFrameConObjetivo = self.variables.global_date_format_dmy_mexican(DataFrameConObjetivo, column_name)
                else:
                    pass
        

        # Recorremos todo el contenido de la columna de "Cuenta Bancaria".
        # si el contenido que encuentre es "digito", solo continuara.
        # si encuentra algo que no sea digito, lo remplazara por el digito 0.
        for dato in DataFrameConObjetivo['CuentaBancaria']:
            try:
                if (dato.isdigit() == True ):
                    continue
                else:
                    DataFrameConObjetivo['CuentaBancaria'] = DataFrameConObjetivo['CuentaBancaria'].replace(dato,0)
            except:
                pass
        
        # obtenemos los objetivos
        # con el json

        DataFrameConObjetivo["Motivo_Cancelación"] = ""
        

        columnas_bol=DataFrameConObjetivo.select_dtypes(include=bool).columns.tolist()
        DataFrameConObjetivo[columnas_bol] = DataFrameConObjetivo[columnas_bol].astype(str)

        DataFrameConObjetivo.columns = DataFrameConObjetivo.columns.str.replace(' ', '_')
        df_completo = DataFrameConObjetivo.query("~(Tipo_Docto == ['Factura de Egreso', 'Facturas de Activo Fijo'])")

        
        if os.path.exists(self.ruta):
            try:
                df_json = pd.read_json(self.ruta)
                for indice, fila in df_json.iterrows():
                    sucursal_json = fila["nombre"]
                    objetivo_json = fila["objetivo"]

                    # Verificar si la sucursal del JSON coincide con la sucursal en df

                    if sucursal_json in df_completo["Sucursal_Factura"].values.tolist():
                        # Actualizar el valor de "Objetivos" en df_completo
                        df_completo.loc[df_completo["Sucursal_Factura"] == sucursal_json, "Objetivos"] = objetivo_json
                    elif sucursal_json in df_completo["Vendedor"].values.tolist():
                        # Actualizar el valor de "Objetivos" en df_completo
                        df_completo.loc[df_completo["Vendedor"] == sucursal_json, "Objetivos"] = objetivo_json
                    else:
                        pass
            except:
                pass

        df_completo["Area"] = "Pago Clientes"

        # # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_completo, self.concesionario)
