"""
Popula tabelas do banco de dados com as informações do CSV
"""
import os

import pandas as pd
import psycopg2
from psycopg2 import sql

DATABASE = os.getenv('DATABASE', 'covid19_casos_brasil')
USER = os.getenv('USER', 'user_name')
HOST = os.getenv('HOST', 'localhost')
PASSWORD = os.getenv('PASSWORD', 'user_password')

ESTADOS = ['SP', 'ES', 'PR']
CIDADES = ['São Paulo', 'Guarapari', 'Dois Vizinhos', 'Piracicaba', 'Curitiba']

CASOS_COVID19 = pd.read_csv("dados/covid19_casos_brasil.csv")

FILTRO_CIDADES = (CASOS_COVID19['state'].isin(ESTADOS)) & \
                 (CASOS_COVID19['place_type'] == 'city') & \
                 (CASOS_COVID19['city'].isin(CIDADES))

CASOS_COVID19_CIDADES = CASOS_COVID19[FILTRO_CIDADES]
CIDADES = CASOS_COVID19_CIDADES.drop_duplicates(subset=['city']) \
    .set_index('city', drop=False).to_dict(orient='index')
CASOS = CASOS_COVID19_CIDADES.to_dict(orient='index')


def connect_db():
    """
    Conecta no Banco de dados
    :return: Conexão do banco de dados
    """

    con = psycopg2.connect(
        dbname=DATABASE,
        user=USER,
        host='',
        password=PASSWORD)
    return con


def create_cidade(con, cidade):
    """
    Verifica se a cidade já existe, se não existe cria
    :param cur_db: Cursor para o banco de dados
    :param cidade: Dados da cidade
    :return: None
    """
    cur = con.cursor()
    cur.execute("""SELECT 1 FROM city WHERE city_ibge_code = '{}'"""
                .format(int(cidade['city_ibge_code'])))
    cidade_existe = cur.fetchone()

    if not cidade_existe:
        cur.execute("""INSERT INTO city(
        city_ibge_code, 
        city, 
        state, 
        estimated_population_2019) VALUES('{}','{}','{}','{}');"""
                    .format(int(cidade['city_ibge_code']),
                            cidade['city'],
                            cidade['state'],
                            int(cidade['estimated_population_2019'])))
        con.commit()


def create_caso(con, caso):
    """
    Verifica se já existe o caso no banco de dados, se não existir salva
    :param cur_db: Cursor para o banco de dados
    :param caso: Dados do caso
    :return: None
    """

    cur = con.cursor()
    cur.execute("""SELECT 1 FROM cases WHERE city_ibge_code = '{}' AND date = '{}'"""
                .format(int(caso['city_ibge_code']), caso['date']))
    caso_existe = cur.fetchone()

    if not caso_existe:
        cur.execute(sql.SQL("""INSERT INTO cases(
            city_ibge_code, 
            date, 
            epidemiological_week, 
            last_available_confirmed,
            last_available_deaths,
            last_available_death_rate,
            last_available_confirmed_per_100k_inhabitants) VALUES('{}','{}','{}','{}','{}','{}','{}');""".format(
            int(caso['city_ibge_code']),
            caso['date'],
            int(caso['epidemiological_week']),
            int(caso['last_available_confirmed']),
            int(caso['last_available_deaths']),
            float(caso['last_available_death_rate']),
            round(float(caso['last_available_confirmed_per_100k_inhabitants']), 5))))
        con.commit()


if __name__ == '__main__':
    con = connect_db()

    for cidade in CIDADES:
        create_cidade(con, CIDADES[cidade])

    for caso in CASOS:
        create_caso(con, CASOS[caso])
