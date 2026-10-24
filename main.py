import re
from datetime import datetime, timedelta
from pprint import pprint

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchWindowException,
    TimeoutException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager

from constants import ARGS_OPTION


def _get_valid_dates() -> str:
    """Фомирует валидную дефолтную дату."""
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    return f'{today.strftime("%d.%m.%Y")}-{tomorrow.strftime("%d.%m.%Y")}'


class ParsingWebsiteOstrovok:
    """Парсинг по сайту ostrovok.ru."""

    def __init__(self) -> None:
        options = ChromeOptions()
        for option in ARGS_OPTION:
            options.add_argument(option)
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = Chrome(options=options, service=service)
        self.website = "https://ostrovok.ru/hotel/russia"

    def forms_hotel_data(self, html_hotel_data: list) -> list[dict]:
        """Формирует данные по каждому отелю."""
        html_classes = (
            '[data-testid="hotel-card-name"]',
            '[data-testid="hotel-card-price-value"]',
            '[data-testid="hotel-card-rating-content"]',
            '[data-testid="hotel-card-distance-center"]',
            'img[class*="GalleryImage_item"]',
            '[class*="HotelRating_reviewsCount"]',
        )
        hotels = []
        for data in html_hotel_data:
            try:
                name = data.find_element(By.CSS_SELECTOR, html_classes[0]).text
            except NoSuchElementException:
                name = "Название отсутсвует"
            try:
                URL = data.find_element(By.CSS_SELECTOR, html_classes[0]).get_attribute(
                    "href"
                )
            except NoSuchElementException:
                URL = "URL отсуствует"
            try:
                price = data.find_element(By.CSS_SELECTOR, html_classes[1]).text
            except NoSuchElementException:
                price = "Цена отсутсвует"
            try:
                rating = data.find_element(By.CSS_SELECTOR, html_classes[2]).text
            except NoSuchElementException:
                rating = "Оценка отсутсвует"
            try:
                reviews = data.find_element(By.CSS_SELECTOR, html_classes[-1]).text
            except NoSuchElementException:
                reviews = "Отзывы отсутсвуют"
            try:
                distance = data.find_element(By.CSS_SELECTOR, html_classes[3]).text
            except NoSuchElementException:
                distance = "Расстояние до центра отсутсвует"
            try:
                img = data.find_element(By.CSS_SELECTOR, html_classes[4]).get_attribute(
                    "src"
                )
            except NoSuchElementException:
                img = "Фото отсутсвует"
            hotel_data = {
                "Название": name,
                "URL": URL,
                "Цена": price,
                "Рейтинг": rating,
                "Отзывы": reviews,
                "Расстояние": distance,
                "Фото": img,
            }
            hotels.append(hotel_data)
        return hotels

    def _search_hotel_new_page_data(self) -> list[dict] | list:
        """Рекурсия для поиска данных, на новой странице."""
        new_page = self.page + 1
        url = self.get_url(
            self.city,
            self.date,
            self.guests,
            self.amenities,
            self.bedding_types,
            self.meal_types,
            self.payment,
            new_page,
            self.price,
            self.reviews_rating,
            self.group,
            self.sort,
        )
        return self.get_hotel_data(url)

    def search_hotel_data(self) -> list[dict] | list:
        """Ищет каждый отель."""
        data = []
        try:
            html_class = '[class*="HotelListDatefull_card"]'
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, html_class))
                )
            except TimeoutException:
                pass
            html_hotel_data = self.driver.find_elements(By.CSS_SELECTOR, html_class)
            if not html_hotel_data:
                self.driver.quit()
                return data
            data.extend(self.forms_hotel_data(html_hotel_data))
            new_data_page = self._search_hotel_new_page_data()
            if (
                not len(new_data_page)
                or new_data_page[0]["Название"] == "Название отсутсвует"
            ):
                self.driver.quit()
                return data
            data.extend(new_data_page)
        except NoSuchElementException:
            self.driver.quit()
        return data

    def get_hotel_data(self, url: str) -> list[dict] | list:
        """Возвращает данные по отелям."""
        try:
            self.driver.get(url)
            return self.search_hotel_data()
        except (WebDriverException, NoSuchWindowException):
            return []

    def get_url(
        self,
        city="tula",
        date=_get_valid_dates(),
        guests="1",
        amenities="",
        bedding_types="",
        meal_types="",
        payment="",
        page=1,
        price="one",
        reviews_rating="",
        group="",
        sort="",
    ) -> str:
        """Формирует URL."""
        (
            self.city,
            self.date,
            self.guests,
            self.amenities,
            self.bedding_types,
            self.meal_types,
            self.payment,
            self.page,
            self.price,
            self.reviews_rating,
            self.group,
            self.sort,
        ) = (
            city,
            date,
            guests,
            amenities,
            bedding_types,
            meal_types,
            payment,
            page,
            price,
            reviews_rating,
            group,
            sort,
        )
        url = (
            f"{self.website}/{city}/?dates={date}&guests={guests}"
            f"&amenities={amenities}&bedding_types={bedding_types}"
            f"&meal_types={meal_types}&payment={payment}"
            f"&page={page}&price={price}&reviews_rating={reviews_rating}"
            f"&type_group={group}&sort={sort}"
        )
        return url


if "__main__" == __name__:
    parser = ParsingWebsiteOstrovok()
    url = parser.get_url()
    pprint(parser.get_hotel_data(url))
