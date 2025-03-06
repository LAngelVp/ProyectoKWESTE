#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias.
import traceback
import os
import pandas as pd
import re
import tkinter as tk
from tkinter import messagebox
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class ContabilidadBalanzaComprobacionAnalisis(Variables):
    def __init__(self):
        try:
            self.variables = Variables()
            self.concesionario = Concesionarios().concesionarioEste
            codigos = pd.read_json(self.variables.bcc_codigos_vs_cuentas)
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
            
            
            df['Cuenta'] = df['Cuenta'].astype(str)
            codigos['Cuenta'] = codigos['Cuenta'].astype(str)
            df = pd.merge(df, codigos[['Cuenta', 'Codigo']], on='Cuenta', how='left')
            columna_codigos = df.pop('Codigo')
            df.insert(2, 'Codigo', columna_codigos, False)
            
            df["Mes"] = self.variables.nombre_mes()
            
            df["Codigo"] = df["Codigo"].fillna("Sin codigo")
            
            self.variables.guardar_datos_dataframe(self.nombre_doc, df, self.concesionario)
        except Exception as e:
            # Mostrar el error en un MessageBox de Tkinter
            error_message = f"Ocurrió un error: {str(e)}\n\nDetalles: {traceback.format_exc()}"
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            messagebox.showerror("Error", error_message)
            root.quit()
        
    

