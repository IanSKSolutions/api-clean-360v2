from dao.routes_details_dao import RoutesDetailsDAO
from db.db_conn import DBConn
import pandas as pd
from sqlalchemy import text
class SQLRoutesDetailsDAO(RoutesDetailsDAO):

    __GET_ROUTE_DETAILS_MONTH = 'select device_number, ST_X(poc_gps) as longitud, ST_Y(poc_gps) as latitud from route_detail where extract(month from updated_at) = %s and extract(year from updated_at) = %s and location_updated = true'
    #where 
    def __init__(self):
        try:
            self.__dbConn = DBConn()
        except:
            print("Problem opening database")

    def list(self, month, year):
        parameters = (
            month,
            year
        )

        print(self.__dbConn._engine)

        df = pd.read_sql(self.__GET_ROUTE_DETAILS_MONTH, self.__dbConn._engine, params=parameters)
        self.closeConnection()
        #print(df.head(10))
        return df
    
    def closeConnection(self):
        self.__dbConn.closeConnection()