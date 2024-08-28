from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import CHANE_keyboard as ck
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import SQLite as sq
import datetime
import random

proxy_url = 'http://proxy.server:3128'
storage = MemoryStorage()
bot = Bot('6015314056:AAFtEgUyx897yl9QWnc2dlJyT06KMD83iZ8')
dp = Dispatcher(bot=bot, storage=storage)
a = False
sum = 0
sum_vivod = 0
num_cart = 0
ID = ''


class ProfileState(StatesGroup):
    number = State()
    sogl_1 = State()
    sogl_2 = State()
    get_id = State()
    admin = State()
    admin_get = State()
    pay = State()
    vivod = State()
    vivod_cart = State()
    admin_vivod = State()


def check_sub(chat_member):
    if chat_member['status'] == 'member' or chat_member['status'] == 'administrator':
        return True
    else:
        return False


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    if sq.check(message.from_user.id):
        await message.answer(text='Выберите меню для перехода⬇️',
                             reply_markup=ck.get_kb_join())
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=ck.hello_message,
                               parse_mode='HTML',
                               reply_markup=ck.get_ikb_sogl())
        await ProfileState.number.set()


@dp.message_handler(commands=['admin'], state='*') # режим админа
async def admin(message: types.Message):
    if message.from_user.id == 6171444954 or message.from_user.id == 1006103801:
        await message.answer(text='Ты в режиме админа\n\nВыбери действие⬇️',
                             reply_markup=ck.get_kb_menu_admin())
    await ProfileState.admin.set()


@dp.message_handler(Text(equals='Подтвердить ПЛАТЕЖ пользователя'), state=ProfileState.admin)
async def join_user(message: types.Message):
    if message.from_user.id == 6171444954 or message.from_user.id == 1006103801:
        await message.answer('Введи ID чела которого хочешь добавить')
    await ProfileState.admin_get.set()


@dp.message_handler(state=ProfileState.admin_get)
async def get_user(message: types.Message, state: FSMContext):
    await message.answer('Пользователь добавлен!')
    global sum
    a = sq.user_ref(int(message.text))
    profit = sq.user_money_profit(a)
    profit = int(profit) + 180
    sq.set_profit(int(a), profit)
    sq.set_balance(int(message.text), 300)
    b = int(sq.user_money_unlock(message.text))
    c = int(sq.user_money_unlock(int(a)))
    b += 90
    c += 180
    sq.set_unlock(int(message.text), b)
    sq.set_unlock(int(a), c)
    sq.set_chane_money(int(message.text), 30 + (float(sum) - 300))
    await bot.send_message(chat_id=int(message.text),
                           text=f'<b>Успешное пополнение☑️</b>\n'
                                f'Cумма: 300₽',
                           parse_mode='HTML')
    await bot.send_message(chat_id=int(a),
                           text=f'Ваш реферал: <code>{message.text}</code> пополнил счет!💸',
                           parse_mode='HTML')
    await state.finish()


@dp.message_handler(Text(equals='Подтвердить ВЫВОД пользователя'), state=ProfileState.admin)
async def vivod_user(message: types.Message):
    if message.from_user.id == 6171444954 or message.from_user.id == 1006103801:
        await message.answer('Введи ID чела')
    await ProfileState.admin_vivod.set()


@dp.message_handler(state=ProfileState.admin_vivod)
async def get_user(message: types.Message, state: FSMContext):
    await message.answer('Вывод подтвержден!')
    global sum_vivod
    balance = sq.user_money_balance(int(message.text))
    unlock = sq.user_money_unlock(int(message.text))
    unlock -= int(sum_vivod)
    sq.set_unlock(int(message.text), unlock)
    await bot.send_message(chat_id=int(message.text),
                           text=f'<b>Успешный вывод☑️</b>\n'
                                f'Cумма: {sum_vivod}₽',
                           parse_mode='HTML')

    await state.finish()


