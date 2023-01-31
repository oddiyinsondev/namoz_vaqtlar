import logging
from aiogram import Dispatcher, types, Bot, executor
from tokken import TOKEN
from buttons import Buttons
from states import Register
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import requests


logging.basicConfig(level=logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def strat_up(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Assalomu alaykum rahmatullohi barakatuh {name}\nYordam uchun /help",reply_markup=Buttons)


@dp.message_handler(commands=['help'])
async def help_my(message: types.Message):
    await message.answer(f"Admin Shohruhbek\nNikename: @ollohga_oshiqmann\nPhone number: +998883601656\nBo'lanishingiz mumkin📲📲📲")


@dp.message_handler(text='QURON')
async def boshladim(message: types.Message):
    await message.answer_photo(photo=open("rasm_video/kuron.jpg", "rb"), caption="Oyat yoki Sura tarjimasini topishingiz mumkin buning uchun izlayotgan sura oyatiz nomini")
    await Register.sura.set()


@dp.message_handler(state=Register.sura)
async def kiriting(message: types.Message, state: FSMContext):
    nummber = message.text
    await state.update_data(
        {'nummber':nummber}
    )
    try:
        await message.answer(f"oyatni kiring")
    except:
        await message.answer("Qidiryotgan surangizning raqamini yuboring")
    await Register.oyat.set()

@dp.message_handler(state=Register.oyat)
async def kiriting_oyat(message: types.Message, state: FSMContext):
    nummber2 = message.text
    await state.update_data(
        {'nummber2':nummber2}
    )
    try:
        data = await state.get_data()
        nomr = data.get('nummber')
        nomr2 = data.get('nummber2')
        url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{nomr}/{nomr2}.json"
        yubor = requests.get(url)
        data = yubor.json()
        xabar = data["text"]
        await message.answer(xabar)
    except:
        await message.answer(f"oyatning nechinchi raqamdaligini yuboring nomi bilan ishlay olmaymiz")
    await state.finish()

@dp.message_handler(text="TAQVIM")
async def taqvim(message: types.Message):
    await message.answer_photo(photo=open("rasm_video/kaba_rasm.jpg", "rb"), caption=f"Mintaqangizni kiriting:")



@dp.message_handler()
async def boshladim(message: types.Message):
    viloyat = message.text
    url = f"https://islomapi.uz/api/present/day?region={viloyat}"
    xabar = requests.get(url)
    text = xabar.json()
    region = text["region"]
    date = text["date"]
    weekday = text["weekday"]
    tong_saharlik = text["times"]["tong_saharlik"]
    quyosh = text["times"]["quyosh"]
    peshin = text["times"]["peshin"]
    asr = text["times"]["asr"]
    shom_iftor = text["times"]["shom_iftor"]
    hufton = text["times"]["hufton"]
    await message.answer_photo(photo=open("rasm_video/taqvim.png", "rb"), caption=f"Bugungi namoz vaqtlari:\nShahar {region}\nSana vaqt: {date}\nKun {weekday}\nNamoz vaqtlari:\nTong_saharlik: {tong_saharlik}\nQuyosh {quyosh}\nPeshin {peshin}\nAsr {asr}\nShom_iftor {shom_iftor}\nHufton {hufton}")    







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
