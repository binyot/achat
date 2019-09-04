import sqlite3
import time
timestamp = lambda: time.time()

def connect(path):
    return sqlite3.connect(path)

class Database:
    def __init__(self, conn, schema_path):
        self.conn = conn
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.execute("PRAGMA synchronous = NORMAL")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        with open(schema_path, mode="r") as f:
            self.cursor.executescript(f.read())
        conn.commit()

    def commit(self):
        self.conn.commit()

    def add_user(self, username):
        q = f"""insert into users(username, created_at)
                values('{username}', {timestamp()})
        """
        user_id = self.cursor.execute(q).lastrowid
        return {"user_id": user_id}

    def add_chat(self, name, users):
        q = f"""insert into chats(name, created_at)
                values('{name}', {timestamp()})
        """
        chat_id = self.cursor.execute(q).lastrowid
        for user_id in users:
            self._insert_user_chat(user_id, chat_id)

        return {"chat_id": chat_id}

    def add_message(self, author, chat, text):
        q = f"""insert into messages(author, chat, text, created_at)
                values({author}, {chat}, '{text}', {timestamp()})
        """
        return {"message_id": self.cursor.execute(q).lastrowid}

    def get_messages_in_chat(self, chat):
        q = f"""select *
                from messages
                where chat = {chat}
                order by created_at desc
            """
        rows = self.cursor.execute(q).fetchall()
        return {"messages": [dict(row) for row in rows]}

    def get_chats_with_user(self, user):
        q = f"""select chat_id, name, created_at
                from chats
                join user_chat on chats.id = user_chat.chat_id
                left join (
                    select chat, max(created_at)
                    from messages
                    group by chat
                    ) as latest
                on latest.chat = chats.id
                where user_id = {user}
                order by created_at desc
        """
        rows = self.cursor.execute(q).fetchall()
        return {"chats": [dict(row) for row in rows]}

    def _insert_user_chat(self, user_id, chat_id):
        q = f"""insert into user_chat(user_id, chat_id)
                values({user_id}, {chat_id})
        """
        self.cursor.execute(q)

    def _get_user_id(self, username):
        q = f"""select id from users
                where username = '{username}'
        """
        user_id = self.cursor.execute(q).fetchone()['id']
        return user_id
