import requests
import json


def get_all_users(token):
    url = "http://backend:8080/get_all_users"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    print(response)
    json_response = response.json()
    print(token)
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
    json_response = response.json()
    return json_response

def get_machine(token, machine_id):
    url = "http://backend:8080/get_machine?machine_id={}".format(machine_id)
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    json_response = response.json()
    return json_response


def pause_machine(token, machine_id):
    url = 'http://backend:8080/pause_machine'
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







#print(get_all_sessions('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMwMTczMDAsImlkIjoyLCJqb2JfcG9zaXRpb24iOiJhZG1pbiIsInBob25lX251bWJlciI6Ijg5MDkwMDAxMTIyIn0.WJm_v57V8YcjFjRv1SbgN8ZkA1UOKhkTDbCr5sgVlbU'))
#print(lock_machine('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM3MTY0MzksImlkIjoxLCJqb2JfcG9zaXRpb24iOiJhZG1pbiIsInBob25lX251bWJlciI6Ijg5MDkwMDAxMTIyIn0.ldrkA2JlDcNniq79IEaiDc70Drqlqxiiij9zE9L4L2U', 'Second Machine'))
#print(unlock_machine('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQxNzQwMTgsImlkIjoxLCJqb2JfcG9zaXRpb24iOiJhZG1pbiIsInBob25lX251bWJlciI6Ijg5MDkwMDAxMTIyIn0.UsROgZOc3lQYpTetH53cwCBubQpS-9pBzTke366moKM', "NEWM123"))
#print(get_machine('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQyMDY3OTAsImlkIjoxLCJqb2JfcG9zaXRpb24iOiJhZG1pbiIsInBob25lX251bWJlciI6Ijg5MDkwMDAxMTIyIn0.c27LBDcQxomwYBCN-fNTumDCAoY5NIKuinia6pNituE', 'NEWM123'))