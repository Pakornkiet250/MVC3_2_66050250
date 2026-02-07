import sqlite3

DB_NAME = "promises.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS Politicians(
            politician_id TEXT PRIMARY KEY CHECK(length(politician_id)=8 AND substr(politician_id,1,1)!='0'),
            name TEXT NOT NULL,
            party TEXT NOT NULL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Campaigns(
            campaign_id TEXT PRIMARY KEY,
            election_year INTEGER NOT NULL,
            district TEXT NOT NULL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Promises(
            promise_id TEXT PRIMARY KEY,
            politician_id TEXT NOT NULL,
            campaign_id TEXT NOT NULL,
            detail TEXT NOT NULL,
            announced_date TEXT NOT NULL, -- YYYY-MM-DD
            status TEXT NOT NULL CHECK(status IN ('NOT_STARTED','IN_PROGRESS','DISAPPEARED')),
            FOREIGN KEY(politician_id) REFERENCES Politicians(politician_id),
            FOREIGN KEY(campaign_id) REFERENCES Campaigns(campaign_id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS PromiseUpdates(
            update_id INTEGER PRIMARY KEY AUTOINCREMENT,
            promise_id TEXT NOT NULL,
            update_date TEXT NOT NULL, -- YYYY-MM-DD
            progress_detail TEXT NOT NULL,
            FOREIGN KEY(promise_id) REFERENCES Promises(promise_id)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('USER','ADMIN'))
        )
        """)

def seed_data():
    """ตามโจทย์: นักการเมือง>=5, คำสัญญา>=10 และมีครบทุกสถานะ"""
    with get_conn() as conn:
        c = conn.cursor()

        # Users
        c.execute("INSERT OR IGNORE INTO Users VALUES (?,?,?)", ("user", "1234", "USER"))
        c.execute("INSERT OR IGNORE INTO Users VALUES (?,?,?)", ("admin", "admin", "ADMIN"))

        # Campaigns
        campaigns = [
            ("CMP2027-A", 2027, "District A"),
            ("CMP2027-B", 2027, "District B"),
        ]
        for row in campaigns:
            c.execute("INSERT OR IGNORE INTO Campaigns VALUES (?,?,?)", row)

        # Politicians 
        politicians = [
            ("12345678", "Somchai", "Party Blue"),
            ("23456789", "Ananda", "Party Red"),
            ("34567891", "Kanya", "Party Green"),
            ("45678912", "Prasit", "Party Yellow"),
            ("56789123", "Nicha", "Party Purple"),
        ]
        for row in politicians:
            c.execute("INSERT OR IGNORE INTO Politicians VALUES (?,?,?)", row)

        # Promises 
        promises = [
            ("P001", "12345678", "CMP2027-A", "Increase minimum wage", "2027-01-10", "NOT_STARTED"),
            ("P002", "12345678", "CMP2027-A", "Reduce public transport fares", "2027-01-12", "IN_PROGRESS"),
            ("P003", "23456789", "CMP2027-A", "Build new hospital", "2027-01-08", "DISAPPEARED"),
            ("P004", "23456789", "CMP2027-B", "Scholarship for students", "2027-01-20", "NOT_STARTED"),
            ("P005", "34567891", "CMP2027-B", "Expand green parks", "2027-01-05", "IN_PROGRESS"),
            ("P006", "34567891", "CMP2027-A", "Fix flood drainage", "2027-01-18", "NOT_STARTED"),
            ("P007", "45678912", "CMP2027-A", "Free internet in public areas", "2027-01-02", "DISAPPEARED"),
            ("P008", "45678912", "CMP2027-B", "Improve road safety", "2027-01-22", "IN_PROGRESS"),
            ("P009", "56789123", "CMP2027-B", "Support SMEs loans", "2027-01-15", "NOT_STARTED"),
            ("P010", "56789123", "CMP2027-A", "Increase teachers allowance", "2027-01-25", "IN_PROGRESS"),
        ]
        for row in promises:
            c.execute("INSERT OR IGNORE INTO Promises VALUES (?,?,?,?,?,?)", row)

        # updates 
        updates = [
            ("P002", "2027-02-01", "Draft proposal submitted to committee"),
            ("P005", "2027-02-03", "Surveyed locations for park expansion"),
            ("P008", "2027-02-10", "Started installing new traffic lights"),
            ("P010", "2027-02-12", "Budget request filed"),
        ]
        for row in updates:
            c.execute("""
                INSERT OR IGNORE INTO PromiseUpdates(promise_id, update_date, progress_detail)
                VALUES (?,?,?)
            """, row)
