from db import get_conn

class PromiseModel:
    @staticmethod
    def list_all_promises():
        # ตามโจทย์: เรียงตามวันที่ประกาศ
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT p.promise_id, p.detail, p.announced_date, p.status,
                       pol.politician_id, pol.name, pol.party,
                       c.campaign_id, c.election_year, c.district
                FROM Promises p
                JOIN Politicians pol ON pol.politician_id = p.politician_id
                JOIN Campaigns c ON c.campaign_id = p.campaign_id
                ORDER BY p.announced_date DESC
            """)
            return cur.fetchall()

    @staticmethod
    def get_promise(promise_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT p.promise_id, p.detail, p.announced_date, p.status,
                       pol.politician_id, pol.name, pol.party,
                       c.campaign_id, c.election_year, c.district
                FROM Promises p
                JOIN Politicians pol ON pol.politician_id = p.politician_id
                JOIN Campaigns c ON c.campaign_id = p.campaign_id
                WHERE p.promise_id=?
            """, (promise_id,))
            return cur.fetchone()

    @staticmethod
    def list_promises_by_politician(politician_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT p.promise_id, p.detail, p.announced_date, p.status
                FROM Promises p
                WHERE p.politician_id=?
                ORDER BY p.announced_date DESC
            """, (politician_id,))
            return cur.fetchall()

    @staticmethod
    def is_disappeared(promise_id: str) -> bool:
        with get_conn() as conn:
            cur = conn.execute("SELECT status FROM Promises WHERE promise_id=?", (promise_id,))
            row = cur.fetchone()
            return (row is not None) and (row[0] == "DISAPPEARED")
