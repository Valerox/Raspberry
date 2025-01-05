from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import platform
import socket

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/system', methods=['GET'])
def getSystemInfo():
    disk = psutil.disk_usage('/')
    print(socket.gethostname())
    def get_cpu_temp():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read()) / 1000.0
            return temp
        except FileNotFoundError:
            return "CPU-Temperatur konnte nicht gefunden werden."
        
    return jsonify({
        'hostname': socket.gethostname(),
        'platform': platform.platform(),
        'architecture': platform.architecture(),
        'cpu_temperature': get_cpu_temp(),
        'cpu_usage': psutil.cpu_percent(percpu=True),
        'storage_used': round(disk.used / (1024**3), 2),
        'storage_total': round(disk.total / (1024**3), 2),
    })

if __name__ == '__main__':
    app.run(debug=True)