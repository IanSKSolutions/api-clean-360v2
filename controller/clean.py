import pandas as pd
from controller.tecnicos import extractDataFromTechniciansCSV
import sys
import os
import unicodedata
import re

fileOutputName = 'clean_file.csv'
fileNameTechnicians = ''

HEADERS_COLUMNS = {
    'operatorName': 0,
    'machineVersion':1,
    'configurationSelected':2,
    'noMachine':3,
    'plate':4,
    'noSerialManu':5,
    'invoiceNumber': 6,
    'stateMachine': 7,
    'salesPocGroup': 8,
    'pocGroup': 9,
    'pocName': 10,
    'pocResponsible': 11,
    'modelMachine': 12,
    'region': 13,
    'status': 14,
    'group': 15,
    'technician': 16,
    'pocCode': 17,
    'preventive': 18,
    'date': 19,
    'audited': 20,
    'cp': 21,
    'latitude': 22,
    'longitude': 23,
    'email': 24,
    'serviceType': 25,
    'tel':26, 
}

HEADERS_OUTPUT = [
    'Nombre del Operador',
    'Versión de Máquina',
    'Configuración Seleccionada',
    'Número de Máquina',
    'Placa',
    'No. de Serie de Manufactura',
    'No. de Factura',
    'Estado de Máquina',
    'Grupo de Venta del POC',
    'Grupo del POC',
    'Nombre del POC',
    'Responsable del POC',
    'Módelo de Máquina',
    'Región',
    'Estatus',
    'Agrupación',
    'Técnico',
    'Código de POC',
    'Preventivo',
    'Fecha',
    'Auditado',
    'CP',
    'Latitud',
    'Longitud',
    'Correo del Técnico',
    'Tipo de Servicio',
    'Celular'
]

mapa_de_estados = {
    "asignado al operador": "assigned to operator",
    "en un poc": "in poc",
    "en un poc con cambio de selección": "in poc with selection change",
    "a ser retirada": "to be removed",
    "a ser reemplazada": "to be replaced",
    "en instalación": "under installation"
}

# Función para buscar el valor correspondiente
def buscar_estado(entrada):
    # Convertir la entrada a minúsculas
    z
    entrada = entrada.lower()

    # Buscar el valor correspondiente en el diccionario
    valor = mapa_de_estados.get(entrada)

    if valor:
        return valor
    else:
        return "Missing"

def correctRegion(actualRow, prevRow, postRow, newRowData):
    
    if actualRow[HEADERS_COLUMNS['operatorName']] == postRow[HEADERS_COLUMNS['operatorName']]:
        newRowData[13] = postRow[HEADERS_COLUMNS['region']]
    elif actualRow[HEADERS_COLUMNS['operatorName']] == prevRow[HEADERS_COLUMNS['operatorName']]:
        if prevRow != None:
            newRowData[13] = prevRow[HEADERS_COLUMNS['region']]

    return newRowData
        

def isSameRegion(operatorName1, operatorName2, region1, region2):
    return operatorName1 == operatorName2 and region1 == region2

def validateInvoiceNumber(prevValue, postValue):
    value = None
    if prevValue != None:
        value = prevValue
    elif postValue != None:
        value = postValue
    else:
        value = '99999999'
    
    return value

