import pandas as pd
from sqlalchemy import create_engine, text, inspect
from dataclasses import dataclass
import os


def save_data_to_parquet(df: pd.DataFrame, file_path: str) -> None:
    df.to_parquet(file_path, engine='pyarrow')

@dataclass
class DBCreds:
    user: str
    password: str
    url: str
    port: str
    root_base: str

def load_db_creds() -> DBCreds:
    return DBCreds(
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_URL"),
        os.getenv("DB_PORT"),
        os.getenv("DB_ROOT_BASE")
    )

def make_engine(creds: DBCreds):
    return create_engine(
    f"postgresql+psycopg2://{creds.user}:{creds.password}@{creds.url}:{creds.port}/{creds.root_base}",
        pool_recycle=3600,
    )

def write_data_to_database(df: pd.DataFrame, creds: DBCreds) -> None:
    new_column_names = {col: col.lower() for col in df.columns}
    df.rename(columns=new_column_names, inplace=True)

    engine = make_engine(creds)

    df.to_sql(
        name="yangalin",
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
    )

    with engine.begin() as conn:
        rows = conn.execute(text("ALTER TABLE public.yangalin ADD PRIMARY KEY (id)"))

def validate_db_data(creds: DBCreds) -> bool:
    engine = make_engine(creds)
    inspector = inspect(engine)
    columns = inspector.get_columns("yangalin", schema="public")
    print("columns")
    print({col["name"]: col["type"] for col in columns})
    print("data")
    print(pd.read_sql_table("yangalin", con=engine).head())
