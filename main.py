import re
from datetime import datetime, timedelta
from pprint import pprint

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import (
    NoSuchElementException, NoSuchWindowException, WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager

from constants import HOTELS_ON_PAGE


class ParsingWebsiteOstrovok():
    """Парсинг по сайту ostrovok.ru."""
    def __init__(self) -> None:
        options = ChromeOptions()
        options.add_argument("log-level=3")
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = Chrome(options=options, service=service)
        self.website = 'https://ostrovok.ru/hotel/russia'
        self.count_hotel = 0

    def forms_hotel_data(self, html_hotel_data: list) -> list[dict]:
        """Формирует данные по каждому отелю."""
        html_classes = (
            'zen-hotelcard-name-link', 'zen-hotelcard-rate-price-value',
            'zen-hotelcard-rating-wrapper-extended',
            'zen-hotelcard-distance', 'zenimage-content',
        )
        hotels = []
        for data in html_hotel_data:
            try:
                name = data.find_element(By.CLASS_NAME, html_classes[0]).text
            except NoSuchElementException:
                name = 'Название отсутсвует'
            try:
                URL = data.find_element(By.CLASS_NAME,
                                        html_classes[0]).get_attribute('href')
            except NoSuchElementException:
                URL = 'URL отсуствует'
            try:
                price = data.find_element(By.CLASS_NAME,
                                          html_classes[1]).text.replace(' ',
                                                                        '')
            except NoSuchElementException:
                price = 'Цена отсутсвует'
            try:
                rating_reviews = (
                    data.find_element(By.CLASS_NAME,
                                      html_classes[2]).text.split('\n')
                    )
                try:
                    reviews = rating_reviews[1]
                    rating = rating_reviews[0]
                except IndexError:
                    rating = rating_reviews[0]
                    reviews = 'Отзывы отсутсвуют'
            except NoSuchElementException:
                rating = 'Оценка отсутсвует'
                reviews = 'Отзывы отсутсвуют'
            try:
                distance = data.find_element(By.CLASS_NAME,
                                             html_classes[3]).text
            except NoSuchElementException:
                distance = 'Расстояние до центра отсутсвует'
            try:
                img = data.find_element(By.CLASS_NAME,
                                        html_classes[4]).get_attribute('src')
            except NoSuchElementException:
                img = 'Фото отсутсвует'
            hotel_data = {
                'Название': name, 'URL': URL, 'Цена': price, 'Рейтинг': rating,
                'Отзывы': reviews, 'Расстояние': distance, 'Фото': img,
                }
            hotels.append(hotel_data)
        return hotels

    def _search_hotel_new_page_data(self) -> list[dict] or list:
        """Рекурсия для поиска данных, на новой странице."""
        if self.page < self.count_page:
            new_page = self.page + 1
            url = self.get_url(
                self.city, self.date, self.guests, self.amenities,
                self.bedding_types, self.meal_types, self.payment,
                new_page, self.price, self.reviews_rating,
                self.group, self.sort
            )
            return self.get_hotel_data(url)
        self.driver.quit()
        return []

    def search_hotel_data(self) -> list[dict] or list:
        """Ищет каждый отель."""
        html_class = 'hotel-wrapper'
        html_hotel_data = self.driver.find_elements(By.CLASS_NAME,
                                                    html_class)
        data = self.forms_hotel_data(html_hotel_data)

        if not self.count_hotel:
            try:
                html_class = ('zenserpresult-header')
                html_hotel_count = self.driver.find_element(By.CLASS_NAME,
                                                            html_class)
                self.count_hotel = int(re.findall(r'\d+',
                                                  html_hotel_count.text)[0])
                self.count_page = self.count_hotel / HOTELS_ON_PAGE
            except IndexError:
                self.driver.quit()
                return []

        data.extend(self._search_hotel_new_page_data())

        return data

    def get_hotel_data(self, url: str) -> list[dict] or list:
        """Возвращает данные по отелям."""
        try:
            self.driver.get(url)
            return self.search_hotel_data()
        except (WebDriverException, NoSuchWindowException):
            return []

    def _get_valid_dates() -> str:
        """Фомирует валидную дефолтную дату."""
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        return f'{today.strftime("%d.%m.%Y")}-{tomorrow.strftime("%d.%m.%Y")}'

    def get_url(self, city='tula', date=_get_valid_dates(), guests='1',
                amenities='', bedding_types='', meal_types='', payment='',
                page=1, price='one', reviews_rating='', group='', sort=''
                ) -> str:
        """Формирует URL."""
        (self.city, self.date, self.guests, self.amenities,
         self.bedding_types, self.meal_types, self.payment, self.page,
         self.price, self.reviews_rating, self.group, self.sort) = (
            city, date, guests, amenities, bedding_types, meal_types, payment,
            page, price, reviews_rating, group, sort
            )
        url = (f'{self.website}/{city}/?dates={date}&guests={guests}'
               f'&amenities={amenities}&bedding_types={bedding_types}'
               f'&meal_types={meal_types}&payment={payment}'
               f'&page={page}&price={price}&reviews_rating={reviews_rating}'
               f'&type_group={group}&sort={sort}')
        return url


if '__main__' == __name__:
    parser = ParsingWebsiteOstrovok()
    url = parser.get_url()
    pprint(parser.get_hotel_data(url))
