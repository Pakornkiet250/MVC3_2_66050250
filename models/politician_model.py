from db import get_conn

class PoliticianModel:
    @staticmethod
    def list_politicians():
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT politician_id, name, party
                FROM Politicians
                ORDER BY name ASC
            """)
            return cur.fetchall()

    @staticmethod
    def get(politician_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT politician_id, name, party
                FROM Politicians WHERE politician_id=?
            """, (politician_id,))
            return cur.fetchone()
