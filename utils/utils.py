import json
import sys
import requests
import urllib3
from colorama import init, Fore
sys.path.append('.')
init(autoreset=True)

def get_config():
    with open('./config/config.json') as config_file:
        return json.load(config_file)

def update_values_get(iot_name, uri):
    response = None
    try:
        request = requests.get(uri)
        data_json = request.text
        response = json.loads(data_json)
    except requests.exceptions.HTTPError:
        print_error("HTTPError in " + iot_name)
    except ConnectionRefusedError:
        print_error("ConnectionRefusedError in " + iot_name)
    except urllib3.exceptions.NewConnectionError:
        print_error("NewConnectionError in " + iot_name)
    except urllib3.exceptions.MaxRetryError:
        print_error("MaxRetryError in " + iot_name)
    except requests.exceptions.ConnectionError:
        print_error("ConnectionError in " + iot_name)
    if response == None:
        return response
    return response

def update_values_post(iot_name, uri):
    response = None
    try:
        request = requests.post(uri)
        data_json = request.text
        response = json.loads(data_json)
    except requests.exceptions.HTTPError:
        print_error("HTTPError in " + iot_name)
    except ConnectionRefusedError:
         print_error("ConnectionRefusedError in " + iot_name)
    except urllib3.exceptions.NewConnectionError:
         print_error("NewConnectionError in " + iot_name)
    except urllib3.exceptions.MaxRetryError:
         print_error("MaxRetryError in " + iot_name)
    except requests.exceptions.ConnectionError:
         print_error("ConnectionError in " + iot_name)

    if response == None:
        return response
    return response

def print_error(error):
    print('\n'+Fore.RED + error)

