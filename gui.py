import sys
from datetime import datetime, timedelta

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QThread, QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from main import ParsingWebsiteOstrovok
from save_data import SaveFile

CITY = {'Москва': 'moscow', 'Тула': 'tula'}
TYPE_GROUP = {
    'Отели, меблированные комнаты': 'hotel',
    'Хостелы, жилые помещения': 'hostel', 'Апартаменты': 'apart',
    'Апарт-отели': 'apart_hotel', 'Гостевые дома': 'guesthouse',
    'Коттеджи, виллы, бунгало': 'cottage_villa_bungalow',
    'Кемпинги': 'camping', 'Глэмпинги': 'glamping',
}
AMENITIES = {
    'Бесплатный интернет': 'has_internet', 'Трансфер': 'has_airport_transfer',
    'Парковка': 'has_parking', 'Бассейн': 'has_pool', 'Фитнес': 'has_fitness',
    'Бар или ресторан': 'has_meal', 'Конференц-зал': 'has_busyness',
    'Спа-услуги': 'has_spa', 'Горнолыжный склон рядом': 'has_ski',
    'Пляж рядом': 'beach', 'Джакузи': 'has_jacuzzi',
    'Зарядка электромобилей': 'has_ecar_charger',
    'Кондиционер': 'air-conditioning',
    'Ванная комната в номере': 'private-bathroom', 'Кухня': 'kitchen',
    'Вид из окна': 'with-view', 'Подходит для детей': 'has_kids',
    'Для гостей с ограниченными возможностями': 'has_disabled_support',
    'Разрешено с домашними животными': 'has_pets',
    'Можно курить': 'has_smoking',
}
MEAL_TYPES = {
    'Питание не включено': 'nomeal', 'Завтрак включён': 'breakfast',
    'Завтрак + обед или ужин включены': 'halfBoard',
    'Завтрак, обед и ужин включены': 'fullBoard',
    'Всё включено': 'allInclusive',
}
REVIEWS_RATING = {
    'Супер: 9+': '9', 'Отлично: 8+': '8', 'Очень хорошо: 7+': '7',
    'Хорошо: 6+': '6', 'Неплохо: 5+': '5'
}
PAYMENT = {
    'Для бронирования не нужна карта': 'nocardrequired',
    'Есть бесплатная отмена': 'freecancellation',
    'Оплата сейчас': 'site', 'Оплата на месте': 'hotel'
}
BEDDING_TYPES = {
    'Двуспальная кровать': 'double', 'Отдельные кровати': 'single'
}
SORT = {
    'По популярности': '', 'Сначала дешевые': 'price.asc',
    'Сначала дорогие': 'price', 'Начиная от центра города': 'destination.asc',
    'Сначала с высокой оценкой': 'rating'
}


class LoadDataHotalThread(QThread):
    """Поток для поиска данных."""
    load_finished = pyqtSignal(object)

    def __init__(self, parser: ParsingWebsiteOstrovok, url: str) -> None:
        super().__init__()
        self.parser = parser
        self.url = url

    def run(self) -> None:
        """Поиск данных по запросу."""
        data = self.parser.get_hotel_data(self.url)
        self.load_finished.emit(data)


