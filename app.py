import requests
import time
import random
import string
import threading
from flask import Flask, render_template_string

app = Flask(__name__)

# Lista de URLs Replit
URLS = [
    "https://67dec50d-bc6f-45f0-babe-45029e97dbfb-00-2f8src31cuzta.janeway.replit.dev/keepalive",
    "https://5c2543a6-a058-49cb-86b7-51a320e5a91c-00-f32zkz78peig.picard.replit.dev/keepalive",
    "https://d74d67c2-81c1-463a-937e-0b57c6d703c1-00-15649h9fk0t3.janeway.replit.dev/keepalive",
    "https://dd1acbcc-cfde-4039-a629-c6a4daba5548-00-1dvh8mz4wv6px.picard.replit.dev/keepalive",
    "https://1f3cbf60-ad8c-468d-a9ff-e86fd9b40d98-00-xed93wxmjs7z.picard.replit.dev/keepalive",
    "https://92d73889-dd7d-469e-a409-53169d9d5850-00-3q5qnulynj9gc.janeway.replit.dev/keepalive"
]

# Diccionario para almacenar el estado de cada URL
status_dict = {url: {"status": "🟡 Pendiente", "code": None, "payload": {}} for url in URLS}

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
        code = res.status_code
        if code == 200:
            status = "🟢 Activo"
        else:
            status = f"🟡 Código {code}"
        print(f"[{url}] {code} - {res.text} | Payload: {payload}")
    except Exception as e:
        code = None
        status = "🔴 Error"
        print(f"[ERROR] {url} - {e}")
    # Actualiza el estado
    status_dict[url] = {"status": status, "code": code, "payload": payload}

def ciclo_keepalive():
    while True:
        print("🔁 Enviando keepalive a todos los proyectos...")
        for url in URLS:
            ping(url)
            time.sleep(2)
        print("🕒 Esperando 10 minutos...")
        time.sleep(600)

# Inicia el ping automático en segundo plano
threading.Thread(target=ciclo_keepalive, daemon=True).start()

# Ruta básica
@app.route("/", methods=["GET"])
def index():
    return "✅ Servicio activo. Keepalives en ejecución."

# Ruta con interfaz visual
@app.route("/status", methods=["GET"])
def status():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Status de Replits</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 20px; }
            table { border-collapse: collapse; width: 100%; background-color: #fff; }
            th, td { border: 1px solid #ccc; padding: 12px; text-align: left; }
            th { background-color: #333; color: white; }
            .green { background-color: #c8e6c9; }
            .yellow { background-color: #fff9c4; }
            .red { background-color: #ffcdd2; }
        </style>
    </head>
    <body>
        <h2>🔍 Estado de tus Replits</h2>
        <table>
            <tr>
                <th>URL</th>
                <th>Estado</th>
                <th>Código</th>
                <th>Payload Enviado</th>
            </tr>
            {% for url, data in status_dict.items() %}
                {% set css_class = "yellow" %}
                {% if "🟢" in data.status %}
                    {% set css_class = "green" %}
                {% elif "🔴" in data.status %}
                    {% set css_class = "red" %}
                {% endif %}
                <tr class="{{ css_class }}">
                    <td>{{ url }}</td>
                    <td>{{ data.status }}</td>
                    <td>{{ data.code if data.code else "N/A" }}</td>
                    <td>{{ data.payload }}</td>
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, status_dict=status_dict)

# Inicia servidor Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
