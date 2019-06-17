#!/usr/bin/env python3
"""

Usage:
    apiExe.py [--new_IP=<IP> | --new_port=<port>]
    apiExe.py [-h | --help | --version]

Arguments:
    --new_IP=<IP>      IP address [default: 0.0.0.0]
    --new_port=<port>  Docking point [default: 5050]

Options:
    -h --help   Show this screen
    --version   Show version
"""

import lib.apiLib
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='storeapi 1.2')
    print(arguments)
    lib.apiLib.main(arguments['--new_IP'], arguments['--new_port'])