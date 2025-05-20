import requests
import time
import random
import string
import threading
from flask import Flask

app = Flask(__name__)

# Tu lista de URLs Replit
URLS = [
    "https://67dec50d-bc6f-45f0-babe-45029e97dbfb-00-2f8src31cuzta.janeway.replit.dev/keepalive"
]

def generar_payload():
    return {
        "valor": random.randint(1000, 100000),
        "texto": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        "activo": random.choice([True, False])
    }

def ping(url):
    payload = generar_payload()
    try:
        res = requests.post(url, json=payload, timeout=10)
        print(f"[{url}] {res.status_code} - {res.text} | Payload: {payload}")
    except Exception as e:
        print(f"[ERROR] {url} - {e}")

def ciclo_keepalive():
    while True:
        print("🔁 Enviando keepalive a todos los proyectos...")
        for url in URLS:
            ping(url)
            time.sleep(2)
        print("🕒 Esperando 10 minutos...")
        time.sleep(600)

# Iniciar el hilo de keepalive en segundo plano
threading.Thread(target=ciclo_keepalive, daemon=True).start()

# Endpoint GET para mantener Render activo
@app.route("/", methods=["GET"])
def index():
    return "✅ Servicio activo. Keepalives en ejecución.", 200

# Iniciar servidor Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
