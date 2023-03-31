
import pandas as pd
import sqlalchemy
import os

engine_connect = sqlalchemy.create_engine("postgresql://env_master:M123xyz@localhost:5433/env_groundwater").connect()
output = '/Users/ashikmahmud/MyDocuments/Personal/GEO2023EX/Final/output.csv'

df = pd.read_csv(output)

with engine_connect as connect:
    df.to_sql('Waterlevel', con=connect, if_exists='append', index=False)
os.remove(output)