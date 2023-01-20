#main.py
import os
import argparse
print(os.path.dirname(os.path.abspath(__file__)))

from album import Album

parser = argparse.ArgumentParser(description='Find duplicate jpg/jpeg files in a directory and its subdirectories')
parser.add_argument('dir', nargs="?", type=str)


if __name__ == '__main__':
    
    dir = parser.parse_args().dir if parser.parse_args().dir else os.path.dirname(os.path.abspath(__file__)) + "\\Photos"
    
    if os.path.exists(dir):
        Album(dir)
    else:
        raise os.error("Invalid path given.")
        