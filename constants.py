HOTELS_ON_PAGE = 20
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
