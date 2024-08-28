from aiogram.types import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# import main

hello_message = '''
🔹 <b>CHANE ENTER</b> - финансовый проект, предоставляющий услуги взаимовыгодной реферальной программы, система аккумулирования средств. 

Важно понимать, что в любой финансовой сфере существуют риски, связанные с инвестированием и торговлей. Поэтому никакая биржа или компания не может дать полные гарантии прибыли или отсутствия рисков. Тем не менее, CHANE ENTER может предоставить своим клиентам некоторые гарантии, чтобы обеспечить надежность и безопасность своих услуг.

Некоторые возможные гарантии, которые может предоставить CHANE ENTER, включают в себя:

🔒 <b>Безопасность средств клиентов:</b> CHANE ENTER гарантирует сохранность средств клиентов на отдельных банковских счетах, отделенных от собственных средств компании. Это обеспечивает защиту пользователей от возможных финансовых рисков, связанных с банкротством системы.

🌐 <b>Прозрачность и открытость:</b> CHANE ENTER предоставляет полную информацию о своих услугах, комиссиях, правилах и условиях, а также предоставляет своим клиентам возможность проверять свои счета.

🦹🏼‍♂️ <b>Обучение и поддержка:</b> CHANE ENTER предоставляет полную поддержку своим клиентам, помогая им улучшать свои торговые навыки и получать доступ к актуальной информации и аналитике.

📲 <b>Удобство и доступность:</b> CHANE ENTER предоставляет удобную и простую платформу для торговли, а также поддерживает широкий спектр способов пополнения и вывода средств.

Тем не менее, напоминаем, что никакая компания или биржа не может дать 100%-ю гарантию на инвестиции. Поэтому, перед тем как начать инвестировать, настоятельно рекомендуется ознакомиться с правилами и условиями инвестиционного проекта и тщательно изучить все возможные риски.

<b>Нажимая «Прочитал✅»</b>, вы автоматически принимаете все условия и правила сервиса.
'''

c = ''


def get_ikb_about_sistem():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Канал📚', url='https://t.me/chane_enter'),
            InlineKeyboardButton(text='Информация📃', url='https://telegra.ph/OTVETY-NA-VOPROSY-05-11-4'),
            InlineKeyboardButton(text='Этапы📊', callback_data='etapi'),
            InlineKeyboardButton(text='Тех.поддержка⚙️', url='https://t.me/chane_support'))
    return ikb


def get_ikb_etapi():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Подробнее', url='https://telegra.ph/EHtapy-05-13'))
    return ikb


def get_ikb_start():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='ЗДЕСЬ ССЫЛКУ НА ОСНОВ КАНАЛ МБ ПРИКРЕПИТЬ', url='https://t.me/v1ncenttt'),
            InlineKeyboardButton(text='Присоединиться!', callback_data='join'))
    return ikb


def get_kb_join():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(KeyboardButton(text='💼Личный кабинет'), KeyboardButton(text='🔗Мои рефералы'),
           KeyboardButton(text='ℹ️Информация о этапах'), KeyboardButton(text='📑О системе'))
    return kb


def get_ikb_replenishment():
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb.add(InlineKeyboardButton(text='➕Пополнение', callback_data='up'),
            InlineKeyboardButton(text='➖Вывод', callback_data='down'),
            InlineKeyboardButton(text='Техническая поддержка', url='https://t.me/chane_support'))
    return ikb


def get_ikb_back():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='⬅️Назад', callback_data='back'))
    return ikb


def get_ikb_sogl():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Прочитал✅', callback_data='agree'))
    return ikb


def get_kb_phone_number():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton(text='☎️Поделиться номером телеофна'))
    return kb


def get_ikb_sub():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Наш основной канал', url='https://t.me/chane_enter'),
            InlineKeyboardButton(text='Подписался!', callback_data='sub'))
    return ikb


def get_ikb_about():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Подробнее🔩', url='https://t.me/chane_enter'))
    return ikb


def get_ikb_check():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Аккаунт поддержки', url='https://t.me/v1ncenttt'),
            InlineKeyboardButton(text='Проверить платеж✅', callback_data='check'))
    return ikb


def get_kb_menu_admin():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text='Подтвердить ПЛАТЕЖ пользователя'),
           KeyboardButton(text='Подтвердить ВЫВОД пользователя'))
    return kb


def ikb_check():
    c = 'right' + str(main.ID)
    print(main.ID)
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='ПОДТВЕРДИТЬ ПЛАТЕЖ', callback_data=c))
    return ikb