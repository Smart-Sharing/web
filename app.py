from datetime import datetime
import api
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
import pytz # to fix timezones
app = Flask(__name__)


def fetch_session_data(token):
    try:
        sessions = api.get_all_sessions(token)
        print("Sessions fetched: ", sessions)
        machines = api.get_all_machines(token)
        print("Machines fetched: ", machines)
        users = api.get_all_users(token)
        print("Users fetched: ", users)

        MSK = pytz.timezone('Europe/Moscow') # local timezone

        users_dict = {user['id']: user for user in users}

        session_data = []
        for session in sessions:
            user = users_dict.get(session['workerId'])
            machine = next((m for m in machines if m['id'] == session['machineId']), None)

            datetime_start = ""

            if "." in session['datetimeStart']:
                datetime_start = datetime.strptime(session['datetimeStart'], '%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                datetime_start = datetime.strptime(session['datetimeStart'], '%Y-%m-%dT%H:%M:%SZ')

            datetime_finish = ""

            if "." in session['datetimeFinish']:
                datetime_finish = datetime.strptime(session['datetimeFinish'], '%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                datetime_finish = datetime.strptime(session['datetimeFinish'], '%Y-%m-%dT%H:%M:%SZ')

            session_data.append({
                'id': session['id'],
                'machine_id': session['machineId'],
                'state': session['state'],
                'voltage': machine['voltage'] if machine else None,
                'name': user['name'] if user else None,
                'phoneNumber': user['phoneNumber'] if user else None,
                'jobPosition': user['jobPosition'] if user else None,
                'datetimeStart': datetime_start.astimezone(MSK).strftime('%Y-%m-%d %H:%M:%S'),
                'datetimeFinish': datetime_finish.astimezone(MSK).strftime('%Y-%m-%d %H:%M:%S')
            })
        print("Processed session data: ", session_data)
        return session_data
    except Exception as e:
        print(f'Error fetching session data: {e}')
        return None


def fetch_machine_data(token):
    try:
        machines = api.get_all_machines(token)
        sessions = api.get_all_sessions(token)

        machine_data = []
        for machine in machines:
            try:
                current_session = next((s for s in sessions if s['machineId'] == machine['id'] and s['state'] == 0), None)
                user = api.get_user(current_session['workerId'], token) if current_session else None

                machine_data.append({
                    'id': machine['id'],
                    'parkingId': machine['parking_id'],
                    'state': machine['state'],
                    'voltage': machine['voltage'],
                    'user': user['name'] if user else None
                })
            except Exception as e:
                print(f'Error processing machine {machine["id"]}: {e}')
        return machine_data
    except Exception as e:
        print(f'Error: {e}')
        return "something went wrong"
    

# New method to fetch machine data for each parking
def fetch_parking_machines_data(token, parking_name):
    try:
        machines = api.get_parking_machines(token, parking_name)
        sessions = api.get_all_sessions(token)

        machine_data = []
        for machine in machines:
            try:
                current_session = next((s for s in sessions if s['machineId'] == machine['id'] and s['state'] == 0), None)
                user = api.get_user(current_session['workerId'], token) if current_session else None

                machine_data.append({
                    'id': machine['id'],
                    'parkingId': machine['parking_id'],
                    'state': machine['state'],
                    'voltage': machine['voltage'],
                    'user': user['name'] if user else None
                })
            except Exception as e:
                print(f'Error processing machine {machine["id"]}: {e}')
        return machine_data
    except Exception as e:
        print(f'Error: {e}')
        return "something went wrong"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phoneNumber']
        password = request.form['password']
        response = requests.post("http://backend:8080/login", json={
            'phone_number': phone_number,
            'password': password
        })
        if response.status_code == 200 and (response.json().get('token')) != None:
            token = response.json().get('token')
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('token', token)
            return resp
        else:
            print("Это токен", response.json().get('token'))
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


def get_token():
    return request.cookies.get('token')


@app.route('/')
def index():
    token = get_token()
    if not token:
        return redirect(url_for('login'))
    sessions = fetch_session_data(token)
    print("Sessions in index: ", sessions)
    return render_template('index.html', sessions=sessions)


@app.route('/get_session_data')
def get_session_data():
    token = get_token()
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    session_data = fetch_session_data(token)
    print(session_data)
    if session_data == "Something went wrong":
        return jsonify({'error': 'Internal Server Error'}), 500
    return jsonify({'sessions': session_data})


@app.route('/machines')
def machines():
    token = get_token()
    if not token:
        return redirect(url_for('login'))
    return render_template('machines.html')


# New route to get machine data for each parking (tested)
@app.route('/parking_machines/<parking_name>')
def parking_machines(parking_name):
    token = get_token()
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    machine_data = fetch_parking_machines_data(token, parking_name)
    if machine_data is None:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'machines': machine_data})


@app.route('/get_machine_data')
def get_machine_data():
    token = get_token()
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    machine_data = fetch_machine_data(token)
    if machine_data is None:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'machines': machine_data})