def correctPocGroups(actualRow, prevRow, postRow, newRowData):
    global HEADERS_COLUMNS

    if (actualRow[HEADERS_COLUMNS['salesPocGroup']] == None or actualRow[HEADERS_COLUMNS['salesPocGroup']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['salesPocGroup']])) and ( actualRow[HEADERS_COLUMNS['pocGroup']] == None or actualRow[HEADERS_COLUMNS['pocGroup']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['pocGroup']])):
        if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], postRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], postRow[HEADERS_COLUMNS['region']]):
            newRowData[HEADERS_COLUMNS['salesPocGroup']] = postRow[HEADERS_COLUMNS['salesPocGroup']]
            newRowData[HEADERS_COLUMNS['pocGroup']] = postRow[HEADERS_COLUMNS['pocGroup']]
        elif prevRow != None: 
            if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], prevRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], prevRow[HEADERS_COLUMNS['region']]):
                newRowData[HEADERS_COLUMNS['salesPocGroup']] = prevRow[HEADERS_COLUMNS['salesPocGroup']]
                newRowData[HEADERS_COLUMNS['pocGroup']] = prevRow[HEADERS_COLUMNS['pocGroup']]
    else:
        if actualRow[HEADERS_COLUMNS['salesPocGroup']] == None or actualRow[HEADERS_COLUMNS['salesPocGroup']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['salesPocGroup']]):
            cellValue = actualRow[HEADERS_COLUMNS['pocGroup']]
            newRowData[HEADERS_COLUMNS['salesPocGroup']] = cellValue[:6] + 'O' + cellValue[7:]
            newRowData[HEADERS_COLUMNS['pocGroup']] = actualRow[HEADERS_COLUMNS['pocGroup']]
        elif actualRow[HEADERS_COLUMNS['pocGroup']] == None or actualRow[HEADERS_COLUMNS['pocGroup']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['pocGroup']]):
            cellValue = actualRow[HEADERS_COLUMNS['salesPocGroup']]
            newRowData[HEADERS_COLUMNS['pocGroup']] = cellValue[:6] + 'T' + cellValue[7:]
            newRowData[HEADERS_COLUMNS['salesPocGroup']] = actualRow[HEADERS_COLUMNS['salesPocGroup']]
        else:
            newRowData[HEADERS_COLUMNS['pocGroup']] = actualRow[HEADERS_COLUMNS['pocGroup']]
            newRowData[HEADERS_COLUMNS['salesPocGroup']] = actualRow[HEADERS_COLUMNS['salesPocGroup']]
    return newRowData

def correctPocNameResponsable(actualRow, prevRow, postRow, newRowData):
    global HEADERS_COLUMNS

    if actualRow[HEADERS_COLUMNS['pocName']] == None or actualRow[HEADERS_COLUMNS['pocName']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['pocName']]):
        if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], postRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], postRow[HEADERS_COLUMNS['region']]):
            newRowData[HEADERS_COLUMNS['pocName']] = postRow[HEADERS_COLUMNS['pocName']]
        elif prevRow != None: 
            if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], prevRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], prevRow[HEADERS_COLUMNS['region']]):
                newRowData[HEADERS_COLUMNS['pocName']] = prevRow[HEADERS_COLUMNS['pocName']]
    else:
         newRowData[HEADERS_COLUMNS['pocName']] = actualRow[HEADERS_COLUMNS['pocName']]

    if actualRow[HEADERS_COLUMNS['pocResponsible']] == None or actualRow[HEADERS_COLUMNS['pocResponsible']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['pocResponsible']]):
        if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], postRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], postRow[HEADERS_COLUMNS['region']]):
            newRowData[HEADERS_COLUMNS['pocResponsible']] = postRow[HEADERS_COLUMNS['pocResponsible']]
        elif prevRow != None: 
            if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], prevRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], prevRow[HEADERS_COLUMNS['region']]):
                newRowData[HEADERS_COLUMNS['pocResponsible']] = prevRow[HEADERS_COLUMNS['pocResponsible']]
    else:
        newRowData[HEADERS_COLUMNS['pocResponsible']] = actualRow[HEADERS_COLUMNS['pocResponsible']]

    return newRowData

def correctAgrupation(value):
    return value[9:17]

def correctCP(actualRow, prevRow, postRow, newRowData):
    global HEADERS_COLUMNS

    if actualRow[HEADERS_COLUMNS['cp']] == None or actualRow[HEADERS_COLUMNS['cp']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['cp']]) or actualRow[HEADERS_COLUMNS['cp']] == '#N/D':
        if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], postRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], postRow[HEADERS_COLUMNS['region']]):
            newRowData[HEADERS_COLUMNS['cp']] = postRow[HEADERS_COLUMNS['cp']]
        elif prevRow != None: 
            if isSameRegion(actualRow[HEADERS_COLUMNS['operatorName']], prevRow[HEADERS_COLUMNS['operatorName']], actualRow[HEADERS_COLUMNS['region']], prevRow[HEADERS_COLUMNS['region']]):
                newRowData[HEADERS_COLUMNS['cp']] = prevRow[HEADERS_COLUMNS['cp']]
    else:
         newRowData[HEADERS_COLUMNS['cp']] = actualRow[HEADERS_COLUMNS['cp']]

    return newRowData