@dp.callback_query_handler(state=ProfileState.number) # номер телефона
async def give_phone_number(callback: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
    await callback.message.answer("Для продолжения работы, отправь свой контакт:", reply_markup=keyboard)
    await ProfileState.sogl_1.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=ProfileState.sogl_1)
async def contacts(msg: types.Message):
    await msg.answer(f"Твой номер успешно получен: {msg.contact.phone_number}", reply_markup=types.ReplyKeyboardRemove())
    await sq.add(msg.from_user.id, msg.from_user.username, msg.contact.phone_number)
    if check_sub(await bot.get_chat_member(chat_id='@chane_enter', user_id=msg.from_user.id)):
        await msg.answer('Введите ID пользователя, который пригласил вас в систему!\n'
                         'Если у вас его нет, отправьте сообщение "нет"')
        await ProfileState.get_id.set()
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text='Для доступа к боту, нужно подписать на наш основной канал!',
                               reply_markup=ck.get_ikb_sub())


@dp.callback_query_handler(state=ProfileState.sogl_1)
async def give_phone_number(callback: types.CallbackQuery):
    if callback.data == 'sub' and check_sub(await callback.bot.get_chat_member(chat_id='@chane_enter', user_id=callback.from_user.id)):
        await callback.message.answer('Введите ID пользователя, который пригласил вас в систему!\n'
                                      'Если у вас его нет, отправьте сообщение "нет"')
        await ProfileState.get_id.set()
    else:
        await callback.message.answer(text='Для доступа к боту, нужно подписать на наш основной канал!',
                                      reply_markup=ck.get_ikb_sub())


@dp.message_handler(state=ProfileState.get_id)
async def get_id(message: types.Message, state: FSMContext):
    if message.text != 'нет':
        a = message.text
        if sq.check(a) and int(message.from_user.id) != int(a):
            sq.add_ref(int(message.from_user.id), int(a))
            await message.answer('Успешно!', reply_markup=ck.get_kb_join())
            await bot.send_message(chat_id=int(message.text),
                                   text=f'По вашему реферальному коду зарегистрировался пользователь с ID: <code>{message.from_user.id}</code>',
                                   parse_mode='HTML')
            await state.finish()
        else:
            await message.answer('Некорректный ID')
            await ProfileState.get_id.set()
    else:
        sq.add_ref(int(message.from_user.id), 1891715370)
        await message.answer(text='Выберите меню для перехода⬇️',
                             reply_markup=ck.get_kb_join())
        await state.finish()


@dp.callback_query_handler(lambda callback: callback.data == 'up')
async def top_up(callback: types.CallbackQuery):
    global sum
    await callback.message.delete()
    a = random.random()
    a = str("%.1f" % a)
    b = random.randint(305, 315)
    sum = str(b) + a[1:]
    await callback.message.answer(text=f'Для успешного пополнения средств используйте инструкцию:\n\n'
                                       f'💳Счет для оплаты:\nhttps://yoomoney.ru/to/4100117042524058\n(Тинькофф/Сбербанк/Qiwi)\n\n💵Сумма платежа: {sum}₽\n\n'
                                       f'<b>После успешного платежа:</b>\n1) Предоставьте квитанцию об успешной оплате на аккаунт поддержки. (По кнопке ниже)\n'
                                       f'2) Нажмите кнопку\n"Проверить платеж✅".',
                                  reply_markup=ck.get_ikb_check(),
                                  parse_mode='HTML')


@dp.callback_query_handler(lambda callback: callback.data == 'check')
async def pay(callback: types.CallbackQuery):
    global sum
    global ID
    ID = str(callback.from_user.id)
    await callback.message.answer(text='<b>Ваша заявка в обработке!</b>\n<em>Время проверки платежа занимает до 12 часов</em>',
                                  parse_mode='HTML')
    await bot.send_message(chat_id=1006103801,
                           text=f'<b>ПОПОЛНЕНИЕ</b>\n'
                                f'Пользователь: @{callback.from_user.username}\n'
                                f'ID: <code>{callback.from_user.id}</code>\n'
                                f'Сумма: {sum}₽',
                           parse_mode='HTML')
    await bot.send_message(chat_id=6171444954,
                           text=f'<b>ПОПОЛНЕНИЕ</b>\n'
                                f'Пользователь: @{callback.from_user.username}\n'
                                f'ID: <code>{callback.from_user.id}</code>\n'
                                f'Сумма: {sum}₽',
                           parse_mode='HTML')


