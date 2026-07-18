import asyncio
import logging
import sys
import datetime as dt

from curl_cffi import requests as cc_requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

import pytesseract
from PIL import Image

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder


API_TOKEN = "8312694091:AAGFdN1OVQU0aTqlUjOxUnSrFVsUj8midN0"

EMAIL = '---'
PASSWORD = '---'

MARTIN = 'https://fortuneadvert.com/martin/?_preview=show&pkey=f73346043c'
Martin_Prices = []
Martin_Checked = dt.datetime.now().strftime("%H:%M")
Martin_Text = ''

DRAGON = 'https://fortuneadvert.com/dragon3/?_preview=show&pkey=f73349023d'
Dragon_Prices = []
Dragon_Checked = dt.datetime.now().strftime("%H:%M")
Dragon_Text = ''

PINCO = 'https://fortuneadvert.com/pinco/?_preview=show&pkey=f73347083a'
Pinco_Prices = []
Pinco_Checked = dt.datetime.now().strftime("%H:%M")
Pinco_Text = ''


class HybridScraper:
    def init(self):
        self.cc_session = cc_requests.Session()
        self.driver = None

    def setup_selenium(self):
        """Настраиваем undetected-chromedriver"""
        options = uc.ChromeOptions()

        # Настройки для обхода детекции
        options.add_argument('--disable-blink-features=AutomationControlled')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        self.driver = uc.Chrome(options=options, browser_executable_path='C:\Program Files\Google\Chrome Beta\Application\chrome.exe')

        # Скрываем WebDriver
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_with_curl_cffi(self, url, impersonate="chrome110"):
        """Получаем данные через curl_cffi"""
        try:
            response = self.cc_session.get(
                url,
                impersonate=impersonate,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                },
                timeout=30
            )
            return response
        except Exception as e:
            print(f"curl_cffi error: {e}")
            return None

    async def scrape_dragon(self, url, message):
        # Пытаемся получить через curl_cffi
        response = self.get_with_curl_cffi(url)

        if response and response.status_code == 200:
            # Если получили через curl_cffi, используем его данные
            print("Success with curl_cffi")
            return response.text
        else:
            # Если не получилось, используем Selenium
            print("Falling back to Selenium")
            if not self.driver:
                self.setup_selenium()

            self.driver.set_window_size(800, 800)
            self.driver.get(url)
            await asyncio.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="main-header"]/div/div/div[2]/div/button[1]').click()
            await message.answer('Dragon: Загрузка')
            await asyncio.sleep(7)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div[2]/span').click()
            await asyncio.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys("dilraider.pek307@gmail.com")
            await asyncio.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
            await asyncio.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys("Sk23Ghf52_0ds")
            await asyncio.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
            await message.answer('Dragon: Вход на сайт')
            await asyncio.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="main-header"]/div/div/div[2]/div/a').click()
            await asyncio.sleep(2)
            self.driver.save_screenshot("dragon.png")
            html1 = self.driver.page_source.split('font-medium leading-[16px] text-gray transition-[color]">')
            html2 = self.driver.page_source.split('px-3 py transition-colors md:bg-bg-container')
            await message.answer('Dragon: Данные сохранены')
            Dragon_Prices = []
            for i in range(1, len(html1)):
                price = html1[i].split('</div>')[0]
                service = html2[i].split('alt="')[1].split('"')[0]
                if '&' in price:
                    price = price.split('&nbsp;')
                    Dragon_Prices.append(f'{service}: {price[0] + price[1]}')
                else:
                    Dragon_Prices.append(f'{service}: {price}')
            print(Dragon_Prices)
            return Dragon_Prices

    async def scrape_martin(self, url, message):
        # Пытаемся получить через curl_cffi
        response = self.get_with_curl_cffi(url)

        if response and response.status_code == 200:
            # Если получили через curl_cffi, используем его данные
            print("Success with curl_cffi")
            return response.text
        else:
            # Если не получилось, используем Selenium
            print("Falling back to Selenium")
            if not self.driver:
                self.setup_selenium()

            self.driver.set_window_size(800, 800)
            self.driver.get(url)
            await asyncio.sleep(3)
            self.driver.find_element(By.CLASS_NAME, 'registration-form__login-link').click()
            await message.answer('Martin: Загрузка')
            print('Martin: logging')
            await asyncio.sleep(3)

            input_email = self.driver.find_element(By.ID, "email")
            input_email.send_keys(EMAIL)
            print('Martin: pasted email')
            await asyncio.sleep(1)

            input_password = self.driver.find_element(By.ID, "password")
            input_password.send_keys(PASSWORD)
            print('Martin: pasted password')
            await asyncio.sleep(3)

            self.driver.find_element(By.CLASS_NAME, 'registration-form__btn').click()
            await message.answer('Martin: Вход на сайт')
            print('Martin: entering')
            await asyncio.sleep(10)

            self.driver.save_screenshot("martin.png")
            html1 = self.driver.page_source.split('_paymentCardText_1xqa6_1')
            html2 = self.driver.page_source.split('_paymentCard_1xqa6_1')
            await message.answer('Martin: Данные сохранены')
            print('Martin: html and screenshot saved. quiting')

            Martin_Prices = []
            for i in range(1, len(html1)):
                price = html1[i][2:15].split('–')[0]
                service = html2[i].split('data-test="')[1].split('"><div class="_paymentCardImage')[0].split()[-1]
                if '&' in price:
                    price = price.split('&nbsp;')
                    Martin_Prices.append(f'{service}: {price[0] + price[1]}Р')
                else:
                    Martin_Prices.append(f'{service}: {price}Р')
            print(Martin_Prices)
            return Martin_Prices

    async def scrape_pinco(self, url, message):
        # Пытаемся получить через curl_cffi
        response = self.get_with_curl_cffi(url)

        if response and response.status_code == 200:
            # Если получили через curl_cffi, используем его данные
            print("Success with curl_cffi")
            return response.text
        else:
            # Если не получилось, используем Selenium
            print("Falling back to Selenium")
            if not self.driver:
                self.setup_selenium()

            self.driver.set_window_size(800, 800)
            self.driver.get(url)
            await asyncio.sleep(15)
            self.driver.find_element(By.XPATH, '/html/body/pu-root/ng-component/div/div/button/span').click()
            await message.answer('Pinco: Загрузка')
            await asyncio.sleep(15)
            self.driver.find_element(By.XPATH, '//*[@id="login"]').send_keys("dilraider.pek307@gmail.com")
            await asyncio.sleep(4)
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("Sk23Ghf52_0ds")
            await asyncio.sleep(1)
            self.driver.find_element(By.CLASS_NAME, 'ui-button_primary').click()
            await message.answer('Pinco: Вход на сайт')
            await asyncio.sleep(30)
            self.driver.find_element(By.CLASS_NAME, 'pu-header__wallet').click()
            await asyncio.sleep(5)
            self.driver.find_element(By.CLASS_NAME, 'ui-payments-view-switcher__tab_row-view').click()
            await asyncio.sleep(5)
            self.driver.save_screenshot("pinco.png")
            await message.answer('Pinco: Данные сохранены')
            await asyncio.sleep(5)
            image = Image.open('pinco.png')
            a = pytesseract.image_to_string(image, lang='rus')
            a = a.split('Мин. ')
            Pinco_Prices = []
            for i in range(len(a)):
                if ' Р - Макс.' in a[i]:
                    Pinco_Prices.append(a[i].split(' Р - Макс.')[0]+"P")
            return Pinco_Prices

    def close(self):
        if self.driver:
            self.driver.quit()


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global Martin_Checked, Martin_Prices, Martin_Text, Dragon_Checked, Dragon_Prices, Dragon_Text, Pinco_Checked, Pinco_Prices, Pinco_Text
    while True:
        await message.answer('Начинаем собирать данные...')


        # First site - Martin
        driver = HybridScraper()
        driver.setup_selenium()
        try:
            Martin_Prices = await driver.scrape_martin(MARTIN, message)
        except:
            await message.answer('Martin: Ошибка сбора данных. Введите /start, чтобы собрать данные ещё раз')
        driver.close()
        Martin_Checked = dt.datetime.now().strftime("%H:%M")
        Martin_Text = f'Martin:\nПоследнее обновление: {Martin_Checked}\n{"\n".join(Martin_Prices)}'

        # End of the first site. Dragon
        driver = HybridScraper()
        driver.setup_selenium()
        try:
            Dragon_Prices = await driver.scrape_dragon(DRAGON, message)
        except:
            await message.answer('Dragon: Ошибка сбора данных. Введите /start, чтобы собрать данные ещё раз')
        driver.close()
        Dragon_Checked = dt.datetime.now().strftime("%H:%M")
        Dragon_Text = f'Dragon Money:\nПоследнее обновление: {Dragon_Checked}\n{"\n".join(Dragon_Prices)}'

        # End of the second site.
        driver = HybridScraper()
        driver.setup_selenium()
        try:
            Pinco_Prices = await driver.scrape_pinco(PINCO, message)
        except:
            await message.answer('Pinco: Ошибка сбора данных. Введите /start, чтобы собрать данные ещё раз')
        driver.close()
        Pinco_Checked = dt.datetime.now().strftime("%H:%M")
        Pinco_Text = f'Pinco:\nПоследнее обновление: {Pinco_Checked}\n{"\n".join(Pinco_Prices)}'

        # End of the third site.

        await message.answer('Данные готовы. Введите /show, чтобы просмотреть')

        await asyncio.sleep(3600)


