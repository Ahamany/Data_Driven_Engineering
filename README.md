Data_Driven_Engineering

Репозиторий проекта ITMO Data Driven Engineering.

Набор данных содержит информацию об аминокислотных последовательностях белков и их свойствах из Protein Data Bank
Link: https://docs.google.com/spreadsheets/d/1_RF8CV2Ej1UKbFwhVzy3kx5Q41cvHS62_0Is_Yv5YUU/edit?usp=sharing

# Project Structure
```
my_project/
|
|--- notebooks/
|    |___ EDA.py
|
|--- etl/
|    |--- __init__.py
|    |--- extract.py
|    |--- load.py
|    |--- main.py
|    |___ transform.py
|
|--- .gitignore
|--- poetry.lock
|--- pyproject.toml
|___ write_to_db.py
|--- data_loader.py
|___ README.md
```

# Создание переменного окружения (conda + poetry)
Для загрузки miniconda (Windows):
url https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
start /wait "" .\miniconda.exe /S
del .\miniconda.exe

### Создание виртуального окружения и активация c помощью Conda:
* ```conda create -n my_env python=3.13 pip```
* Инициализируем conda: ```conda init``` -> открыть новый терминал
* ```conda activate my_env```

Посмотреть существующие виртуальные окружения:
```conda env list```

### Добавление необходимых библиотек с помощью Poetry:
* Устанавливаем poetry ```pip install poetry```
* Создание пакета my_project в my_project: ```poetry new my_project```
* ```cd my_project``` - переход в директорию
* ```poetry add jupyterlab pandas matplotlib wget``` - добавление новых зависимостей в проект
* ```poetry install --no-root``` - установка всех библиотек из pyproject.toml

Скрипт выгрузки файла из Google Drive и вывод на экран первых 10 строк лежит в ```data_loader.py```

Также в этом файле представлено приведение типов и сохранение в формат .csv и .parcuet

Запуск скрипта:
```python3 data_loader.py```

Ниже представлен скриншот первых 10 строк датафрейма:
![data_cardiovascular_risk](photo/df_head(10).png)

<details>
<summary>Итоговые типы столбцов</summary>
<img src="photo/df_types.png" alt="drawing" width="200"/>
</details>

### black
Установка: ```poetry add --group dev black```

Запуск (форматирование кода):

```poetry run black src/experiments/data_loader.py```

### Загрузка датасета в базу данных
Запуск скрипта:
```python3 src/experiments/write_to_db.py```

### Рендер ноутбука 
[Ноутбук с EDA](https://nbviewer.org/github/Margo2512/data_driven_engineering/blob/main/notebooks/EDA.ipynb)

### Пакет etl
Поддерживает аргументы командной строки, `python3 src/etl/main.py --help` чтобы посмотреть доступные.

Запуск всего ETL пайплайна с загрузкой в базу данных
`python3 src/etl/main.py etl --file_id <file_id>`

Проверка таблицы в базе данных и вывод нескольких первых значений
`python3 src/etl/main.py validate_db`

Необходимо указать такие переменные окружения:
- DB_USER
- DB_PASSWORD
- DB_URL
- DB_PORT
- DB_ROOT_BASE

Можно сделать это с помощью .env файла, используя флаг  `--use_dotenv`
