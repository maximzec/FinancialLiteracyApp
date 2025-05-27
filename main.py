from flask import Flask, request, jsonify
from datetime import datetime, timezone, timedelta
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'
USAGE_FILE = 'data_usage.json'  # отдельный файл для использования

# Изначально, если нет файлов, создаём их
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)
if not os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

@app.route('/api/update', methods=['POST'])
def update_data():
    # Здесь данные о новых уникальных пользователях
    data = request.get_json()
    if not data or 'timestamp' not in data or 'usage_count' not in data:
        return jsonify({"error": "Invalid data"}), 400

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        candles = json.load(f)
    candles.append(data)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(candles, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "ok"}), 200

@app.route('/api/update_usage', methods=['POST'])
def update_usage():
    # Здесь данные о количестве использований (каждое использование отправляет usage_count=1)
    data = request.get_json()
    if not data or 'timestamp' not in data or 'usage_count' not in data:
        return jsonify({"error": "Invalid data"}), 400

    with open(USAGE_FILE, 'r', encoding='utf-8') as f:
        usage_data = json.load(f)
    usage_data.append(data)
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(usage_data, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "ok"}), 200

@app.route('/api/candles', methods=['GET'])
def get_candles():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        candles = json.load(f)

    # Вычисляем сегодняшнюю полуночь по UTC
    now_utc = datetime.now(timezone.utc)
    today_midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)

    # Фильтруем данные, оставляя только записи за текущий день
    todays_data = []
    for c in candles:
        dt = datetime.fromisoformat(c['timestamp'])
        if dt >= today_midnight_utc:
            todays_data.append(c)

    # Аггрегируем по часу уникальных пользователей
    aggregated = {}
    for c in todays_data:
        dt = datetime.fromisoformat(c['timestamp'])
        hour_str = dt.strftime("%H:00")
        aggregated[hour_str] = aggregated.get(hour_str, 0) + c['usage_count']

    result = [{"time": k, "users": v} for k, v in aggregated.items()]
    result.sort(key=lambda x: x['time'])
    return jsonify(result), 200

@app.route('/api/candles_usage', methods=['GET'])
def get_candles_usage():
    with open(USAGE_FILE, 'r', encoding='utf-8') as f:
        usage_data = json.load(f)

    # Вычисляем сегодняшнюю полуночь по UTC
    now_utc = datetime.now(timezone.utc)
    today_midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)

    # Фильтруем данные, оставляя только записи за текущий день
    todays_usage = []
    for c in usage_data:
        dt = datetime.fromisoformat(c['timestamp'])
        if dt >= today_midnight_utc:
            todays_usage.append(c)

    # Аггрегируем по часу количество использований
    aggregated = {}
    for c in todays_usage:
        dt = datetime.fromisoformat(c['timestamp'])
        hour_str = dt.strftime("%H:00")
        aggregated[hour_str] = aggregated.get(hour_str, 0) + c['usage_count']

    result = [{"time": k, "users": v} for k, v in aggregated.items()]
    result.sort(key=lambda x: x['time'])
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
