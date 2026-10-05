import httpx
from aiogram import Router
router = Router()

CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
DOLLAR_URL = "https://open.er-api.com/v6/latest/USD"
FALLBACK = "📈"
CUSTOM_RATE_ID = "5278751923338490157"
BAKSI_CASTOM_ID = "5409048419211682843"

async def cursik() -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(CBR_URL)
        data = response.json()
        return data["Valute"]["CNY"]["Value"]


async def baksik() -> float:
    async with httpx.AsyncClient() as client:
        money = await client.get(DOLLAR_URL)
        data = money.json()
        return data["rates"]["CNY"]

customid = "5231449120635370684"


@router.message()
async def vvod_yanei(message):
    text = message.text.strip().replace(",", ".")
    spisok_cen = []
    try:
        for i in text.split():
            spisok_cen.append(int(i))
    except ValueError:
        await message.answer("Пожалуйста, введите числа. Например: 500 1200 300")
        return

    if not spisok_cen:
        await message.answer("Не нашёл ни одной цены.")
        return

    try:
        rate = await cursik()
    except Exception as e:
        await message.answer("Обновление курса, попробуйте позже")
        print(f"ОШИБКА КУРСА: {type(e).__name__}: {e}")
        return

    results = []
    for cena in spisok_cen:
        price_rub = int(cena * rate)
        final = int(price_rub * (1.05 if price_rub >= 15000 else 1.07))
        results.append(final)

    total_yuan = sum(spisok_cen)
    total_rub = sum(results)


    await message.answer("Итоговая стоимость всех товаров:\n"
                         f"<tg-emoji emoji-id=\"{CUSTOM_RATE_ID}\">{FALLBACK}</tg-emoji> {total_yuan}\n"
                         f"<tg-emoji emoji-id=\"{customid}\">{FALLBACK}</tg-emoji> {total_rub}\n"
                         f"<tg-emoji emoji-id=\"{BAKSI_CASTOM_ID}\">{FALLBACK}</tg-emoji> {round(total_yuan / await baksik(), 0) }\n"
                         "Для оформления заказа проследуйте далее")
