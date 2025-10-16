
import pandas as pd

FILE_ID = "16khQQ4-SW6tCEDuxzqiIa9_bpzjw3V7p"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

raw_data = pd.read_csv(file_url)     # читаем файл
print(raw_data.head(10))         # выводим на экран первые 10 строк для проверки