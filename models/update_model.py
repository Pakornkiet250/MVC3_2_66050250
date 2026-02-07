from db import get_conn
from models.promise_model import PromiseModel

class PromiseUpdateModel:
    @staticmethod
    def list_updates(promise_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT update_id, update_date, progress_detail
                FROM PromiseUpdates
                WHERE promise_id=?
                ORDER BY update_date DESC, update_id DESC
            """, (promise_id,))
            return cur.fetchall()

    @staticmethod
    def add_update(promise_id: str, update_date: str, progress_detail: str):
      
        if PromiseModel.is_disappeared(promise_id):
            raise ValueError("Promise status is DISAPPEARED. Updates are not allowed.")

        progress_detail = (progress_detail or "").strip()
        if not progress_detail:
            raise ValueError("Progress detail cannot be empty.")

        with get_conn() as conn:
            conn.execute("""
                INSERT INTO PromiseUpdates(promise_id, update_date, progress_detail)
                VALUES (?,?,?)
            """, (promise_id, update_date, progress_detail))
