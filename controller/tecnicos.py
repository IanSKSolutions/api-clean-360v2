import pandas as pd

def extractDataFromTechniciansCSV(agroup, fileNameTechnicians):
    global FILE_NAME
    
    df = pd.read_csv(fileNameTechnicians)

    row = df[df['CODIGOTECNICO'] == agroup]
    
    data = {
        'name': row['NOMBRETECNICO'].iloc[0] if not row['NOMBRETECNICO'].empty and not pd.isna(row['NOMBRETECNICO'].iloc[0]) else 'Demo',
        'email': row['Correo'].iloc[0] if not row['Correo'].empty and not pd.isna(row['Correo'].iloc[0]) else 'demo@mx.nestle.com',
        'tel': row['CELULAR'].iloc[0] if not row['CELULAR'].empty and not pd.isna(row['CELULAR'].iloc[0]) else '5555555555'
    }

    return data
