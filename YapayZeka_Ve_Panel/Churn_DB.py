import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def gercek_veritabanindan_getir():
    baglanti_adresi = os.getenv(
        "DB_URL", 
        "mssql+pyodbc://@EMRH/ChurnCRM_DB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    
    engine = create_engine(baglanti_adresi)
    
    sorgu = "SELECT * FROM Musteriler" 
    
    df = pd.read_sql(sorgu, engine)
    return df