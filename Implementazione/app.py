from flask import Flask, request, jsonify
from tasks import *

app = Flask(__name__)

#  DEFINIZIONE DELLE RICHIESTE HTTP

@app.route('/scan', methods=['POST'])
def scan():
    ip_address = request.json.get('ip_address')

    if not ip_address:
        return jsonify({'errore': 'IP richiesto'}), 400

    result = run_scans.delay(ip_address)
    return jsonify({'task_id': result.task_id}), 202

@app.route('/scantime', methods=['POST'])
def scan_time():
    ip_address = request.json.get('ip_address')
    time = request.json.get('time')

    if ip_address is None and time < 1:
        return jsonify({'errore': 'IP e time richiesti'}), 400
    result = run_scans_time.delay(ip_address, time)
    return jsonify({'task_id': result.task_id}), 202
"""
@app.route('/stop', methods= ['POST'])
def stop_task():
    flag = request.json.get('flag')
    if flag == int(1):
        print("ANNULLO ULTIMO TASK: " + last_id)
        stop.delay()
    return jsonify({'task_id': "ID_STOP"}), 202
"""
@app.route('/stop', methods= ['POST'])
def stop_scan():
    result = stop.delay()
    return jsonify({'task_id': result.task_id}), 202


@app.route('/scanport', methods=['POST'])
def scan_port():
    ip_address = request.json.get('ip_address')
    port = request.json.get('port')
    if not ip_address or not port:
        return jsonify({'errore': 'IP e porte richiesti'}), 400
    result = run_scan_port.delay(ip_address, port)
    return jsonify({'task_id': result.task_id}), 202


@app.route('/scanservice', methods=['POST'])
def scan_service():
    ip_address = request.json.get('ip_address')
    if not ip_address:
        return jsonify({'errore': 'IP richiesto'}), 400
    result = run_scan_service.delay(ip_address)
    return jsonify({'task_id': result.task_id}), 202


@app.route('/scanos', methods=['POST'])
def scan_os():
    ip_address = request.json.get('ip_address')
    if not ip_address:
        return jsonify({'errore': 'IP richiesto'}), 400
    result = run_scan_os.delay(ip_address)
    return jsonify({'task_id': result.task_id}), 202


@app.route('/scanvuln', methods=['POST'])
def scan_vuln():
    ip_address = request.json.get('ip_address')
    if not ip_address:
        return jsonify({'errore': 'IP richiesto'}), 400
    result = run_scan_vuln.delay(ip_address)
    return jsonify({'task_id': result.task_id}), 202


if __name__ == '__main__':
    app.run(debug=True, port=9090)

