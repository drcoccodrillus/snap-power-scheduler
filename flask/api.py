from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

processes = {}

@app.route('/set-shutdown-schedule', methods=['POST'])
def schedule_shutdown():
    try:
        schedule_payload = request.get_json()

        #Cancel any existing schedule
        cancel_shutdown()

        #Write the schedule payload to a file
        file_path = os.path.join(os.environ['SNAP_COMMON'], 'schedule_payload.json')
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w') as file:
            file.write(json.dumps(schedule_payload))

        #Start the scheduler process
        process = subprocess.Popen(['python3', os.path.join(os.environ['SNAP'], 'bin', 'scheduler.py'), file_path])
        processes['scheduler'] = process

        #Write to log file the PID of the scheduler process
        file_path = os.path.join(os.environ['SNAP_COMMON'], 'subprocess_current.log')
        with open(file_path, 'w') as file:
            file.write(str(processes['scheduler'].pid))
        
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

        #Use the scheduler function to clean up the scheduler
        subprocess.Popen(['python3', os.path.join(os.environ['SNAP'], 'bin', 'cancel.py')])

        #Kill the scheduler process
        if 'scheduler' in processes:
            process = processes['scheduler']
            id = process.pid
            process.terminate()
            del processes['scheduler']

            #Write to log file the PID of the latest terminated scheduler process
            file_path = os.path.join(os.environ['SNAP_COMMON'], 'subprocess_terminated.log')
            with open(file_path, 'w') as file:
                file.write(str(id))

        return jsonify(status='OK', message='Shutdown schedule cancelled successfully')
    except Exception as e:
        return jsonify(status='KO', message='Shutdown schedule elimination error', error=str(e))

if __name__ == '__main__':
    app.run()
