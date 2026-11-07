import httpx
import re
import time
from aiogram import Router, F
import asyncio
import ssl
router = Router()

CBR_URL = "https://api.tinkoff.ru/v1/currency_rates?from=CNY&to=RUB"
DOLLAR_URL = "https://open.er-api.com/v6/latest/USD"
FALLBACK = "📈"
CUSTOM_RATE_ID = "5278751923338490157"
BAKSI_CASTOM_ID = "5409048419211682843"

RATE_CATEGORY = "Swft"  # поменяй под свой способ оплаты
CACHE_TTL = 600  # 10 минут
RATE = 1.00


_ssl_ctx = ssl.create_default_context(cafile="ca_bundle.pem")
_cache = {"value": None, "ts": 0.0}


async def cursik() -> float:
    now = time.time()
    if _cache["value"] is not None and now - _cache["ts"] < CACHE_TTL:
        return _cache["value"]

    try:
        async with httpx.AsyncClient(verify=_ssl_ctx, timeout=30) as client:
            response = await client.get(CBR_URL)
            response.raise_for_status()
            payload = response.json()["payload"]
            rates = payload["rates"]

        print(f"КУРС: lastUpdate={payload['lastUpdate']['milliseconds']}, now={int(now * 1000)}")

        for rate in rates:
            if rate["category"] == RATE_CATEGORY:
                value = rate["sell"] * RATE
                _cache["value"] = value
                _cache["ts"] = now
                return value
        raise ValueError(f"Категория {RATE_CATEGORY} не найдена")
    except Exception as e:
        print(f"ОШИБКА ОБНОВЛЕНИЯ КУРСА: {type(e).__name__}: {e}")
        if _cache["value"] is not None:
            return _cache["value"]
        raise


async def baksik() -> float:
    async with httpx.AsyncClient() as client:
        money = await client.get(DOLLAR_URL)
        data = money.json()
        return data["rates"]["CNY"]

customid = "5231449120635370684"

async def get_rates() -> tuple[float, float]:
    cny_rub, usd_cny = await asyncio.gather(cursik(), baksik())
    return cny_rub, usd_cny


@router.message(F.text)
async def vvod_yanei(message):
    text = message.text.replace(",", ".")
    spisok_cen = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]

    if not spisok_cen:
        await message.answer("Пожалуйста, введите числа. Например: 500 1200 300")
        return

    # курс нужно получить ДО цикла расчёта
    try:
        rate, usd_cny = await get_rates()
    except Exception as e:
        await message.answer("Обновление курса, попробуйте позже")
        print(f"ОШИБКА КУРСА: {type(e).__name__}: {e}")
        return


    results = []
    for cena in spisok_cen:
        price_rub = int(cena * rate)
        final = int(price_rub * (1.08 if price_rub >= 15000 else 1.10))
        results.append(final)

    total_yuan = sum(spisok_cen)
    total_rub = sum(results)


    await message.answer("Итоговая стоимость всех товаров:\n"
                         f"<tg-emoji emoji-id=\"{CUSTOM_RATE_ID}\">{FALLBACK}</tg-emoji> {total_yuan}\n"
                         f"<tg-emoji emoji-id=\"{customid}\">{FALLBACK}</tg-emoji> {total_rub}\n"
                         f"<tg-emoji emoji-id=\"{BAKSI_CASTOM_ID}\">{FALLBACK}</tg-emoji> {round(total_yuan / usd_cny, 0) }\n"
                         "Для оформления заказа обращайтесь к администратору: @dnlqa")
