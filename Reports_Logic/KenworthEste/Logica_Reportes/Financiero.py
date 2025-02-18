#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class ResultadosFinancieros(Variables):
    def __init__(self):
        # FUNCION PARA OBTENER EL DEPARTAMENTO
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.nombre_doc = 'RFE.xlsx'
        # CREAMOS UN ARRAY CON EL NOMBRE DE LAS COLUMNAS QUE VAMOS A OCUPAR DEL DATAFRAME ORIGINAL
        # ESTE ARRAY SE VA A OCUPAR MAS ADELANTE PARA CREAR EL DATAFRAME FINAL.
            
        columnas = [
            "Sucursal",
            "Numarticulo",
            "idCliente",
            "NomDepto",
            "CondicionUnidad",
            "NombreCte",
            "idClienteAsignatario",
            "NombreCteAsignatario",
            "Vendedor",
            "NumCategoria",
            "Modelo",
            "cantidad",
            "Venta",
            "NC_Bonif",
            "VentasNetas",
            "CostoTotal",
            "UtilidadBruta",
            "Compras",
            "VtasInternas",
            "NCreddeProv",
            "NCargodeProv",
            "ProvNCargoCargo",
            "ProvNCargoAbono",
            "ProvNCredCargo",
            "ProvNCredAbono",
            "NotaCargoCte"
        ]

        # OBTENEMOS LA RUTA DEL ARCHIVO Y PARSEAMOS SU CONTENIDO Y SUS CABECERAS.
        
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        df.columns = df.columns.str.replace(" ", "_")
        
        # creamos la tabla pivote, con el fin de obtener las unidades facturadas
        pivot = pd.pivot_table(df, index=['Numarticulo', 'Modelo', 'Sucursal', 'idCliente', 'NombreCte', 'idClienteAsignatario', 'NombreCteAsignatario', 'NumCategoria', 'Vendedor', 'NomDepto', 'CondicionUnidad'], values=['cantidad', 'Venta', 'NC_Bonif', 'VentasNetas', 'CostoTotal', 'UtilidadBruta', '%_Margen_Conc', 'Compras', 'VtasInternas', 'NCreddeProv', 'NCargodeProv',	'ProvNCargoCargo',	'ProvNCargoAbono',	'ProvNCredCargo',	'ProvNCredAbono',	'NotaCargoCte'
        ],  aggfunc='sum')

        # copiamos la tabla pivote en una nueva variable
        df_pivote = pivot.copy()

        # eliminamos el formato de la tabla pivote, con la finalidas de aparecer los numeros que la tabla pivote maneja como vacios
        df_pivote.reset_index(inplace=True)
        
        # excluimos las cotizaciones
        df_unidades_facturadas = df_pivote.query("cantidad == 1").copy()

        df_unidades_facturadas_ordenado = df_unidades_facturadas[columnas]

        if (len(df_unidades_facturadas_ordenado) == 0):
            # GUARDAMOS EL ARCHIVO
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)

        else:
            # df_unidades_facturadas_ordenado.insert(
            #     loc = 1,
            #     column = "ZonaVenta",
            #     value = df_unidades_facturadas_ordenado["Sucursal"],
            #     allow_duplicates=True
            # )

            df_unidades_facturadas_ordenado.insert(
                loc = 15,
                column = "Margen(%)",
                value = df_unidades_facturadas_ordenado["UtilidadBruta"] / df_unidades_facturadas_ordenado["VentasNetas"],
                allow_duplicates=False
            )

            departamento = df_unidades_facturadas_ordenado["CondicionUnidad"].apply(lambda x: self.obtenerDepartamento(x))
            col_numero_articulo = "CH-" + df_unidades_facturadas_ordenado["Numarticulo"].map(str)
            col_modelo = "AM" + df_unidades_facturadas_ordenado["Modelo"].map(str)

            df_unidades_facturadas_ordenado["Numarticulo"] = col_numero_articulo
            df_unidades_facturadas_ordenado["Modelo"] = col_modelo

            df_unidades_facturadas_ordenado["Fecha"] = self.variables.date_movement_config_document()
            df_unidades_facturadas_ordenado["Ciudad"] = ""
            df_unidades_facturadas_ordenado["Estado"] = ""
            df_unidades_facturadas_ordenado["Status"] = ""
            df_unidades_facturadas_ordenado["Mes"] = self.variables.nombre_mes()
            df_unidades_facturadas_ordenado["Latitud"] = ""
            df_unidades_facturadas_ordenado["Longitud"] = ""


            df_unidades_facturadas_ordenado.insert(
                loc = 0,
                column = "Categoria",
                value = "Facturacion",
                allow_duplicates = False
            )

            df_unidades_facturadas_ordenado.insert(
                loc = 1,
                column = "Area",
                value = departamento,
                allow_duplicates = False
            )

            df_unidades_facturadas_ordenado.insert(
                loc = 2,
                column = "Departamento",
                value = df_unidades_facturadas_ordenado["Area"].str.upper(),
                allow_duplicates = False
            )
            
            df_unidades_facturadas_ordenado.insert(
                loc = 4,
                column = "Fecha Vta",
                value = "",
                allow_duplicates = False
            )
            
            df_unidades_facturadas_ordenado.insert(
                loc = 5,
                column = "Zona Vta",
                value = "",
                allow_duplicates = False
            )
            


    # TERMINAMOS DE INSERTAR COLUMNAS ------------------

            # FORMATEAMOS LAS COLUMNAS DE FECHA

            for column_name in df_unidades_facturadas_ordenado.columns:
                if "fecha" in column_name.lower():
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_america(df_unidades_facturadas_ordenado, column_name)
                    df_unidades_facturadas_ordenado = self.variables.global_date_format_dmy_mexican(df_unidades_facturadas_ordenado, column_name)
                else:
                    pass

            # BUSCAMOS COLUMNAS QUE SEAN DE TIPO BOOLEANO, SI LAS ENCUENTRA, QUE LAS CONVIERTA EN CADENA.

            columnas_bol=df_unidades_facturadas_ordenado.select_dtypes(include=bool).columns.tolist()
            df_unidades_facturadas_ordenado[columnas_bol] = df_unidades_facturadas_ordenado[columnas_bol].astype(str)
            
            df_unidades_facturadas_ordenado.drop(['NomDepto', 'CondicionUnidad'], axis=1, inplace=True)

            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            self.variables.guardar_datos_dataframe(self.nombre_doc, df_unidades_facturadas_ordenado, self.concesionario)
        
    def obtenerDepartamento(self, valor):
            # currentYear = datetime.now().year
            if (valor.lower() == "usado"):
                return "Venta de Unidades Usadas"
            else:
                return "Venta de Unidades Nuevas"