@dp.message(Command("show"))
async def show(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Показать скриншот", callback_data="show_screenshot_martin"))
    await message.answer(Martin_Text, reply_markup=builder.as_markup())

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Показать скриншот", callback_data="show_screenshot_dragon"))
    await message.answer(Dragon_Text, reply_markup=builder.as_markup())

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Показать скриншот", callback_data="show_screenshot_pinco"))
    await message.answer(Pinco_Text, reply_markup=builder.as_markup())


@dp.message(Command('martin'))
async def martin(message: types.Message):
    global Martin_Checked, Martin_Prices, Martin_Text
    driver = HybridScraper()
    driver.setup_selenium()
    try:
        Martin_Prices = await driver.scrape_martin(MARTIN, message)
    except:
        await message.answer('Martin: Ошибка сбора данных. Введите /martin, чтобы собрать данные ещё раз')
    driver.close()
    Martin_Checked = dt.datetime.now().strftime("%H:%M")
    Martin_Text = f'Martin:\nПоследнее обновление: {Martin_Checked}\n{"\n".join(Martin_Prices)}'


@dp.message(Command('dragon'))
async def dragon(message: types.Message):
    global Dragon_Checked, Dragon_Prices, Dragon_Text
    driver = HybridScraper()
    driver.setup_selenium()
    try:
        Dragon_Prices = await driver.scrape_dragon(DRAGON, message)
    except:
        await message.answer('Dragon: Ошибка сбора данных. Введите /dragon, чтобы собрать данные ещё раз')
    driver.close()
    Dragon_Checked = dt.datetime.now().strftime("%H:%M")
    Dragon_Text = f'Dragon Money:\nПоследнее обновление: {Dragon_Checked}\n{"\n".join(Dragon_Prices)}'


@dp.message(Command('pinco'))
async def pinco(message: types.Message):
    global Pinco_Checked, Pinco_Prices, Pinco_Text
    driver = HybridScraper()
    driver.setup_selenium()
    try:
        Pinco_Prices = await driver.scrape_pinco(PINCO, message)
    except:
        await message.answer('Pinco: Ошибка сбора данных. Введите /pinco, чтобы собрать данные ещё раз')
    driver.close()
    Pinco_Checked = dt.datetime.now().strftime("%H:%M")
    Pinco_Text = f'Pinco:\nПоследнее обновление: {Pinco_Checked}\n{"\n".join(Pinco_Prices)}'


@dp.message(Command('martin'))
async def martin(message: types.Message):
    global Martin_Checked, Martin_Prices, Martin_Text
    driver = HybridScraper()
    driver.setup_selenium()
    try:
        Martin_Prices = await driver.scrape_martin(MARTIN, message)
    except:
        await message.answer('Martin: Ошибка сбора данных. Введите /start, чтобы собрать данные ещё раз')
    driver.close()
    Martin_Checked = dt.datetime.now().strftime("%H:%M")
    Martin_Text = f'Martin:\nПоследнее обновление: {Martin_Checked}\n{"\n".join(Martin_Prices)}'


@dp.callback_query(F.data == "show_screenshot_martin")
async def show_screenshot_martin(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data="hide_screenshot_martin"))
    await Bot(token=API_TOKEN).send_photo(chat_id=callback.message.chat.id,
                                          photo=FSInputFile('martin.png'),
                                          reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data == "hide_screenshot_martin")