@dp.callback_query_handler(lambda callback: callback.data == 'down')
async def vivod(callback: types.CallbackQuery):
    a = sq.user_money_unlock(callback.from_user.id)
    await callback.message.answer(text=f'Вывод средств🏛️\n\n'
                                  f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                  f'♻️Доступно для вывода: {a}₽\n\n'
                                  f'<em>Важно!</em>\n'
                                  f'•Минимальная сумма вывода - 10₽.\n'
                                  f'•Комиссия 5%\n'
                                  f'•Выводы осуществляются на карты VISA\Mastercard\МИР\n'
                                  f'➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                  f'<b>Введите сумму вывода:</b>',
                                  parse_mode='HTML')
    await ProfileState.vivod.set()


@dp.message_handler(state=ProfileState.vivod)
async def sum_vivod(message: types.Message, state: FSMContext):
    a = int(sq.user_money_unlock(message.from_user.id))
    b = int(sq.user_money_balance(message.from_user.id))
    global sum_vivod
    try:
        if int(message.text) < 10:
            await message.answer(text='Сумма для вывода должна быть больше 10 рублей.')
        elif b != 300:
            await message.answer(text=f'Для вывода необходимо быть участником системы❗️\n\n'
                                      f'<em>*участником является пользователь, совершивший пополнение на фиксированную сумму (300₽).\n'
                                      f'Рекомендуем совершить депозит и попробовать еще раз!</em>\n'
                                      f'(для перехода в главное меню введите /start)',
                                 parse_mode='HTML')
        elif int(message.text) > a:
            await message.answer(text='Сумма для вывода не должна превышать доступные для вывода средства.')
        else:
            sum_vivod = message.text
            await message.answer(text=f'<b>Введите номер карты:</b>',
                                 parse_mode='HTML')
            await ProfileState.vivod_cart.set()
    except:
        await message.answer('Некорректный ввод')
        await state.finish()


@dp.message_handler(state=ProfileState.vivod_cart)
async def vivod_cart(message: types.Message, state: FSMContext):
    global sum_vivod
    id = message.from_user.id
    a = int(sum_vivod) - (float(sum_vivod) * 0.05)
    global num_cart
    num_cart = message.text
    await message.answer(text=f'Вывод успешно заказан!✅\n\n'
                              f'<em>Будет зачислено:</em> {a}\n'
                              f'<em>Максимальное время выплаты 12 часов</em>',
                         parse_mode='HTML')
    await bot.send_message(chat_id=1006103801,
                           text=f'<b>ВЫВОД</b>\n'
                                f'ID: <code>{id}</code>\n'
                                f'Карта: <code>{num_cart}</code>\n'
                                f'Сумма: {sum_vivod}₽',
                           parse_mode='HTML')
    await bot.send_message(chat_id=6171444954,
                           text=f'<b>ВЫВОД</b>\n'
                                f'ID: <code>{id}</code>\n'
                                f'Карта: <code>{num_cart}</code>\n'
                                f'Сумма: {sum_vivod}₽',
                           parse_mode='HTML')
    await state.finish()


