import requests
import argparse
from getpass import getpass
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('--matrix-host', required=True)
parser.add_argument('--user-name')
parser.add_argument('--password')
parser.add_argument('--message-text-file', required=True)
parser.add_argument('--message-id', required=True)

args = parser.parse_args()

matrix_host = args.matrix_host
user_name = args.user_name
password = args.password
message_text_file = args.message_text_file
message_id = args.message_id

def main():
    token = read_token()    
    if token is None:
        token = get_token()
        save_token(token)
    user_names = get_user_name_list(token)
    with open(message_text_file, 'r') as file:
        message_text = file.read()
    for recipient in user_names:
        response = send_message(recipient, message_text, f'{recipient}{message_id}', token)
        if response.status_code != 200:
            print("could not send server notice to " + recipient)
            print(response.json())
            exit(1)
        print(f'message sent to {recipient}')
        sleep(0.5)


def read_token():
    try:    
        with open(".token", "r") as file:
            return file.readline()
    except IOError:
        return None

def get_token():
    global user_name, password
    if user_name is None:   
        user_name = input("enter admin user name: ")
    if password is None:
        password = getpass("enter user password: ")
    return authenticate(user_name, password)

def save_token(token):
    with open(".token", "w") as file:
        file.write(token)


def authenticate(user, password):
    request_body = {
      "type": "m.login.password",
      "identifier": {
            "type": "m.id.user",
            "user": user
        },
      "password": password
    }
    response = requests.post(f'{matrix_host}/_matrix/client/r0/login', json=request_body)
    if response.status_code != 200:
        print(request.json())
        exit(1)
    return response.json()['access_token']

def get_user_name_list(token):
    response = requests.get(f'{matrix_host}/_synapse/admin/v2/users', headers=auth_header(token))
    return [user["name"] for user in response.json()["users"]]

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def send_message(recipient, message, id, token):
    request_body = {
        "user_id": recipient,
        "content": {
            "msgtype": "m.text",
            "body": message
            }
    }
    return requests.put(f'{matrix_host}/_synapse/admin/v1/send_server_notice/{id}',
                        json=request_body,
                        headers=auth_header(token))
        
if __name__ == '__main__':
    main()
