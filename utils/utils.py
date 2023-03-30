import json
import sys
sys.path.append('.')

def get_config():
    with open('./config/config.json') as config_file:
        return json.load(config_file)

def print_error(skk): 
    print("\033[91m {}\033[00m" .format(skk))
