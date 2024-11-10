from datetime import datetime, timedelta
from app.database import get_mongo_client

class Heartbeat:
    def __init__(self, db):
        self.db = db
        self.last_heartbeat = datetime.now()
        self.sources = []

    def receive_heartbeat(self, source, empresa, sinc):
        self.last_heartbeat = datetime.now()
        
        ping_data = {
            "time": self.last_heartbeat,
            "source": source,
            "empresa": empresa,
            "sinc": sinc
        }

        self.sources.append(ping_data)

        if len(self.sources) > 5:
            self.sources.pop(0)

        self.log_ping_to_mongo(ping_data)

    def log_ping_to_mongo(self, ping_data):
        collection_name = f"pings_{ping_data['time'].year}_{ping_data['time'].month:02d}"
        collection = self.db[collection_name]
        
        collection.insert_one(ping_data)

    def is_heartbeat_missing(self):
        if datetime.now() - self.last_heartbeat > timedelta(minutes=1):
            self.log_absence()
            return True
        return False

    def log_absence(self):
        self.db.absences.insert_one({
            "time": datetime.now(),
            "message": "Heartbeat missing"
        })
