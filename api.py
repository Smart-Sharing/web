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
