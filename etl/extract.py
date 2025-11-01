import pandas as pd


def read_data(file_id: str) -> pd.DataFrame:
    file_url = f"https://drive.google.com/uc?id={file_id}"
    return pd.read_csv(file_url)
