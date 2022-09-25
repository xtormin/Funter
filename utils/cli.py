import sys
import argparse

parser = argparse.ArgumentParser(add_help = True, description = '%(prog)s hunts all forms and inputs found in a list of urls.')

parser.add_argument('-u','--url', 
                    help = 'Url to scrape', 
                    nargs = '+')
parser.add_argument('-U','--urlslist', 
                    help = 'File with the list of urls to scrape', 
                    nargs = '+')
parser.add_argument('-o','--outputfile', 
                    help = 'Output file to CSV')
parser.add_argument('-r','--resetdata', 
                    help = 'Reset database to defaults', action= "store_true")
parser.add_argument('-v','--verbose', 
                    help = 'Verbose', action= "store_true")                                  

def get():
    return parser.parse_args()

def help():
    return parser.print_help(sys.stderr)