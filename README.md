Ссылка на датасет: https://drive.google.com/file/d/1aXF6kBAxg2cA-j0MSgPzUoL4QQiDoJVK/view?usp=sharing - cобирала данные с сайта PubChem через API.

Датасет с платформы Kaggle: https://drive.google.com/file/d/1ZAaB3w-ssykhQXt8ikc9w4RM3seucxpQ/view?usp=sharing.

# Project Structure
```
my_project/
|
|--- notebooks/
|    |___ EDA.py
|
|--- src/
|    |--- __init__.py
|    |--- extract.py
|    |--- load.py
|    |--- main.py
|    |___ transform.py
|
|--- .gitignore
|--- poetry.lock
|--- pyproject.toml
|___ README.md
```

# Создание переменного окружения (conda + poetry)
Для загрузки miniconda через Homebrew:
```brew install --cask miniconda```

### Создание виртуального окружения и активация c помощью Conda:
* ```conda create -n my_env python=3.13 pip```
* Инициализируем все поддерживаемые оболочки: ```conda init --all``` -> открыть новый терминал
* ```conda activate my_env```

Посмотреть существующие виртуальные окружения:
```conda env list```

### Добавление необходимых библиотек с помощью Poetry:
* Устанавливаем poetry ```pip install poetry```
* Создание пакета my_project в my_project: ```poetry new my_project```
* ```cd my_project``` - переход в директорию
* ```poetry add jupyterlab pandas matplotlib wget``` - добавление новых зависимостей в проект
* ```poetry install --no-root``` - установка всех библиотек из pyproject.toml

Скрипт выгрузки файла из Google Drive и вывод на экран первых 10 строк лежит в ```src/experiments/data_loader.py```

Также в этом файле представлено приведение типов и сохранение в формат .csv

Запуск скрипта:
```python3 src/experiments/data_loader.py```

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
