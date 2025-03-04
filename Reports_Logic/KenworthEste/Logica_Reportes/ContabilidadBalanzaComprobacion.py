#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias.
import os
import pandas as pd
import re
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class ContabilidadBalanzaComprobacionAnalisis:
    def __init__(self):
        self.variables = Variables()
        self.concesionario = Concesionarios().concesionarioEste
        self.nombre_doc = 'BCC.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        
# comment: Validacion REGEX para la columna de cuentas
        patron = r"^\d+(-\d+){3}$"
        #----------------
        
        Cumplen_cuenta = [bool(re.match(patron, valor)) for valor in df["Cuenta"]]
        df.insert(1, 'Cumple_la_cuenta', Cumplen_cuenta, False)
        
        columnas_bol=df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)
        
        try:
            codigos = pd.read_json(self.variables.bcc_codigos_vs_cuentas)
        except FileNotFoundError:
            return
        df['Cuenta'] = df['Cuenta'].astype(str)
        codigos['Cuenta'] = codigos['Cuenta'].astype(str)
        df = pd.merge(df, codigos[['Cuenta', 'Codigo']], on='Cuenta', how='left')
        columna_codigos = df.pop('Codigo')
        df.insert(2, 'Codigo', columna_codigos, False)
        
        self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
        
        
    

