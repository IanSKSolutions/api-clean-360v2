from flask import request, send_file
from flask_restful import Resource
import pandas as pd
import io
from controller.clean import clean
import traceback
import os

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

            return send_file(fileOutputName, mimetype='text/csv',
                         as_attachment=True,
                         download_name='archivo.csv')
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            return {"error": str(e)}, 500