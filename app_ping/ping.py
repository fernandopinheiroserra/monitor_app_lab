import time
import requests
import random
import string

HEADERS = {
    "User-Agent": "PingEmulator/1.0 (Python Requests)",
    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \"Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

def generate_random_name(prefix, length=6):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return f"{prefix}{random_string}"

def send_ping():
    empresa = generate_random_name("empresa_")
    sinc = generate_random_name("sinc_")

    ping_url = f"http://master_alert:8000/ping?empresa={empresa}&sinc={sinc}"

    try:
        response = requests.get(ping_url, headers=HEADERS)
        if response.status_code == 200:
            print(f"Ping enviado com sucesso! Empresa: {empresa}, Sinc: {sinc}")
        else:
            print(f"Falha ao enviar o ping: Código de status {response.status_code}")
    except requests.RequestException as e:
        print(f"Erro ao enviar o ping: {e}")

def start_ping_emulator(interval=10):
    print("Iniciando emulador de ping...")
    while True:
        send_ping()
        time.sleep(interval)

if __name__ == "__main__":
    start_ping_emulator()
