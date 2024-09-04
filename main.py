from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from endpoints.clean_csv_endpoint import CleanCSVEndpoint


app = Flask(__name__)
CORS(app)
api= Api(app)
        
api.add_resource(CleanCSVEndpoint, '/upload-csv')

if __name__ == '__main__':
    app.run(debug=True)