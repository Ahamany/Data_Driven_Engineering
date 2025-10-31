import pandas as pd

FILE_ID = "16khQQ4-SW6tCEDuxzqiIa9_bpzjw3V7p"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
df = pd.read_csv(file_url)  # загрузка файла

raw_data = pd.read_csv(file_url)     # читаем файл
print(raw_data.head(10))         # выводим на экран первые 10 строк для проверки

print("\n Общая информация о датасете:")
print(df.info())  # просмотр всех типов столбцов и значений, в том числе сколько NaN

print("\n Кол-во пропусков по столбцам:")
print(df.isnull().sum())  # посчитать пустые значения для всех столбцов

print("\n Уникальные значения для текстовых колонок:")
for col in df.select_dtypes(include=["object"]).columns:
    print(col, df[col].nunique(), df[col].unique()[:10])  # просмотр уникальных значений

print("\n Статистика для числовых колонок:")
print(df.describe())  # для числовых колонок просмотр минимума, максимума и среднего
