import confuse
from termcolor import colored

# LOAD CONFIG FROM YAML FILE
config = confuse.Configuration('XNP', __name__)
config.set_file('config/config.yaml')

APPVER = config['app']['version'].get()

def main():
    BANNER = f"""                 
    ____ _  _ _  _ ___ ____ ____ 
    |___ |  | |\ |  |  |___ |__/ 
    |    |__| | \|  |  |___ |  \ 

    Github: https://github.com/xtormin/Funter
    Version: {APPVER}
    By: @xtormin

    HAPPY HUNTING! 8)
    """

    print(colored(BANNER, 'red', attrs=['bold']))