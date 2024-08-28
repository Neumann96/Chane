import sqlite3


async def add(i, name, ph_num):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()
    try:
        item = []
        item.append(i)
        item.append(name)
        item.append(ph_num)
        cursor.execute('INSERT INTO users(id, user_name, phone_number) VALUES(?, ?, ?);', item)
        connect.commit()
        cursor.close()
    except:
        pass


def check(id):
    try:
        connect = sqlite3.connect('CHANE.db')
        cursor = connect.cursor()

        chat_id = int(id)
        exists = cursor.execute("SELECT 1 FROM users WHERE id = ?", [chat_id]).fetchone()

        if exists:
            return True
        else:
            return False
    except:
        return False


def time(id):
    try:
        sqlite_connection = sqlite3.connect('CHANE.db')
        cursor = sqlite_connection.cursor()

        records = cursor.execute('SELECT date FROM users WHERE id = ?', [id]).fetchall()
        a = str(records[0])
        return a[2:12]
    except:
        pass


def add_ref(id_ref, id_osn):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    chat_id = int(id_osn)
    exists = cursor.execute("SELECT 1 FROM ref WHERE osn_id = ?", [chat_id]).fetchone()
    if exists == None:
        cursor.execute('INSERT INTO ref(osn_id) VALUES(?)', (id_osn,))
        k = 0
        kol = cursor.execute('SELECT * FROM ref WHERE osn_id = ?', (id_osn,)).fetchone()
        for i in kol:
            if i != 0 and i != None:
                k += 1
        c = str('ref' + str(k))

        cursor.execute(f"Update ref set {c} = ? where osn_id = {id_osn}", (id_ref,))
        connect.commit()
    else:
        k = 0
        kol = cursor.execute('SELECT * FROM ref WHERE osn_id = ?', (id_osn,)).fetchone()
        for i in kol:
            if i != None and i != 0:
                k += 1
        c = str('ref' + str(k))

        cursor.execute(f"Update ref set '%s' = ? where osn_id = {id_osn}" % c, (id_ref,))
        connect.commit()
    cursor.close()


def user_money_balance(id):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = ?", (id,))
    result = cursor.fetchone()
    if result:
        return result[0]


def col_ref(id):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()
    a = 0
    try:
        res = cursor.execute('SELECT * FROM ref WHERE osn_id = ?', (id,)).fetchone()
        for i in res:
            if i != None and i != 0:
                a += 1
        return a - 1
    except:
        return a


def user_money_profit(id):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    cursor.execute("SELECT profit FROM users WHERE id = ?", (id,))
    result = cursor.fetchone()
    if result:
        return result[0]


def user_money_unlock(id):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    cursor.execute("SELECT unlock FROM users WHERE id = ?", (id,))
    result = cursor.fetchone()
    if result:
        return result[0]


def set_balance(id, balance):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    sqlite_update_query = """Update users set balance = ? where id = ?"""
    column_values = (balance, id)
    cursor.execute(sqlite_update_query, column_values)
    connect.commit()
    cursor.close()


def user_ref(id_ref):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    row = cursor.execute("SELECT * FROM ref").fetchall()
    for i in range(len(row)):
        for j in range(1, len(row)):
            if str(row[i][j]) == str(id_ref):
                return row[i][0]


def set_profit(id, profit):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    sqlite_update_query = """Update users set profit = ? where id = ?"""
    column_values = (profit, id)
    cursor.execute(sqlite_update_query, column_values)
    connect.commit()
    cursor.close()


def set_unlock(id, unlock):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    sqlite_update_query = """Update users set unlock = ? where id = ?"""
    column_values = (unlock, id)
    cursor.execute(sqlite_update_query, column_values)
    connect.commit()
    cursor.close()


def set_chane_money(id, money):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    sqlite_update_query = """Update users set money_in_chane = ? where id = ?"""
    column_values = (money, id)
    cursor.execute(sqlite_update_query, column_values)
    connect.commit()
    cursor.close()


def users():
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()
    b = 0
    a = cursor.execute("SELECT balance FROM users").fetchall()
    for i in range(len(a)):
        if a[i][0] == 300 or a[i][0] == '300':
            b += 1
    cursor.close()
    return b


def my_ref(id):
    connect = sqlite3.connect('CHANE.db')
    cursor = connect.cursor()

    c = []
    a = cursor.execute("SELECT * FROM ref WHERE osn_id = ?", (id,)).fetchone()
    try:
        for i in a:
            if i != 0 and i != None and i != id:
                c.append(i)
        return c
    except:
        return c