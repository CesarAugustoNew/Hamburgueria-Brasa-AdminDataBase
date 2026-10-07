import pandas as pd
import streamlit as st

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


SERVIDOR = st.secrets["database"]["server"]
BANCO = st.secrets["database"]["database"]
USUARIO = st.secrets["database"]["user"]
SENHA = st.secrets["database"]["password"]
DRIVER = "ODBC Driver 18 for SQL Server"


def conectar():
    odbc = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BANCO};"
        f"UID={USUARIO};"
        f"PWD={SENHA};"
        "TrustServerCertificate=yes;"
    )

    return create_engine(
        "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)
    )


def consultar(sql):
    with conectar().connect() as conexao:
        return pd.read_sql(text(sql), conexao)