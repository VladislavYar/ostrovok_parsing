import os
import json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application, CommandHandler, ConversationHandler,
    MessageHandler, ContextTypes, filters
    )


from dotenv import load_dotenv


load_dotenv()


TOKEN_BOT = os.getenv('TOKEN')
INSLAND = '🏝️'
kEYBOARD = [
        ['Дата', 'Цена за ночь RUB'],
        ['Количество гостей', 'Сортировка'],
        ['Город', 'Тип размещения'],
        ['В отеле', 'В номере'],
        ['Особенности размещения', 'Питание'],
        ['Оценка по отзывам', 'Оплата и бронирование'],
        ['Тип кроватей'],
        ['Поиск', 'Выход'],
    ]

async def filter_select_output(update: Update,
                               context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выводит выбор фильтра для пользователя."""
    return ConversationHandler.END


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Поиск отелей."""
    return ConversationHandler.END


async def insland(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начало выбора фильтров для парсинга."""
    text = 'Какие фильтры ты хочешь задать?'
    markup = ReplyKeyboardMarkup(kEYBOARD, one_time_keyboard=True)
    await update.effective_message.reply_text(text, reply_markup=markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """При старте приветсвует и выводит кнопку."""

    button = ReplyKeyboardMarkup(
        [[INSLAND, ]], resize_keyboard=True)
    name = update.message.chat.first_name
    text = (
            f'Приветствую тебя, {name}! Я ботограмм v1.0\n'
            'Занимаюсь парсингом сайта ostrovok.ru\n'
            'Умею фильровать данные по твоим запросам'
            'и выводить данные в файл.\n'
            'Ткни в островок, не бойся;)'
            )

    await update.effective_message.reply_text(text, reply_markup=button)


def main() -> None:
    """Старт бота."""

    application = Application.builder().token(TOKEN_BOT).build()

    start_filter = filters.Regex(INSLAND)
    search_filter = (
        filters.Regex('Дата') |
        filters.Regex('Цена за ночь RUB') |
        filters.Regex('Количество гостей') |
        filters.Regex('Сортировка') |
        filters.Regex('Город') |
        filters.Regex('В отеле') |
        filters.Regex('В номере') |
        filters.Regex('Особенности размещения') |
        filters.Regex('Питание') |
        filters.Regex('Оценка по отзывам') |
        filters.Regex('Оплата и бронирование') |
        filters.Regex('Тип кроватей')
        )

    handler = ConversationHandler(
        entry_points=[CommandHandler("start", start),
                      MessageHandler(start_filter, start)],
        states={
            0: [
                MessageHandler(
                    search_filter, filter_select_output
                ),
            ],
            1: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
                )
            ],
            2: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex('Поиск'), search)],
    )

    application.add_handlers(handler)

    application.run_polling()


if __name__ == "__main__":
    main()
