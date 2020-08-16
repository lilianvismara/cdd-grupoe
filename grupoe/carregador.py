"""
Popula tabelas do banco de dados com as informações do CSV
"""
import os

import pandas as pd

DATABASE = os.getenv('DATABASE', 'covid19_casos_brasil')
USER = os.getenv('USER', 'user_name')
HOST = os.getenv('HOST', 'localhost')
PASSWORD = os.getenv('PASSWORD', 'user_password')

ESTADOS = ['SP', 'ES', 'ES']
CIDADES = ['São Paulo', 'Guarapari', 'Dois Vizinhos', 'Piracicaba', 'Curitiba']

CASOS_COVID19 = pd.read_csv("dados/covid19_casos_brasil.csv")

FILTRO_CIDADES = (CASOS_COVID19['state'].isin(ESTADOS)) & \
                 (CASOS_COVID19['place_type'] == 'city') & \
                 (CASOS_COVID19['city'].isin(CIDADES))

CASOS_COVID19_CIDADES = CASOS_COVID19[FILTRO_CIDADES]
