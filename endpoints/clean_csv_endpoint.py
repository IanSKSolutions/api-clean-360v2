from datetime import datetime
from flask import request, send_file
from flask_restful import Resource
import pandas as pd
import io
from controller.clean import clean
import traceback
import os
from dao.sql.sql_routes_details_dao import SQLRoutesDetailsDAO
from controller.update_locations import update_locations

class CleanCSVEndpoint(Resource):
    def post(self):
        # Verifica si se ha enviado un archivo en la solicitud
        if 'file' not in request.files:
            return {"error": "No file part"}, 400
        
        file = request.files['file']

        # Verifica si se ha seleccionado un archivo
        if file.filename == '':
            return {"error": "No selected file"}, 400
        
        try:
            clean(io.StringIO(file.stream.read().decode('utf-8')))
            fileOutputName = os.getenv("FILE_OUTPUT_NAME")

            routes_details_dao = SQLRoutesDetailsDAO()
            df_file_clean = pd.read_csv(fileOutputName, encoding='utf-8')
            ahora = datetime.now()

            # Extraer el mes y el año
            mes = ahora.month  # Nombre completo del mes
            anio = ahora.year
            df_routeDetails = routes_details_dao.list(mes-1,anio)
            update_locations(df_routeDetails,df_file_clean)
            return send_file(fileOutputName, mimetype='text/csv',
                         as_attachment=True,
                         download_name='archivo.csv')
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return {"error": str(e)}, 500