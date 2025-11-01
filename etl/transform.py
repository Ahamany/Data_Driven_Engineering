import numpy as np
import pandas as pd


def clean_and_convert_pdb_data(df):

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
    df_clean.columns = ['id'] + list(df_clean.columns[1:])

    return df_clean
