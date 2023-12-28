# ostrovok_parsing

Проект состоит из парсера сайта(main.py) ostrovok.ru(бронирование отелей) с возможностью фильтрации данных по параметрам GET-запроса. Парсинг организован на Selenium, WebDriver использовался(и находится в репозитории) для Chrome версии 112.   

Для более удобного взаимодействия имеется GUI(gui.py) с возможность выбора всех возможных фильтров на сайте, с выводом информации по отелям в табличном виде и сохранение в CSV, EXCEL файлы(save_data.py).

## Как запустить проект:

В терминале, перейдите в каталог, в который будет загружаться приложение:
```
cd 
```
Клонируйте репозиторий:
```
git clone git@github.com:VladislavYar/ostrovok_parsing.git
```

Установить Chrome версии 112(или обновить драйвер с оффициального сайта)

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить файл main.py для вывода данных в консоль, gui.py для вывода в таблицу или сохранение в файл

## Cтек проекта
Python v3.11, Selenium, PyQt5
