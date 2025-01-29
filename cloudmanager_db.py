import threading

from sqlalchemy.orm import sessionmaker

import cm_dashboards.alchemy_db as db

lock = threading.Lock()
db_engines = {}


def get_db_engine(jobrun_id):
    """
    Retrieve a stored SQL Alchemy engine, using jobrun as a key
    Create if doesn't exist
    """
    global db_engines
    # Use lock to avoid multiple same entry creations
    lock.acquire()
    try:
        if jobrun_id not in db_engines:
            db_engines[jobrun_id] = CloudManagerDB(jobrun_id)
    finally:
        lock.release()
    return db_engines[jobrun_id]


class CloudManagerDB:
    DB_ENGINE = None
    # DB_METADATA = None
    Session = None

    def __init__(self, jobrun):
        self.jobrun = jobrun
        # Get connection to Cloud Manager DB
        self.dashboard_url = db.get_db_connection_url(jobrun)
        self.DB_ENGINE = db.get_db_engine(self.dashboard_url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.DB_ENGINE)

    def get_session(self):
        """
        Get SQL Alchemy session
        """
        return self.Session()

    def get_engine(self):
        """
        Get SQL Alchemy engine
        """
        return self.DB_ENGINE