def correctCoords(actualRow, newRowData):
    global HEADERS_COLUMNS
    latitude = 0
    try:
        latitude = actualRow[HEADERS_COLUMNS['latitude']].replace(",", "")
    except:
        latitude = actualRow[HEADERS_COLUMNS['latitude']]

    if latitude == '#N/D':
        latitude = 19.4323884006848
    else: 
        latitude = float(latitude)
    
    if latitude < 0:
        newRowData[HEADERS_COLUMNS['latitude']] = latitude*-1
    
    if latitude <= 47.4798412 and latitude >= 14.535102:
        newRowData[HEADERS_COLUMNS['latitude']] = latitude
    elif latitude <= 47479841200 and latitude >= 14535202000:
       newRowData[HEADERS_COLUMNS['latitude']] = latitude/1000000000
    else:
       newRowData[HEADERS_COLUMNS['latitude']] = 19.4323884006848

    longitude = 0

    try:
        longitude = actualRow[HEADERS_COLUMNS['longitude']].replace(",", "")
    except:
        longitude = actualRow[HEADERS_COLUMNS['longitude']]

    if longitude == '#N/D':
        longitude = -99.1333848444616
    else:
        longitude = float(longitude)

    if longitude >= 0:
        newRowData[HEADERS_COLUMNS['longitude']] = longitude*-1
    
    if longitude <= -86.710664000 and longitude >= -117.124430000:
        newRowData[HEADERS_COLUMNS['longitude']] = longitude
    elif longitude <= -86710664000 and longitude >= -117124430000:
       newRowData[HEADERS_COLUMNS['longitude']] = longitude/1000000000
    else:
       newRowData[HEADERS_COLUMNS['longitude']] = -99.1333848444616

    return newRowData

def remove_accents(text):
  withoutAccents = ""
  traduction_table = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "ñ": "n"
  }
  for letter in text:
    letter_without_accent = traduction_table.get(letter, letter)
    withoutAccents += letter_without_accent
  return withoutAccents

def is_email_valid(email):
  regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
  return re.search(regex, email) is not None