@app.route('/unlock_machine', methods=['POST'])
def unlock_machine():
    data = request.get_json()
    machine_id = data.get('machine_id')
    token = get_token()
    if not token or not machine_id:
        return jsonify({'error': 'Invalid request'}), 400


    result = api.unlock_machine(token, machine_id)
    if result.get('status'):
        return jsonify({'message': 'Machine unlocked successfully'})
    else:
        return jsonify({'error': 'Failed to unlock machine'}), 500
    

@app.route('/stop_machine', methods=['POST'])
def stop_machine():
    data = request.get_json()
    machine_id = data.get('machine_id')
    token = get_token()
    if not token or not machine_id:
        return jsonify({'error': 'Invalid request'}), 400

    result = api.lock_machine(token, machine_id)
    if result.get('status'):
        return jsonify({'message': 'Machine unlocked successfully'})
    else:
        return jsonify({'error': 'Failed to unlock machine'}), 500


@app.route('/machine/<machine_id>')
def machine_page(machine_id):
    token = get_token()
    if not token:
        return redirect(url_for('login'))

    machine_info = api.get_machine(token, machine_id)
    if machine_info is None:
        return "Ошибка получения данных о машине", 500

    # Определяем состояние машины
    if machine_info['state'] == 0:
        machine_status = 'Свободна'
    else:
        machine_status = 'Используется'

    return render_template('machine.html', machine=machine_info, status=machine_status)


@app.route('/api/machine/<machine_id>')
def api_machine(machine_id):
    token = get_token()
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    machine_info = api.get_machine(token, machine_id)
    if machine_info is None:
        return jsonify({"error": "Error fetching machine data"}), 500

    # Определяем состояние машины
    if machine_info['state'] == 0:
        machine_status = 'Свободна'
    else:
        machine_status = 'Используется'

    return jsonify({
        "machine": machine_info,
        "status": machine_status
    })


# New methods for parking places
# (tested)
@app.route('/parkings')
def parkings():
    token = get_token()
    if not token:
        return redirect(url_for('login'))
    return render_template('parkings.html')

# (tested)
@app.route('/get_parkings_data')
def get_parkings_data():
    token = get_token()
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    parkings_data = api.get_all_parkings(token)
    print(parkings_data)
    if parkings_data == "Something went wrong":
        return jsonify({'error': 'Internal Server Error'}), 500
    return jsonify({'parkings': parkings_data})


# (tested)
@app.route('/add_machine', methods=['POST'])
def add_machine():
    data = request.get_json()
    machine_id = data.get('machine_id')
    parking_id = data.get('parking_id')
    token = get_token()
    if not token or not machine_id or not parking_id:
        return jsonify({'error': 'Invalid request'}), 400

    result = api.manualy_add_machine(token, parking_id, machine_id)
    if result.get('status'):
        return jsonify({'message': 'Machine added successfully'})
    else:
        return jsonify({'error': 'Failed to add machine'}), 500


# (tested)
@app.route('/register_parking', methods=['POST'])
def register_parking():
    data = request.get_json()
    name = data.get('name')
    mac_addr = data.get('mac_addr')
    capacity = data.get('capacity')
    token = get_token()
    if not token or not name or not mac_addr:
        return jsonify({'error': 'Invalid request'}), 400

    result = api.register_parking(token, name, mac_addr, capacity)
    if result.get('status'):
        return jsonify({'message': 'Parking registered successfully'})
    else:
        return jsonify({'error': 'Failed to register new parking'}), 500


# (tested)
@app.route('/update_parking_state', methods=['POST'])
def update_parking_state():
    data = request.get_json()
    parking_id = data.get('parking_id')
    state = data.get('state')
    token = get_token()
    if not token or not parking_id or not state:
        return jsonify({'error': 'Invalid request'}), 400

    result = api.update_parking_state(token, parking_id, state)
    if result.get('status'):
        return jsonify({'message': 'Parking state updated successfully'})
    else:
        return jsonify({'error': 'Failed to update parking state'}), 500


# (tested)
@app.route('/update_parking_capacity', methods=['POST'])
def update_parking_capacity():
    data = request.get_json()
    parking_id = data.get('parking_id')
    capacity = data.get('capacity')
    token = get_token()
    if not token or not parking_id:
        return jsonify({'error': 'Invalid request'}), 400

    result = api.update_parking_capacity(token, parking_id, capacity)
    if result.get('status'):
        return jsonify({'message': 'Parking capacity updated successfully'})
    else:
        return jsonify({'error': 'Failed update parking capacity'}), 500


# New methods to work with qr-codes and parking zone
# (tested)
@app.route('/parking/<parking_name>')
def parking(parking_name):
    token = get_token()
    if not token:
        return redirect(url_for('login'))
    return render_template('parking.html', name=parking_name)


# (tested)
@app.route('/get_qr_key')
def get_qr_key():
    token = get_token()
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    data = api.get_qr_key(token)
    print(data)
    if data == "Something went wrong":
        return jsonify({'error': 'Internal Server Error'}), 500
    return jsonify({'qr_key': data['qr_key'], 'local_ip': data['local_ip']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
