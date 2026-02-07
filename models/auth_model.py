from db import get_conn

class AuthModel:
    @staticmethod
    def login(username: str, password: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT username, role
                FROM Users
                WHERE username=? AND password=?
            """, (username.strip(), password.strip()))
            return cur.fetchone()
