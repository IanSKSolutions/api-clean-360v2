import pandas as pd
import os

def update_locations(archivo_fuente, archivo_destino):
    # Realizar la combinación usando la columna 'device_number' del archivo fuente y 'NÔøΩmero de mÔøΩquina' del archivo destino
    combinacion = archivo_destino.merge(archivo_fuente[['device_number', 'latitud', 'longitud']],
                                        left_on='Número de Máquina', right_on='device_number', how='left', suffixes=('', '_nuevo'))
    # Reemplazar las columnas 'Latitude' y 'Longitude' en archivo_destino con los valores de archivo_fuente
    # Se conservan los valores originales donde no haya coincidencias
    combinacion['Latitud'] = combinacion['latitud'].combine_first(combinacion['Latitud'])
    combinacion['Longitud'] = combinacion['longitud'].combine_first(combinacion['Longitud'])
    # Convertir las columnas 'Latitude' y 'Longitude' a float para asegurar que el formato decimal sea correcto
    combinacion['Latitud'] = pd.to_numeric(combinacion['Latitud'], errors='coerce')
    combinacion['Longitud'] = pd.to_numeric(combinacion['Longitud'], errors='coerce')
    # Asegurar que los números se muestren con puntos decimales y sin omitir ningún número significativo
    combinacion['Latitud'] = combinacion['Latitud'].apply(lambda x: f'{x:.6f}' if pd.notnull(x) else '')
    combinacion['Longitud'] = combinacion['Longitud'].apply(lambda x: f'{x:.6f}' if pd.notnull(x) else '')
    # Eliminar las columnas adicionales que ya no se necesitan
    combinacion.drop(columns=['latitud', 'longitud', 'device_number'], inplace=True)
    # Guardar el archivo CSV actualizado con la codificación adecuada para evitar problemas de caracteres
    combinacion.to_csv(os.getenv("FILE_OUTPUT_NAME"), index=False, encoding='utf-8')