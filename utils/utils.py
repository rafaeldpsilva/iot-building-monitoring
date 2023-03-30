import json
import sys
from colorama import init, Fore

sys.path.append('.')

def get_config():
    with open('./config/config.json') as config_file:
        return json.load(config_file)

def print_error(error):
    init(autoreset=True)
    print(Fore.RED + error)
    
