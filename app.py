import requests
import time
import random
import string

# Lista de tus proyectos (URLs del endpoint /keepalive de Replit)
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

while True:
    print("🔁 Enviando keepalive a todos los proyectos...")
    for url in URLS:
        ping(url)
        time.sleep(2)  # pequeño delay entre pings para no saturar
    print("🕒 Esperando 10 minutos...")
    time.sleep(600)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