class SearchHotel():
    """Поиск и вывод данных по отелям."""
    def __init__(self, win):
        self.win = win
        self.win.search.clicked.connect(self.search_hotel)
        self.win.CSV.triggered.connect(lambda: self._file_save('*.csv'))
        self.win.Excel.triggered.connect(lambda: self._file_save('*.xls'))
        self.msg = QMessageBox()
        self.save = SaveFile()
        self.data = {}
        self._setting()

    def _file_save(self, name_extension):
        """Сохраняет данные в файл."""
        dir = QFileDialog.getSaveFileName(filter=name_extension)
        path = dir[0]
        if dir[1] == '*.csv':
            self.save.to_csv(self.data, path)
        elif dir[1] == '*.xls':
            self.save.to_excel(self.data, path)

    def _setting(self):
        """Настройка первоночального состояния."""
        today = datetime.today()
        date_now = int(today.year), int(today.month), int(today.day)
        tomorrow = today + timedelta(days=1)
        date_tomorrow = (
            int(tomorrow.year), int(tomorrow.month), int(tomorrow.day)
        )
        q_date_now = QDate(*date_now)
        q_date_tomorrow = QDate(*date_tomorrow)
        self.win.beginning_day.setDate(q_date_now)
        self.win.end_day.setDate(q_date_tomorrow)

        q_date_now = QDate(*date_now)
        q_date_tomorrow = QDate(*date_tomorrow)
        self.win.beginning_day.setMinimumDate(q_date_now)
        self.win.end_day.setMinimumDate(q_date_tomorrow)

        price_validator = QIntValidator(100, 100000)
        self.win.min_price.setValidator(price_validator)
        self.win.max_price.setValidator(price_validator)

        guest_validator = QIntValidator(1, 9)
        self.win.guest.setValidator(guest_validator)

        self.win.city.setCurrentItem(win.city.item(0))
        self.win.sort.setCurrentItem(win.sort.item(0))

        self.win.save.setEnabled(False)

    def data_output_table(self, data) -> None:
        """Выводит данные в таблицу."""
        count_hotels = len(data)
        count_column = self.win.parsing_data.columnCount()
        try:
            name_keys = list(data[0].keys())
            self.win.parsing_data.setRowCount(count_hotels)
            for i in range(count_hotels):
                for j in range(count_column):
                    item = QtWidgets.QTableWidgetItem(data[i][name_keys[j]])
                    win.parsing_data.setItem(i, j, item)
            self.win.save.setEnabled(True)
            self.data = data
        except IndexError:
            self.msg.setWindowTitle("Info")
            self.msg.setText("По Вашему запросу ничего не найдено.")
            self.msg.setIcon(QMessageBox.Icon.Information)
            self.msg.setStandardButtons(QMessageBox.StandardButton.Cancel)
            self.msg.exec()
        self.win.search.setEnabled(True)
        self.win.search.setText('Поиск')

    def _get_selected_items(self, items: list, items_filters: dict) -> str:
        """Формирует строку для поиска из выбранных элементов в таблице."""
        values = []
        for item in items:
            values.append(items_filters[item.text()])
        values = ".".join(values)
        return values

    def _generates_data_url(self) -> tuple:
        """Формирует данные для поиска."""
        beginning_day = win.beginning_day.date().toString('dd.MM.yyyy')
        end_day = win.end_day.date().toString('dd.MM.yyyy')
        date = f'{beginning_day}-{end_day}'

        min_price = self.win.min_price.text()
        max_price = self.win.max_price.text()
        price = f'{min_price}-{max_price}.one'
        if int(min_price) == 100 and int(max_price) == 100000:
            price = 'one'

        guest = self.win.guest.text()

        page = 1

        name_sort = self.win.sort.selectedItems()[0].text()
        sort = SORT[name_sort]

        name_city = self.win.city.selectedItems()[0].text()
        city = CITY[name_city]

        values = self.win.type_placement.selectedItems()
        type_group = self._get_selected_items(values, TYPE_GROUP)

        values = self.win.in_hotel.selectedItems()
        values.extend(self.win.in_room.selectedItems())
        values.extend(self.win.features_placement.selectedItems())
        amenities = self._get_selected_items(values, AMENITIES)

        values = self.win.food.selectedItems()
        meal_types = self._get_selected_items(values, MEAL_TYPES)

        values = self.win.rating.selectedItems()
        reviews_rating = self._get_selected_items(values, REVIEWS_RATING)

        values = self.win.payment_booking.selectedItems()
        payment = self._get_selected_items(values, PAYMENT)

        values = self.win.bedding.selectedItems()
        bedding_types = self._get_selected_items(values, BEDDING_TYPES)

        values = (
            city, date, guest, amenities, bedding_types, meal_types, payment,
            page, price, reviews_rating, type_group, sort
        )
        return values

    def search_hotel(self) -> None:
        """Создаёт поток поиска."""
        self.win.save.setEnabled(False)
        self.win.search.setEnabled(False)
        self.win.search.setText('Ведётся поиск...')
        parser = ParsingWebsiteOstrovok()
        data = self._generates_data_url()
        url = parser.get_url(*data)
        self.thread = LoadDataHotalThread(parser, url)
        self.thread.load_finished.connect(self.data_output_table)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


if '__main__' == __name__:
    app = QtWidgets.QApplication([])
    win = uic.loadUi("gui.ui")
    win.show()

    search = SearchHotel(win)

    sys.exit(app.exec())
