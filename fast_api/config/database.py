import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Para manipular la base de datos

sqlite_file_name = "../database.sqlite" # Nombre de la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__)) # Ruta del folder que contiene la base de datos

databse_url = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}" # Ruta absoluta al archivo de la base de datos

engine = create_engine(databse_url, echo=True) # Crea la base de datos
session = sessionmaker(bind=engine) # Se conecta a la base de datos
base = declarative_base() # Manipulacion de la base de datos