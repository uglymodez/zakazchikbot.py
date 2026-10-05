
from aiogram import Router, F
from aiogram.filters import Command
from handlers.orders import cursik
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()
FALLBACK = "📈"
MONEY = "5370852450414644361"
HELP = "5238025132177369293"
START = "5303479226882603449"
POZER = "5278751923338490157"
LOKL = "5402498632739996967"
BARBOS = "5251203410396458957"
NEKTO = "5447410659077661506"
FINAL = "5443127283898405358"

def reply_keyoard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="О нас")],
            [KeyboardButton(text= "Курс юаня"), KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Перезапуск бота"), KeyboardButton(text="Контакты")]
        ],
        resize_keyboard=True,
    )
    return keyboard


@router.message(Command("start"))
@router.message(F.text.lower() == "перезапуск бота")
async def start(message):
    await message.answer(
        f"<tg-emoji emoji-id=\"{LOKL}\">{FALLBACK}</tg-emoji> \n"
        f"Здравствуйте, это бот для оформления заказа в сервисе PRO100\n"
        "\nМы занимаемся выкупом предметов с китайской площадки BUFF\n"
        "\nРаботаем с самой низкой комиссией на рынке\n"
        "\nДля начала работы можете вводить цены интересующих вас предметов с BUFF\n"
        "\n\n /help - для помощи",
        reply_markup = reply_keyoard()
    )
@router.message(Command("help"))
@router.message(F.text.lower() == "помощь")
async def help(message):
    await message.answer("Список доступных команд:\n"
                         f"<tg-emoji emoji-id=\"{START}\">{FALLBACK}</tg-emoji> /start - перезапуск бота\n"
                         f"<tg-emoji emoji-id=\"{BARBOS}\">{FALLBACK}</tg-emoji> /info - о нашей работе\n"
                         f"<tg-emoji emoji-id=\"{NEKTO}\">{FALLBACK}</tg-emoji> /contacts - наши контакты\n"
                         f"<tg-emoji emoji-id=\"{MONEY}\">{FALLBACK}</tg-emoji> /exchange - узнать курс юаня к рублю от банка ЦБ на сегоднящний день\n"
                         f"<tg-emoji emoji-id=\"{HELP}\">{FALLBACK}</tg-emoji> /help - открыть меню доступных комманд")

@router.message(Command("exchange"))
@router.message(F.text.lower() == "курс юаня")
async def curs(message):
    rate = await cursik()
    await message.answer(f"<tg-emoji emoji-id=\"{POZER}\">{FALLBACK}</tg-emoji> Курс: {rate:.2f} ₽ за 1 CNY\n")

@router.message(Command("info"))
@router.message(F.text.lower() == "о нас")
async def otzivi(message):
    await message.answer(f"<tg-emoji emoji-id=\"{FINAL}\">{FALLBACK}</tg-emoji> \n"
                         "Можете узнать о нашей работе, прочитав отзывы наших клиентов по ссылке: https://t.me/+ZAZWpemKLIY0YzAy")


@router.message(Command("contacts"))
@router.message(F.text.lower() == "контакты")
async def contacts(message):
    await message.answer("Если у вас остались вопросы:\n" 
                         "1)По работе ТГ бота:\n"
                          "@etiimena\n" 

                          "2)По оформлению заказа:\n"
                          "@dnlqa")