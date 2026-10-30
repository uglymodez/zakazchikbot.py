from pathlib import Path
from aiogram import Router, F
from aiogram.filters import Command, callback_data
from handlers.orders import cursik
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import FSInputFile

router = Router()
FALLBACK = "📈"

BASE_DIR = Path(__file__).resolve().parent.parent  # папка bottgbaf
IMG_DIR = BASE_DIR / "images"

INFO_PHOTO = FSInputFile(IMG_DIR / "info1.jpeg")

MONEY = "5370852450414644361"
HELP = "5238025132177369293"
START = "5303479226882603449"
POZER = "5278751923338490157"
LOKL = "5402498632739996967"
BARBOS = "5251203410396458957"
NEKTO = "5208615751639903398"
FINAL = "5228991918305726190"

def reply_keyoard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Калькулятор цены")],
            [KeyboardButton(text= "Курс юаня"), KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Отзывы"), KeyboardButton(text="Контакты")],
            [KeyboardButton(text="О нас")]
        ],
        resize_keyboard=True,
    )
    return keyboard

def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "Для перехода в основное меню нажмите", callback_data = "info_more")],
        ]
    )
    return keyboard

@router.callback_query(F.data == "info_more")
async def proccess_more_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await start(callback.message)



@router.message(Command("start"))
@router.message(F.text.lower() == "о нас")
async def start(message):
    await message.answer(

        f"<tg-emoji emoji-id=\"{LOKL}\">{FALLBACK}</tg-emoji> \n"
        f"Здравствуйте, это бот для оформления заказа в сервисе PRO100\n"
        "\nМы занимаемся выкупом предметов с китайской площадки BUFF\n"
        "\nРаботаем с самой низкой комиссией на рынке\n"
        "\n"
        "\n\n /help - для помощи",
        reply_markup = reply_keyoard(),

    )
@router.message(Command("help"))
@router.message(F.text.lower() == "помощь")
async def help(message):
    await message.answer("Список доступных команд:\n"
                         f"\n<tg-emoji emoji-id=\"{START}\">{FALLBACK}</tg-emoji> /start - о нас\n"
                         f"\n<tg-emoji emoji-id=\"{BARBOS}\">{FALLBACK}</tg-emoji> /info - о нашей работе\n"
                         f"\n<tg-emoji emoji-id=\"{NEKTO}\">{FALLBACK}</tg-emoji> /contacts - наши контакты\n"
                         f"\n<tg-emoji emoji-id=\"{MONEY}\">{FALLBACK}</tg-emoji> /exchange - официальный курс юаня к рублю\n"
                         f"\n<tg-emoji emoji-id=\"{HELP}\">{FALLBACK}</tg-emoji> /help - открыть меню доступных комманд")

@router.message(Command("exchange"))
@router.message(F.text.lower() == "курс юаня")
async def curs(message):
    rate = await cursik()
    await message.answer(f"<tg-emoji emoji-id=\"{POZER}\">{FALLBACK}</tg-emoji> Курс: {rate:.2f} ₽ за 1 CNY\n")

@router.message(Command("info"))
@router.message(F.text.lower() == "отзывы")
async def otzivi(message):
    await message.answer_photo(
        photo = INFO_PHOTO,
        caption = f"<tg-emoji emoji-id=\"{FINAL}\">{FALLBACK}</tg-emoji>"
            "Можете узнать о нашей работе, прочитав отзывы клиентов по ссылке:\n\n https://t.me/+ZAZWpemKLIY0YzAy"
    )



@router.message(Command("contacts"))
@router.message(F.text.lower() == "контакты")
async def contacts(message):
    await message.answer("Если у вас остались вопросы:\n" 
                         "1)По работе ТГ бота:\n"
                          "@etiimena\n" 
                          "2)По оформлению заказа:\n"
                          "@dnlqa")

@router.message(Command("calculate"))
@router.message(F.text.lower() == "калькулятор цены")
async def calculate(message):
    await message.answer("Можете вводить цену предмета или предметов в юанях:",
                         reply_markup = get_main_inline_keyboard()
                         )
