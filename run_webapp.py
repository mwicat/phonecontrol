import json
import pickle
import plac
import threading
import time

from collections import defaultdict

import requests.defaults

requests.defaults.max_retries = 0

import phonerc.webfe as webfe

DEFAULT_PORT = 5000
DEFAULT_UPDATE_SECS = 300


@plac.annotations(
   groups_file=('Groups file', 'option', 'g', str),
   custom_groups_file=('Custom groups file', 'option', 'c', str),
   port=('Port', 'option', 'p', int)
   )
def run(groups_file=None, custom_groups_file=None, port=DEFAULT_PORT):
    webfe.app.run(host='', port=port, debug=True, threaded=True)

def main():
    plac.call(run)


if __name__ == '__main__':
    main()

        