@dp.message_handler(Text(equals='💼Личный кабинет'), state='*')
async def profile(message: types.Message):
    date_start = sq.time(message.from_user.id)
    start = datetime.date(int(date_start[:4]), int(date_start[5:7]), int(date_start[8:]))
    today = datetime.date.today()
    days = str(today - start)[:2]

    balance = sq.user_money_balance(message.from_user.id)

    unlock = sq.user_money_unlock(message.from_user.id)

    profit = sq.user_money_profit(message.from_user.id)

    col_ref = sq.col_ref(message.from_user.id)

    photo = open("profile.mp4", 'rb')
    await bot.send_animation(chat_id=message.from_user.id,
                             animation=photo,
                             caption=f'💻Личный кабинет:\n\n'
                             f'📲Депозит: {balance}₽\n'
                             f'♻️Доступно для вывода: {unlock}₽\n'
                             f'🗄ID: <code>{message.from_user.id}</code>\n\n'
                             f'➖➖➖➖➖➖➖➖➖➖➖\n\n'
                             f'ℹ️Статистика пользователя:\n\n'
                             f'┏🕓Дней в системе: {days}\n'
                             f'┣📈Личный заработок: {profit}₽\n'
                             f'┗🚻Приглашено: {col_ref}\n\n'
                             f'➖➖➖➖➖➖➖➖➖➖➖\n'
                             f'CHANE ENTER🪙\n'
                             f'Лимит возможностей - вымысел\n'
                             f'неудачников.',
                             reply_markup=ck.get_ikb_replenishment(),
                             parse_mode='HTML')


@dp.message_handler(Text(equals='🔗Мои рефералы'), state='*')
async def profile(message: types.Message):
    photo = open('my_ref.mp4', 'rb')
    c = sq.my_ref(message.from_user.id)
    a = ''
    n = len(c)
    if n != 0:
        for i in c:
            a += f'ID: {i} - {sq.user_money_balance(i)}₽\n'
    await bot.send_animation(chat_id=message.from_user.id,
                             animation=photo,
                             caption=f'🚻Мои рефералы:\n\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                     f'🛗Количество рефералов: {n}\n\n'
                                     f'{a}\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'📲Реферальный код: <code>{message.from_user.id}</code>',
                             reply_markup=ck.get_kb_join(),
                             parse_mode='HTML')


@dp.message_handler(Text(equals='ℹ️Информация о этапах'), state='*')
async def profile(message: types.Message):
    col_people = sq.users()
    photo = open('info.mp4', 'rb')
    await bot.send_animation(chat_id=message.from_user.id,
                             animation=photo,
                             caption=f'📑Информация о этапах:\n\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'📈{col_people} из 150 вкладчиков.\n\n'
                                     f'⚙️Информация обновляется постоянно!'
                                     f'Единица измерения - 10 вкладчиков.\n\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'Система CHANE ENTER обладает возможностью автоматизированной репродукции.\n'
                                     f'По достижению указанного количества вкладчиков, наступит второй этап жизни системы. '
                                     f'Возможностей станет намного больше: лимит на сумму вложения возрастёт, вырастет допустимое количество активных вкладчиков.\n'
                                     f'Каждое обновление приносит новый этап функционирования системы, продлевая срок жизни и перспективы проекта.',
                             reply_markup=ck.get_ikb_about())


@dp.message_handler(Text(equals='📑О системе'), state='*')
async def profile(message: types.Message):
    photo = open('about.mp4', 'rb')
    await bot.send_animation(chat_id=message.from_user.id,
                             animation=photo,
                             caption=f'⚙️О системе:\n\n'
                                     f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                     f'📚Основная информация:\n\n'
                                     f'1. Основной канал в TELEGRAM.\n'
                                     f'2. Подробная информация, правила, основная механика проекта.\n'
                                     f'3. Подробная информация о этапах системы, на что это влияет. \n'
                                     f'4. Техническая поддержка проекта.',
                             reply_markup=ck.get_ikb_about_sistem())


@dp.callback_query_handler(lambda callback: callback.data == 'etapi')
async def etapi(callback: types.CallbackQuery):
    a = sq.users()
    b = 150 - a
    await callback.message.answer(text=f'Система находится на 1 этапе.\n\n'
                                       f'🚻Количество приглашенных пользователей: {a}\n'
                                       f'♻️Остаток пользователей до обновления системы: {b}',
                                  reply_markup=ck.get_ikb_etapi())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)