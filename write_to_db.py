from sqlalchemy import create_engine, text, inspect
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_url = os.getenv("DB_URL")
db_port = os.getenv("DB_PORT")
db_root_base = os.getenv("DB_ROOT_BASE")

assert db_url

data = pd.read_parquet(r"data/pdb_data_cleaned.parquet").iloc[:100]
data.info()
new_column_names = {col: col.lower() for col in data.columns}
data.rename(columns=new_column_names, inplace=True)
data.info()

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_root_base}",
    pool_recycle=3600,
)
data.to_sql(
    name="yangalin",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False,
)

with engine.begin() as conn:
    rows = conn.execute(text("ALTER TABLE public.yangalin ADD PRIMARY KEY (id)"))

inspector = inspect(engine)
columns = inspector.get_columns("yangalin", schema="public")
print("columns")
print({col["name"]: col["type"] for col in columns})
print("data")
print(pd.read_sql_table("yangalin", con=engine).head())
