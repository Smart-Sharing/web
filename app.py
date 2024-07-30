from datetime import datetime
import api
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
app = Flask(__name__)

def fetch_session_data(token):
    try:
        sessions = api.get_all_sessions(token)
        print("Sessions fetched: ", sessions)
        machines = api.get_all_machines(token)
        print("Machines fetched: ", machines)
        users = api.get_all_users(token)
        print("Users fetched: ", users)


        users_dict = {user['id']: user for user in users}

        session_data = []
        for session in sessions:
            user = users_dict.get(session['workerId'])
            machine = next((m for m in machines if m['id'] == session['machineId']), None)

            datetime_start = datetime.strptime(session['datetimeStart'], '%Y-%m-%dT%H:%M:%SZ')
            datetime_finish = datetime.strptime(session['datetimeFinish'], '%Y-%m-%dT%H:%M:%SZ')

            session_data.append({
                'id': session['id'],
                'machine_id': session['machineId'],
                'state': session['state'],
                'voltage': machine['voltage'] if machine else None,
                'name': user['name'] if user else None,
                'phoneNumber': user['phoneNumber'] if user else None,
                'jobPosition': user['jobPosition'] if user else None,
                'datetimeStart': datetime_start.strftime('%Y-%m-%d %H:%M:%S'),
                'datetimeFinish': datetime_finish.strftime('%Y-%m-%d %H:%M:%S')
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
        users = api.get_all_users(token)

        machine_data = []
        for machine in machines:
            try:
                current_session = next((s for s in sessions if s['machineId'] == machine['id'] and s['state'] == 0), None)
                user = api.get_user(token, current_session['workerId']) if current_session else None

                machine_data.append({
                    'id': machine['id'],
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
        response = requests.post("http://91.236.197.212:8080/login", json={
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


@app.route('/pause_machine', methods=['POST'])
def pause_machine():
    data = request.get_json()
    machine_id = data.get('machine_id')
    token = get_token()
    if not token or not machine_id:
        return jsonify({'error': 'Invalid request'}), 400

    # Логика для паузы машины
    result = api.pause_machine(token, machine_id)



@app.route('/stop_machine', methods=['POST'])
def stop_machine():
    data = request.get_json()
    machine_id = data.get('machine_id')
    token = get_token()
    if not token or not machine_id:
        return jsonify({'error': 'Invalid request'}), 400

    result = api.lock_machine(token, machine_id)



@app.route('/machine/<machine_id>')
def machine_page(machine_id):
    token = get_token()
    if not token:
        return redirect(url_for('login'))

    machine_info = api.get_machine_and_sessions(token, machine_id)
    if machine_info is None:
        return "Ошибка получения данных о машине", 500

    return render_template('machine.html', machine=machine_info['machine'], status=machine_info['status'])

@app.route('/api/machine/<machine_id>')
def api_machine(machine_id):
    token = get_token()
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    machine_info = api.get_machine_and_sessions(token, machine_id)
    if machine_info is None:
        return jsonify({"error": "Error fetching machine data"}), 500

    return jsonify({
        "machine": machine_info['machine'],
        "status": machine_info['status']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

