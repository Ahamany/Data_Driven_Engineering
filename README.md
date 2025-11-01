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
(curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe start /wait "" .\miniconda.exe /S del .\miniconda.exe)

### Создание виртуального окружения и активация c помощью Conda:
* ```conda create -n my_env python=3.13```
* Инициализируем conda: ```conda init``` -> открыть новый терминал
* ```conda activate my_env```

Посмотреть существующие виртуальные окружения:
```conda env list```

### Добавление необходимых библиотек с помощью Poetry:
* Устанавливаем poetry ```pip install poetry```
* Создание пакета my_project в my_project: ```poetry new my_project```
* ```cd my_project``` - переход в директорию
* ```poetry add jupyterlab pandas matplotlib``` - добавление новых зависимостей в проект
* ```poetry install --no-root``` - установка всех библиотек из pyproject.toml

Скрипт выгрузки файла из Google Drive и вывод на экран первых 10 строк лежит в ```data_loader.py```

Также в этом файле представлено приведение типов и сохранение в формат .csv и .parcuet

Запуск скрипта:
```python3 data_loader.py```

Ниже представлен скриншот первых 10 строк датафрейма:

<img width="563" height="248" alt="image" src="https://github.com/user-attachments/assets/d4c65ed5-20cc-4b0f-8a3b-7d9624d52402" />

Итоговые типы столбцов

<img width="466" height="598" alt="image" src="https://github.com/user-attachments/assets/bfafd95a-21e9-4914-a32c-703b64e0df5c" />


### black
Установка: ```poetry add --group dev black```

Запуск (форматирование кода):

```poetry run black data_loader.py```

### Загрузка датасета в базу данных
Запуск скрипта:
```python3 write_to_db.py```

### Рендер ноутбука 
[Ноутбук с EDA](https://github.com/Ahamany/Data_Driven_Engineering/blob/main/notebooks/EDA.ipynb)

### Пакет etl
Поддерживает аргументы командной строки, `python3 etl/main.py --help` чтобы посмотреть доступные.

Запуск всего ETL пайплайна с загрузкой в базу данных
`python3 etl/main.py etl --file_id <file_id>`

Проверка таблицы в базе данных и вывод нескольких первых значений
`python3 etl/main.py validate_db`

Необходимо указать такие переменные окружения:
- DB_USER
- DB_PASSWORD
- DB_URL
- DB_PORT
- DB_ROOT_BASE

Можно сделать это с помощью .env файла, используя флаг  `--use_dotenv`
