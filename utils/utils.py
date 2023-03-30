import json
import sys
from colorama import Fore
sys.path.append('.')

def get_config():
    with open('./config/config.json') as config_file:
        return json.load(config_file)

def print_error(error): 
    print('\033[93m' + error + '\033[0m')
