import sqlite3


NAME = "data/db.db"


def get_coins(nickname):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        return cur.execute("""select coins, green_skin, red_skin, yellow_skin, blue_skin from shop where nickname_id =(select id from nicknames where nickname = ?)""", (nickname.strip().lower(),)).fetchone()


def register_users(nickname):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        cur.execute("""insert into nicknames(nickname) values(?)""", (nickname.strip().lower(),))
        id_ = cur.execute("""select id from nicknames where nickname = ?""", (nickname.strip().lower(),)).fetchone()[0]
        cur.execute("""insert into shop values (?, 0, 1, 0, 0, 0)""", (id_,))
        cur.execute("""insert into leaderboards(nickname_id, record) values (?, 0)""", (id_,))


def check_users(nickname):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        return cur.execute("""select id from nicknames where nickname = ?""", (nickname.strip().lower(),)).fetchone()


def change_coins(nickname, coins):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        cur.execute("""update shop set coins = coins + ? where nickname_id = (select id from nicknames where nickname = ?)""", (coins, nickname.strip().lower()))
        con.commit()


def record(nickname, score):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        current_record = cur.execute("""select record from leaderboards where nickname_id = (select id from nicknames where nickname = ?)""", (nickname.strip().lower(),)).fetchone()[0]
        if score > current_record:
            cur.execute("""update leaderboards set record = ? where nickname_id = (select id from nicknames where nickname = ?)""", (score, nickname.strip().lower()))
            con.commit()


def high_record(nickname):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        current_record = cur.execute(
            """select record from leaderboards where nickname_id = (select id from nicknames where nickname = ?)""",
            (nickname.strip().lower(),)).fetchone()[0]
        return current_record


def buy_dino(nickname, color):
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        cur.execute(f"""update shop set {color} = 1 where nickname_id = (select id from nicknames where nickname = ?)""", (nickname.strip().lower(),))
        con.commit()


def get_list_leaderboards():
    with sqlite3.connect(NAME) as con:
        cur = con.cursor()
        results = cur.execute("""select record from leaderboards""").fetchall()
        nicknames = cur.execute("""select nickname from nicknames""").fetchall()
        lst = [(y[0], x[0]) for x, y in zip(results, nicknames)]
        return sorted(lst, key=lambda x: x[1], reverse=True)[:10]