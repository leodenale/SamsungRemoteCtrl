import logging
import csv
from helpers import tvcon

def execute(config, filename):
    try:
        with open(filename, newline='') as macro_file:
            reader = csv.DictReader(macro_file, ('key', 'wait'))

            for line in reader:
                key = line['key']
                if key.startswith('#'):
                    # is a comment, ignore it
                    continue
                wait = float(line['wait'] or 500.0)
                tvcon.send(config, key, wait)

    except (FileNotFoundError, IOError):
        logging.error('No such macro file: ' + filename)
