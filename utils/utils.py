import json
import sys
from colorama import init, Fore

sys.path.append('.')
init(autoreset=True)

def get_config():
    with open('./config/config.json') as config_file:
        return json.load(config_file)

def print_error(error):
    print(Fore.RED + error)
    
