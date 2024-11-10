from datetime import datetime, timedelta
from app.database import get_mongo_client

class Heartbeat:
    def __init__(self, db):
        self.db = db  # Armazena a instância do banco de dados
        self.last_heartbeat = datetime.now()
        self.sources = []

    def receive_heartbeat(self, source, empresa, sinc):
        self.last_heartbeat = datetime.now()
        
        # Estrutura do ping recebido
        ping_data = {
            "time": self.last_heartbeat,
            "source": source,
            "empresa": empresa,
            "sinc": sinc
        }

        # Adiciona o ping à lista de fontes ativas para exibição no frontend
        self.sources.append(ping_data)

        # Limita o histórico na memória a 5 entradas
        if len(self.sources) > 5:
            self.sources.pop(0)

        # Salva o ping no MongoDB
        self.log_ping_to_mongo(ping_data)

    def log_ping_to_mongo(self, ping_data):
        # Define o nome da coleção com base no mês atual
        collection_name = f"pings_{ping_data['time'].year}_{ping_data['time'].month:02d}"
        collection = self.db[collection_name]
        
        # Insere o ping na coleção mensal
        collection.insert_one(ping_data)

    def is_heartbeat_missing(self):
        if datetime.now() - self.last_heartbeat > timedelta(minutes=1):
            self.log_absence()
            return True
        return False

    def log_absence(self):
        # Salva uma ausência no MongoDB
        self.db.absences.insert_one({
            "time": datetime.now(),
            "message": "Heartbeat missing"
        })
