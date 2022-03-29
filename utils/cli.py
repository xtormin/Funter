import sys
import argparse

parser = argparse.ArgumentParser(add_help = True, description = '%(prog)s hunts all forms and inputs found in a list of urls.')

parser.add_argument('-U','--urlslist', 
                    help = 'File with the list of urls', 
                    nargs = '+')
parser.add_argument('-o','--outputfile', 
                    help = 'Output file')
parser.add_argument('-s','--showweb', 
                    help = 'Launch a website to visualize obtained data', action= "store_true")
parser.add_argument('-r','--resetdata', 
                    help = 'Reset database to defaults', action= "store_true")                              

def get():
    return parser.parse_args()

def help():
    return parser.print_help(sys.stderr)