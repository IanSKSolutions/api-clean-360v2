import os
from sqlalchemy import create_engine

class DBConn:
    def __init__(self):
        self.__db_host = os.getenv('DB_HOST')
        self.__db_name = os.getenv('DB_NAME')
        self.__db_user = os.getenv('DB_USER')
        self.__db_pass = os.getenv('DB_PASS')
        self.__db_string_connection = f'postgresql+psycopg2://{self.__db_user}:{self.__db_pass}@{self.__db_host}/{self.__db_name}'
        print(self.__db_string_connection)
        self.__engine = create_engine(self.__db_string_connection)

    @property
    def _engine(self):
        return self.__engine
    
    def closeConnection(self):
        try:
            self.__engine.dispose()
        except:
            print("There was an error closing engine")