from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pandas as pd
import io

app = Flask(__name__)
api= Api(app)

class UploadCSV(Resource):
    def post(self):
        # Verifica si se ha enviado un archivo en la solicitud
        if 'file' not in request.files:
            return {"error": "No file part"}, 400
        
        file = request.files['file']

        # Verifica si se ha seleccionado un archivo
        if file.filename == '':
            return {"error": "No selected file"}, 400
        
        try:
            df = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))

            data = df.to_dict(orient='records')

            return data, 200
        
        except Exception as e:
            return {"error": str(e)}, 500
        
api.add_resource(UploadCSV, '/upload-csv')

if __name__ == '__main__':
    app.run(debug=True)