import requests
import json


def get_all_users(token):
    url = "http://backend:8080/get_all_users"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def get_all_machines(token):
    url = "http://backend:8080/get_all_machines"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


# New method to get machines for each parking by it's id
def get_parking_machines(token, parking_name):
    url = "http://backend:8080/get_parking_machines?name={}".format(parking_name)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def get_all_sessions(token):
    url = "http://backend:8080/get_all_sessions"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def get_user(user_id, token):
    url = "http://backend:8080/get_user?user_id={}".format(user_id)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def get_machine(token, machine_id):
    url = "http://backend:8080/get_machine?machine_id={}".format(machine_id)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def stop_machine(token, machine_id):
    url = 'http://backend:8080/stop_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def unstop_machine(token, machine_id):
    url = 'http://backend:8080/unstop_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def unlock_machine(token, machine_id):
    url = 'http://backend:8080/unlock_machine'
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
    url = 'http://backend:8080/lock_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


# New methods for parking places
def get_all_parkings(token):
    url = "http://backend:8080/get_all_parkings"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def get_parking(token, parking_id):
    url = "http://backend:8080/get_parking?parking_id={}".format(parking_id)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    return json_response


def register_parking(token, name, mac_addr, capacity, state):
    url = 'http://backend:8080/register_parking'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'name': name,
        'mac_addr': mac_addr,
        'capacity': capacity,
        'state': state,
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def update_parking_state(token, parking_id, newState):
    url = 'http://backend:8080/update_parking_state'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'id': parking_id,
        'state': newState,
    }
    response = requests.request("PUT", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def update_parking_capacity(token, parking_id, newCapacity):
    url = 'http://backend:8080/update_parking_state'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'id': parking_id,
        'capacity': newCapacity,
    }
    response = requests.request("PUT", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()


def manualy_add_machine(token, parking_id, machine_id):
    url = 'http://backend:8080/add_machine'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'machine_id': machine_id,
        'parking_id': parking_id,
    }
    response = requests.request("PUT", url, headers=headers, data=json.dumps(payload))
    print(response.text)
    return response.json()