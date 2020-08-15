"""
Conecta no banco de dados postgresql
Cria um banco de dados chamado "covid19_casos_brasil" caso não exista
Cria as tabelas "city" e "cases"
"""

import os

import psycopg2
from psycopg2 import sql
from psycopg2._psycopg import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE = os.getenv('DATABASE', 'covid19_casos_brasil')
USER = os.getenv('USER', 'user_name')
HOST = os.getenv('HOST', 'localhost')
PASSWORD = os.getenv('PASSWORD', 'user_password')
TABLES = [
    {'name': 'city',
     'sql': 'CREATE TABLE city(city_ibge_code int NOT NULL, city varchar(255), state varchar(2), estimated_population_2019 int, PRIMARY KEY (city_ibge_code))'},
    {'name': 'cases',
     'sql': 'CREATE TABLE cases(city_ibge_code int NOT NULL, date date, epidemioloical_wek int, last_available_confirmed int, last_available_deths int, last_available_death_rate numeric, last_available_confirmed_per_100k_inhabitants numeric, CONSTRAINT PK_Cases PRIMARY KEY (city_ibge_code, date), FOREIGN KEY (city_ibge_code) REFERENCES city(city_ibge_code))'}
]


def connect_db():
    try:
        con = psycopg2.connect(
            dbname=DATABASE,
            user=USER,
            host='',
            password=PASSWORD)
        cur = con.cursor()
    except OperationalError:
        con = psycopg2.connect(
            dbname='postgres',
            user=USER,
            host='',
            password=PASSWORD)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
        cur = con.cursor()
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(DATABASE))
        )
    return cur


def check_tables(cur):
    for table in TABLES:
        # Verifica se a tabela existe
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table['name'],))
        if not cur.fetchone()[0]:
            cur.execute(table['sql'])


cur = connect_db()
check_tables(cur)

pass
