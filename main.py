import io
import socket
import threading
import webbrowser

import qrcode
from flask import Flask, render_template_string, request, send_file
from flask_sock import Sock

from html_page import HTML
from phoneHTML import HTML_phone

UDP_PORT = 33333
TCP_PORT = 4444
WEB_PORT = 8080

app = Flask(__name__)
sock = Sock(app)

esp_conn = None
esp_lock = threading.Lock()
web_clients = set()
web_clients_lock = threading.Lock()


def log(msg, to_web=True):
    print(msg)

    if not to_web:
        return

    with web_clients_lock:
        clients = list(web_clients)

    dead_clients = []

    for client in clients:
        try:
            client.send(msg)
        except Exception:
            dead_clients.append(client)

    if dead_clients:
        with web_clients_lock:
            for client in dead_clients:
                web_clients.discard(client)


def get_local_ip():
    sock_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock_ip.connect(("8.8.8.8", 80))
        ip = sock_ip.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        sock_ip.close()

    return ip


def build_urls():
    local_ip = get_local_ip()
    desktop_url = f"http://{local_ip}:{WEB_PORT}"
    phone_url = f"{desktop_url}/phone"
    return desktop_url, phone_url


@app.after_request
def add_no_cache_headers(response):
    if request.path in {"/", "/phone", "/qr"}:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.route("/")
def index():
    desktop_url, phone_url = build_urls()
    return render_template_string(
        HTML,
        desktop_url=desktop_url,
        phone_url=phone_url,
    )


@app.route("/phone")
def phone():
    desktop_url, phone_url = build_urls()
    return render_template_string(
        HTML_phone,
        desktop_url=desktop_url,
        phone_url=phone_url,
    )


@sock.route("/ws")
def websocket(ws):
    with web_clients_lock:
        web_clients.add(ws)

    log("[WEB] Client connecté", to_web=False)

    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break

            with esp_lock:
                if esp_conn:
                    esp_conn.sendall(msg.encode())
                    log(f"[PC → ESP] {msg.rstrip()}")
                else:
                    log("[ERREUR] Aucun ESP connecté")

    except Exception as exc:
        log(f"[WEB] Erreur WebSocket : {exc}", to_web=False)

    finally:
        with web_clients_lock:
            web_clients.discard(ws)

        log("[WEB] Client déconnecté", to_web=False)


@app.route("/qr")
def qr_code():
    _, phone_url = build_urls()
    img = qrcode.make(phone_url)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")

def udp_discovery_server():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp.bind(("", UDP_PORT))

    print(f"[UDP] Discovery sur 0.0.0.0:{UDP_PORT}")

    while True:
        data, addr = udp.recvfrom(1024)
        msg = data.decode(errors="ignore").strip()

        print(f"[UDP] {addr} → {msg}")

        if msg == "PN_PING":
            response = f"PN_PONG:{TCP_PORT}".encode()
            udp.sendto(response, addr)
            print(f"[UDP] Réponse envoyée : PN_PONG:{TCP_PORT}")

def handle_esp(conn, addr):
    global esp_conn

    with esp_lock:
        esp_conn = conn

    log(f"[TCP] ESP connecté : {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode(errors="replace").rstrip()
            log(f"[ESP → PC] {text}")

    except ConnectionResetError:
        pass

    finally:
        with esp_lock:
            if esp_conn == conn:
                esp_conn = None

        conn.close()
        log(f"[TCP] ESP déconnecté : {addr}")

def tcp_server():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind(("", TCP_PORT))
    tcp.listen(1)

    log(f"[TCP] Serveur sur 0.0.0.0:{TCP_PORT}")

    while True:
        conn, addr = tcp.accept()
        threading.Thread(
            target=handle_esp,
            args=(conn, addr),
            daemon=True
        ).start()


if __name__ == "__main__":
    threading.Thread(target=udp_discovery_server, daemon=True).start()
    threading.Thread(target=tcp_server, daemon=True).start()

    desktop_url, phone_url = build_urls()
    local_url = f"http://localhost:{WEB_PORT}"

    log(f"[WEB] Interface locale : {local_url}", to_web=False)
    log(f"[WEB] Interface réseau : {desktop_url}", to_web=False)
    log(f"[WEB] Interface téléphone : {phone_url}", to_web=False)

    threading.Timer(1.0, lambda: webbrowser.open(local_url)).start()

    app.run(host="0.0.0.0", port=WEB_PORT, threaded=True)
