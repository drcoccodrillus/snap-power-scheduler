from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/set-shutdown-schedule', methods=['POST'])
def schedule_shutdown():
    try:
        schedule_payload = request.get_json()
        file_path = os.path.join(os.environ['SNAP_COMMON'], 'schedule_payload.json')
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w') as file:
            file.write(json.dumps(schedule_payload))
        subprocess.Popen(['python3', os.path.join(os.environ['SNAP'], 'bin', 'scheduler.py'), file_path])
        return jsonify(status='OK', message='Shutdown schedule set successfully')
    except Exception as e:
        return jsonify(status='KO', message='Shutdown schedule set error', error=str(e))

@app.route('/cancel-shutdown-schedule', methods=['GET'])
def cancel_shutdown():
    try:
        file_path = os.path.join(os.environ['SNAP_COMMON'], 'schedule_payload.json')
        schedule_payload = {
            "mon": None,
            "tue": None,
            "wed": None,
            "thu": None,
            "fri": None,
            "sat": None,
            "sun": None
        }
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w') as file:
            file.write(json.dumps(schedule_payload))
        subprocess.Popen(['python3', os.path.join(os.environ['SNAP'], 'bin', 'cancel.py')])
        return jsonify(status='OK', message='Shutdown schedule cancelled successfully')
    except Exception as e:
        return jsonify(status='KO', message='Shutdown schedule cancelled error', error=str(e))

if __name__ == '__main__':
    app.run()