def procesaFila(actualRow, prevRow, postRow):

    global HEADERS_OUTPUT
    global HEADERS_COLUMNS
    newRowData = [0]*27
    
    newRowData[0] = actualRow[HEADERS_COLUMNS['operatorName']]

    newRowData = correctRegion(actualRow=actualRow, prevRow=prevRow, postRow=postRow, newRowData=newRowData)

    newRowData[1] = actualRow[HEADERS_COLUMNS['machineVersion']]
    newRowData[2] = actualRow[HEADERS_COLUMNS['configurationSelected']]
    newRowData[3] = actualRow[HEADERS_COLUMNS['noMachine']]
    newRowData[4] = actualRow[HEADERS_COLUMNS['plate']]
    newRowData[5] = actualRow[HEADERS_COLUMNS['noSerialManu']]

    if actualRow[HEADERS_COLUMNS['invoiceNumber']] == None or actualRow[HEADERS_COLUMNS['invoiceNumber']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['invoiceNumber']]):
        newRowData[6] = validateInvoiceNumber(prevRow[HEADERS_COLUMNS['invoiceNumber']] if prevRow != None else None, postRow)
    else:
        newRowData[6] = actualRow[HEADERS_COLUMNS['invoiceNumber']]

    newRowData[7] = buscar_estado(actualRow[HEADERS_COLUMNS['stateMachine']])

    newRowData = correctPocGroups(actualRow=actualRow, prevRow=prevRow, postRow=postRow, newRowData=newRowData)
    newRowData = correctPocNameResponsable(actualRow=actualRow, prevRow=prevRow, postRow=postRow, newRowData=newRowData)

    newRowData[12] = actualRow[HEADERS_COLUMNS['modelMachine']]
    newRowData[14] = actualRow[HEADERS_COLUMNS['status']]

    if actualRow[HEADERS_COLUMNS['group']] == None or actualRow[HEADERS_COLUMNS['group']] == '' or pd.isna(actualRow[HEADERS_COLUMNS['group']]):
        newRowData[HEADERS_COLUMNS['group']] = correctAgrupation(newRowData[HEADERS_COLUMNS['pocGroup']])
    else:
        newRowData[15] = actualRow[HEADERS_COLUMNS['group']]
    
        
    dataTecnician = extractDataFromTechniciansCSV(newRowData[15], fileNameTechnicians)
    newRowData[HEADERS_COLUMNS['technician']] = dataTecnician['name']
    newRowData[HEADERS_COLUMNS['email']] = dataTecnician['email']
    newRowData[HEADERS_COLUMNS['tel']] = dataTecnician['tel']
    

    if newRowData[HEADERS_COLUMNS['technician']] == '#N/D':
        newRowData[16] = 'Vacante'
    else:
        newRowData[16] = newRowData[HEADERS_COLUMNS['technician']]
    
    newRowData[24] = remove_accents(newRowData[HEADERS_COLUMNS['email']])
    
    if not is_email_valid(newRowData[24]):
        if newRowData[24] == 'Vacante' or newRowData[24] == 'VACANTE' or newRowData[24] == '#N/D':
            newRowData[24] = 'demo@mx.nestle.com'
        else:
            return None

    if newRowData[24] == 'demo@mx.nestle.com' or newRowData[24] == '#N/D':
        newRowData[26] = '55 6565 4560'
    else:
        newRowData[26] = newRowData[HEADERS_COLUMNS['tel']]

    newRowData[17] = actualRow[HEADERS_COLUMNS['pocCode']]
    newRowData[HEADERS_COLUMNS['preventive']] = 'Si' if actualRow[HEADERS_COLUMNS['preventive']] != None and actualRow[HEADERS_COLUMNS['preventive']] != '' and not pd.isna(actualRow[HEADERS_COLUMNS['preventive']]) else 'No'
    newRowData[19] = actualRow[HEADERS_COLUMNS['date']] if actualRow[HEADERS_COLUMNS['date']] != None and actualRow[HEADERS_COLUMNS['date']] != '' and not pd.isna(actualRow[HEADERS_COLUMNS['date']]) else ''
    newRowData[HEADERS_COLUMNS['audited']] = 'Si' if actualRow[HEADERS_COLUMNS['audited']] != None and actualRow[HEADERS_COLUMNS['audited']] != '' and not pd.isna(actualRow[HEADERS_COLUMNS['audited']]) else 'No'
    newRowData = correctCP(actualRow=actualRow, prevRow=prevRow, postRow=postRow, newRowData=newRowData)
    newRowData = correctCoords(actualRow, newRowData=newRowData)

    newRowData[HEADERS_COLUMNS['serviceType']] = 'Auditoría' if actualRow[HEADERS_COLUMNS['serviceType']] != None and actualRow[HEADERS_COLUMNS['serviceType']] != '' and pd.isna(actualRow[HEADERS_COLUMNS['serviceType']]) else 'Correctivo'
    
    return newRowData

def clean(file):

    global fileNameTechnicians
    
    fileNameTechnicians = os.getenv('FILE_NAME_TECHNICIANS')
    fileOutputName = os.getenv('FILE_OUTPUT_NAME')

    print("Limpiando archivo generado")
    try:
        os.remove(fileOutputName)
    except:
        print("No hay archivo que limpiar")
     
    try:
        chunkSize = 99
        prevRow = None
        postRow = None
        actualRow = None
       
        for i, chunk in enumerate(pd.read_csv(file, chunksize=chunkSize, skiprows=0, encoding="utf-8")):
            data = []
            for row_index, row in enumerate(chunk.itertuples(index=False)):
                
                if actualRow != None:
                    postRow = row

                if actualRow != None and postRow != None:
                    newRow = procesaFila(actualRow, prevRow, postRow)
                    if newRow != None:
                        actualRow = newRow
                        data.append(actualRow)

                if actualRow != None:
                    prevRow = actualRow
                
                actualRow = row

            df_output = pd.DataFrame(data)
            df_output.to_csv(fileOutputName, index=False, mode='a', encoding="utf-8", header=False,)
            ##Save info in CSV
        print("Proceso terminado")
    except FileNotFoundError:
        print('No se encontró el archivo.')