async def hide_screenshot_martin(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Показать скриншот", callback_data="show_screenshot_martin"))
    await Bot(token=API_TOKEN).send_message(chat_id=callback.message.chat.id,
                                            text=Martin_Text,
                                            reply_markup=builder.as_markup())


@dp.callback_query(F.data == "show_screenshot_dragon")
async def show_screenshot_dragon(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data="hide_screenshot_dragon"))
    await Bot(token=API_TOKEN).send_photo(chat_id=callback.message.chat.id,
                                          photo=FSInputFile('dragon.png'),
                                          reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data == "hide_screenshot_dragon")
async def hide_screenshot_dragon(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Показать скриншот", callback_data="show_screenshot_dragon"))
    await Bot(token=API_TOKEN).send_message(chat_id=callback.message.chat.id,
                                            text=Dragon_Text,
                                            reply_markup=builder.as_markup())

@dp.callback_query(F.data == "show_screenshot_pinco")
async def show_screenshot_pinco(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data="hide_screenshot_pinco"))
    await Bot(token=API_TOKEN).send_photo(chat_id=callback.message.chat.id,
                                          photo=FSInputFile('pinco.png'),
                                          reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data == "hide_screenshot_pinco")
async def hide_screenshot_pinco(callback: types.CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Показать скриншот", callback_data="show_screenshot_pinco"))
    await Bot(token=API_TOKEN).send_message(chat_id=callback.message.chat.id,
                                            text=Pinco_Text,
                                            reply_markup=builder.as_markup())


async def main() -> None:
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
