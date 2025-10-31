import pandas as pd
import numpy as np

FILE_ID = "16khQQ4-SW6tCEDuxzqiIa9_bpzjw3V7p"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
df = pd.read_csv(file_url)  # загрузка файла

raw_data = pd.read_csv(file_url)     # читаем файл
print(raw_data.head(10))         # выводим на экран первые 10 строк для проверки

def clean_and_convert_pdb_data(df):
    """
    Функция для очистки и приведения типов данных в датасете PDB
    """

    # Создаем копию датафрейма для работы
    df_clean = df.copy()

    # 1. Обработка числовых колонок с возможными пропусками и некорректными значениями

    # residueCount - количество остатков (целое число)
    df_clean['residueCount'] = pd.to_numeric(df_clean['residueCount'], errors='coerce').fillna(0).astype('Int64')

    # resolution - разрешение (float)
    # Заменяем запятые на точки и конвертируем в float
    df_clean['resolution'] = (
        df_clean['resolution']
        .astype(str)
        .str.replace(',', '.')
        .replace('nan', np.nan)
        .replace('None', np.nan)
        .replace('', np.nan)
        .astype(float)
    )

    # structureMolecularWeight - молекулярная масса (float)
    df_clean['structureMolecularWeight'] = pd.to_numeric(
        df_clean['structureMolecularWeight'], errors='coerce'
    )

    # crystallizationTempK - температура кристаллизации (float)
    df_clean['crystallizationTempK'] = pd.to_numeric(
        df_clean['crystallizationTempK'], errors='coerce'
    )

    # densityMatthews - плотность Мэтьюза (float)
    df_clean['densityMatthews'] = (
        df_clean['densityMatthews']
        .astype(str)
        .str.replace(',', '.')
        .replace('nan', np.nan)
        .replace('None', np.nan)
        .replace('', np.nan)
        .astype(float)
    )

    # densityPercentSol - процент растворителя (float)
    df_clean['densityPercentSol'] = pd.to_numeric(
        df_clean['densityPercentSol'], errors='coerce'
    )

    # phValue - pH значение (float)
    df_clean['phValue'] = pd.to_numeric(df_clean['phValue'], errors='coerce')

    # publicationYear - год публикации (целое число)
    df_clean['publicationYear'] = pd.to_numeric(
        df_clean['publicationYear'], errors='coerce'
    ).fillna(0).astype('Int64')

    # 2. Обработка текстовых колонок

    # structureId - идентификатор структуры (строка)
    df_clean['structureId'] = df_clean['structureId'].astype(str)

    # classification - классификация (категория)
    df_clean['classification'] = (
        df_clean['classification']
        .fillna('UNKNOWN')
        .astype('category')
    )

    # experimentalTechnique - экспериментальная техника (категория)
    df_clean['experimentalTechnique'] = (
        df_clean['experimentalTechnique']
        .fillna('UNKNOWN')
        .astype('category')
    )

    # macromoleculeType - тип макромолекулы (категория)
    df_clean['macromoleculeType'] = (
        df_clean['macromoleculeType']
        .fillna('UNKNOWN')
        .astype('category')
    )

    # crystallizationMethod - метод кристаллизации (категория)
    df_clean['crystallizationMethod'] = (
        df_clean['crystallizationMethod']
        .fillna('UNKNOWN')
        .astype('category')
    )

    # pdbxDetails - детали (строка)
    df_clean['pdbxDetails'] = df_clean['pdbxDetails'].astype(str)

    # sequences - последовательности (строка)
    df_clean['sequences'] = df_clean['sequences'].astype(str)

    # 3. Оптимизация типов данных для экономии памяти

    # Преобразование категориальных колонок
    categorical_columns = ['classification', 'experimentalTechnique',
                           'macromoleculeType', 'crystallizationMethod',
                           'resolution_category']

    for col in categorical_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype('category')

    # Оптимизация числовых типов
    int_columns = ['residueCount', 'publicationYear', 'sequence_length']
    for col in int_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype('Int64')

    return df_clean


def analyze_data_types(df):
    """
    Функция для анализа типов данных в датафрейме
    """
    print("=== АНАЛИЗ ТИПОВ ДАННЫХ ===")
    print(f"Общее количество строк: {len(df)}")
    print(f"Общее количество колонок: {len(df.columns)}")
    print("\nТипы данных после преобразования:")
    print(df.dtypes)

    print("\nИнформация о памяти:")
    print(df.info(memory_usage='deep'))

    print("\nПропущенные значения:")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    missing_info = pd.DataFrame({
        'Пропущено': missing_data,
        'Процент': missing_percent
    })
    print(missing_info[missing_info['Пропущено'] > 0])


# Основной скрипт
if __name__ == "__main__":

    # Очистка и преобразование данных
    df_clean = clean_and_convert_pdb_data(df)

    # Анализ результатов
    analyze_data_types(df_clean)

    # Дополнительная статистика
    print("\n=== СТАТИСТИКА ПО ЧИСЛОВЫМ КОЛОНКАМ ===")
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    print(df_clean[numeric_columns].describe())

    print("\n=== СТАТИСТИКА ПО КАТЕГОРИАЛЬНЫМ КОЛОНКАМ ===")
    categorical_columns = df_clean.select_dtypes(include=['category']).columns
    for col in categorical_columns:
        print(f"\n{col}:")
        print(df_clean[col].value_counts().head(10))

    # Сохранение обработанных данных
    output_filename = 'pdb_data_cleaned.csv'
    df_clean.to_csv(output_filename, index=False)
    print(f"\nОбработанные данные сохранены в файл: {output_filename}")

    # Демонстрация нескольких строк обработанных данных
    print("\n=== ПЕРВЫЕ 5 СТРОК ОБРАБОТАННЫХ ДАННЫХ ===")
    pd.set_option('display.max_columns', None)
    print(df_clean.head())
