import pandas as pd
import streamlit as st

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


DRIVER = "ODBC Driver 18 for SQL Server"


def conectar():
    if "database" not in st.secrets:
        raise RuntimeError(
            "Banco de dados indisponível neste ambiente "
            "(secrets não configurados)."
        )

    cfg = st.secrets["database"]

    odbc = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={cfg['server']};"
        f"DATABASE={cfg['database']};"
        f"UID={cfg['user']};"
        f"PWD={cfg['password']};"
        "TrustServerCertificate=yes;"
    )

    return create_engine(
        "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)
    )


def consultar(sql):
    with conectar().connect() as conexao:
        return pd.read_sql(text(sql), conexao)