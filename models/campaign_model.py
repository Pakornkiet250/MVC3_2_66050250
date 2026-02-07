from db import get_conn

class CampaignModel:
    @staticmethod
    def get(campaign_id: str):
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT campaign_id, election_year, district
                FROM Campaigns WHERE campaign_id=?
            """, (campaign_id,))
            return cur.fetchone()
