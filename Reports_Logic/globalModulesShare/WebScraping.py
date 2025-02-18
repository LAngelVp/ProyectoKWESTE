import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from urllib3.exceptions import InsecureRequestWarning
from .ContenedorVariables import Variables
from .mensajes_alertas import Mensajes_Alertas
import tkinter as tk
from tkinter import messagebox
class Web_scraping:
    def __init__(self):
        self.fecha_inicial = None
        self.fecha_final = None
        self.fecha_inicial_rango_fechas = None
        self.fecha_final_rango_fechas = None
        self.fecha_inicial_mes_anterior = None
        self.fecha_final_mes_anterior = None

    def obtener_dolares(self, fecha_inicial, fecha_final):
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.fecha_inicial_rango_fechas = pd.to_datetime(fecha_inicial, format='%d/%m/%Y')
        self.fecha_final_rango_fechas = pd.to_datetime(fecha_final, format='%d/%m/%Y')
        
        df = self.procesar_dolares()
        
        if df is None:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error al obtener los dolares en el DOF", 
                         "No se logró obtener la información del DOF. Puede ser por problemas de conexión o fallos en la plataforma. Intente más tarde.")
            
            # Cerrar la aplicación de Tkinter
            root.quit()
            return None
        
        # Crear el rango de fechas completo
        rango_completo_fechas = pd.date_range(start=self.fecha_inicial_rango_fechas, end=self.fecha_final_rango_fechas, freq='D')
        df_completo_fechas = pd.DataFrame(rango_completo_fechas, columns=['Fecha'])
        
        # Merge de las fechas con los valores
        juntar_dos = pd.merge(df_completo_fechas, df, on='Fecha', how='left')
        
        # Rellenar los NaN con el valor anterior
        juntar_dos['Valor'] = juntar_dos['Valor'].ffill()
        
        if juntar_dos["Valor"].isna().any():
            juntar_dos = self.completar_datos_en_valor(juntar_dos)
            
        for column_name in juntar_dos.columns:
            if "fecha" in column_name.lower():
                juntar_dos = Variables().global_date_format_america(juntar_dos, column_name)
                juntar_dos = Variables().global_date_format_dmy_mexican(juntar_dos, column_name)
            else:
                pass
        juntar_dos['Valor'] = pd.to_numeric(juntar_dos['Valor'])
        return juntar_dos

    def completar_datos_en_valor(self, dataframe):
        # Ajustar las fechas para obtener datos del mes anterior
        self.fecha_inicial_mes_anterior = self.fecha_inicial_rango_fechas - pd.DateOffset(months=1)
        self.fecha_final_mes_anterior = self.fecha_inicial_rango_fechas - pd.Timedelta(days=1)
        
        df_mes_anterior = self.procesar_dolares()
        
        if df_mes_anterior is None:
            return
        
        ultimo_valor_mes_anterior = df_mes_anterior['Valor'].iloc[-1]
        
        dataframe['Valor'] = dataframe['Valor'].fillna(ultimo_valor_mes_anterior)
        
        return dataframe
        
    def procesar_dolares(self):
        if self.fecha_inicial_mes_anterior is None or self.fecha_final_mes_anterior is None:
            ruta_dof = f'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={self.fecha_inicial}&hfecha={self.fecha_final}#gsc.tab=0'
        else:
            ruta_dof = f'https://www.dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha={self.fecha_inicial_mes_anterior.strftime("%d/%m/%Y")}&hfecha={self.fecha_final_mes_anterior.strftime("%d/%m/%Y")}#gsc.tab=0'
        
        # Silenciar la advertencia de SSL
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Realizar la solicitud con SSL deshabilitado
        response = requests.get(ruta_dof, verify=False)

        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
            div = self.soup.find('div', {'id': 'cuerpo_principal'})
            if div:
                self.tabla = div.find('table', {'class': 'Tabla_borde'})
                if self.tabla:
                    tabla_html = str(self.tabla)
                    df = pd.read_html(StringIO(tabla_html))[0]
                    df.columns = df.iloc[0]
                    df.drop(index=0, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    if 'Fecha' in df.columns:
                        df["Fecha"] = pd.to_datetime(df['Fecha'], dayfirst=True)
                    return df
                else:
                    return None
            else:
                return None
        else:
            return None