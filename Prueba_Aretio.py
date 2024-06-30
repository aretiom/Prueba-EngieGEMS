# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 18:03:17 2024

@author: nonoa
"""

import pandas as pd
import numpy as np


#   Carga facturas AGIKEY

factAGI = pd.read_excel('AGIkey_facturas.xlsx',dtype={'FechaEstado': str})

facturas = factAGI.loc[(factAGI['Origen'] == 'TVB') &
                       (factAGI['FechaEstado'] == '2024-02-04 00:00:00') & 
                       (factAGI['ServicioFacturado']=='Almacenamiento TVB')]


sumAGI = facturas['Importe'].str.replace(',', '.').astype(float).sum()


#   Carga Deals


cargadeals = pd.read_excel('JVLNG_CTV_STOK_ABRIL_2024_06_18_13_34.xlsx')


#   Filtro deals

deals = cargadeals.loc[(cargadeals['AggregatedKey'] == '39980344,2024/06/13 16:51:32,STOK')]
subflows = eval(np.array(deals.loc[(deals['AggregatedKey'] == '39980344,2024/06/13 16:51:32,STOK')]['Flows'])[0])

#   Creación dataframe con subflows

dfsubflow = pd.DataFrame()

for elem in subflows:
    df = pd.DataFrame([elem])
    dfsubflow=pd.concat([dfsubflow,df],ignore_index=True)


#   Cálculo de la conciliación

dfsubflow = dfsubflow.loc[dfsubflow[dfsubflow['Date'].str.startswith('2024-03')].index]
dfsubflow = dfsubflow.loc[dfsubflow['Amount']!=0]
sumsubf = dfsubflow['Amount'].sum()

#   Creación del archivo txt con los resultados

with open('Resultados.txt', 'w',encoding='utf-8') as archivo:
    archivo.write('RESULTADOS DE LA CONCILIACIÓN\n')
    archivo.write('\n')
    archivo.write('●  Facturas de AGIKEY:\n')
    
    for i in facturas.index.tolist():
        archivo.write('    ■  Factura: ' + str(facturas['NumeroFactura'][i]) + 
                      ', Importe: ' + str(facturas['Importe'][i]) + 
                      ', Fecha de emisión: ' + str(facturas['FechaFactura'][i]) + '\n')
    archivo.write('\n')
    archivo.write('●  Deals:\n')
    archivo.write('    ■  Deal: ' + str(deals['AggregatedKey'][26])[0:7] + 
                  ', Cantidad: ' + str(sumsubf) + 
                  ', Start delivery date: ' + str(deals['StartDeliveryDate'][26]) + 
                  ', End delivery date: ' + str(deals['EndDeliveryDate'][26]) + 
                  ', Procedencia: ' + 'JVLNG_CTV_STOK\n')
    for i in dfsubflow.index.tolist():
        archivo.write('        ●●●  Sublow: ' + str(dfsubflow['Id'][i]) + 
                      ', Date: ' + str(dfsubflow['Date'][i]) + 
                      ', Subcantidad: ' + str(dfsubflow['Amount'][i]) + '\n')
    
    archivo.write('RESULTADO DE LA CONCILIACIÓN\n')
    archivo.write('    Total facturas AGIKEY: ' + str(sumAGI) + '\n')
    archivo.write('    Total deals: ' + str(sumsubf) + '\n')
    archivo.write('    Total facturas AGIKEY - Total deals = ' + str(sumAGI-sumsubf) + '\n')

    

    







