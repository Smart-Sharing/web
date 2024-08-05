import requests
import json


def get_all_users(token):
    url = "http://host.docker.internal:8080/get_all_users"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    print(token)
    return json_response


def get_all_machines(token):
    url = "http://host.docker.internal:8080/get_all_machines"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response

def get_all_sessions(token):
    url = "http://host.docker.internal:8080/get_all_sessions"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response

def get_user(user_id, token):
    url = "http://host.docker.internal:8080/get_user?user_id={}".format(user_id)
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    json_response = response.json()
    return json_response

def get_machine(token, machine_id):
    url = "http://host.docker.internal:8080/get_machine?machine_id={}".format(machine_id)
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    json_response = response.json()
    return json_response


def pause_machine(token, machine_id):
    url = 'http://host.docker.internal:8080/pause_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response = requests.post(url, headers=headers)
    return response.json()

def unlock_machine(token, machine_id):
    url = 'http://host.docker.internal:8080/unlock_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()

def lock_machine(token, machine_id):
    url = 'http://host.docker.internal:8080/lock_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def start_machine(token, machine_id):
    url = 'http://host.docker.internal:8080/unlock_machine'
    headers = {
        'machine_id': machine_id,
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.json()


def get_machine_and_sessions(token, machine_id):
    try:

        machine_url = f"http://host.docker.internal:8080/get_machine?machine_id={machine_id}"
        headers = {'Authorization': f'Bearer {token}'}
        machine_response = requests.get(machine_url, headers=headers)
        machine_data = machine_response.json()


        sessions_url = "http://host.docker.internal:8080/get_all_sessions"
        sessions_response = requests.get(sessions_url, headers=headers)
        sessions_data = sessions_response.json()


        active_session = any(session['machineId'] == machine_id and session['state'] == 0 for session in sessions_data)

        machine_status = 'Свободна'
        if active_session:
            machine_status = 'Используется'
        else:

            pass


        return {
            'machine': machine_data,
            'status': machine_status
        }

    except Exception as e:
        print(f'Error fetching machine and session data: {e}')
        return None


print(get_all_sessions('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMwMTczMDAsImlkIjoyLCJqb2JfcG9zaXRpb24iOiJhZG1pbiIsInBob25lX251bWJlciI6Ijg5MDkwMDAxMTIyIn0.WJm_v57V8YcjFjRv1SbgN8ZkA1UOKhkTDbCr5sgVlbU'))
