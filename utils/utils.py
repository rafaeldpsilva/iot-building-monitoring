import json
import sys

import requests
import urllib3
import os
import logging
sys.path.append('.')

FILE_PATH = os.environ.get('CARAVELS_CONFIG_FILE')
if FILE_PATH is None:
    raise EnvironmentError("Caravels config file not setup!")


def get_config():
    with open(FILE_PATH) as config_file:
        return json.load(config_file)


def update_values_get(process_name, uri):
    response = None
    try:
        request = requests.get(uri)
        data_json = request.text
        response = json.loads(data_json)
    except requests.exceptions.HTTPError:
        logging.warning("HTTPError in " + process_name)
    except ConnectionRefusedError:
        logging.warning("ConnectionRefusedError in " + process_name)
    except urllib3.exceptions.NewConnectionError:
        logging.warning("NewConnectionError in " + process_name)
    except urllib3.exceptions.MaxRetryError:
        logging.warning("MaxRetryError in " + process_name)
    except requests.exceptions.ConnectionError:
        logging.warning("ConnectionError in " + process_name)
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
        logging.warning("HTTPError in " + iot_name)
    except ConnectionRefusedError:
        logging.warning("ConnectionRefusedError in " + iot_name)
    except urllib3.exceptions.NewConnectionError:
        logging.warning("NewConnectionError in " + iot_name)
    except urllib3.exceptions.MaxRetryError:
        logging.warning("MaxRetryError in " + iot_name)
    except requests.exceptions.ConnectionError:
        logging.warning("ConnectionError in " + iot_name)

    if response == None:
        return response
    return response
