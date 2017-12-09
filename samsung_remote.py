#!/usr/bin/env python3

import argparse
import sys
import ssdp
import logging
import tvinfo
import tvcon
import macro

def loadLog(quiet):
    logging.basicConfig(filename='app.log',
                        format='%(asctime)s [%(levelname)6s]: %(message)s',
                        level=logging.DEBUG)
    if not quiet:
        root = logging.getLogger()
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)


def main():
    parser = argparse.ArgumentParser(
        description='Controls your Samsumg SmartTV thru Wifi')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true',
                       help='sends the command to the first TV available')
    group.add_argument(
        '-i',
        metavar='ip',
        help='defines the ip of the TV that will receive the command')

    parser.add_argument('-k', metavar='key', help='the key to be sent to TV')
    parser.add_argument(
        '-l',
        action='store_true',
        help='use legacy method instead of default mode (websocket)')
    parser.add_argument(
        '-m',
        metavar='<file>',
        help='the macro file with commands to be sent to TV')
    parser.add_argument(
        '-p',
        action='store_true',
        help="search all TV's in the network and turn them off")
    parser.add_argument(
        '-q',
        action='store_true',
        help='do not print messages to console')
    parser.add_argument(
        '-s',
        action='store_true',
        help="scans the network and print all the TV's found")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    loadLog(args.q)
    logging.debug('Program started with: %s', sys.argv)

    if args.s:
        logging.info('Scanning network...')
        tvs = ssdp.scan_network(True, wait=1)
        if not tvs:
            # try again, with a higher timeout
            tvs = ssdp.scan_network(True, wait=2)
        if not tvs:
            logging.info("No Samsung TV's found in the network")
        sys.exit(0)

    config = {
        'name': 'python remote',
        'ip': '10.0.1.2',
        'mac': '00-AB-11-11-11-11',
        'description': 'samsungctl',
        'id': 'PC',
        'host': '',
        'port': 55000,
        'method': 'websocket',
        'timeout': 0,
    }

    if args.i:
        config['host'] = args.i
    else:
        # no need to scan network if ip is passed as parameter
        tvs = ssdp.scan_network(False)
        if not tvs:
            # try again, with a higher timeout
            logging.error(
                'No Samsung TV found in the first run, trying again...')
            tvs = ssdp.scan_network(False, wait=1)
            if not tvs:
                logging.error('No Samsung TV found in the network.')
                sys.exit(0)

    if args.a:
        config['host'] = tvs[0]['ip']
        config['method'] = tvinfo.getMethod(tvs[0]['model'])
        logging.info('Sending command to first TV found: ' + tvs[0]['fn'])

    if args.l:
        config['method'] = 'legacy'

    if args.k:
        tvcon.send(config, args.k)

    if args.p:
        for tv in tvs:
            config['host'] = tv['ip']
            config['method'] = tvinfo.getMethod(tv['model'])
            if tvcon.send(config, 'KEY_POWEROFF'):
                logging.info('Turning off ' + tv['fn'] + ' succeed')
            else:
                logging.error('Turning off ' + tv['fn'] + ' failed')

    if args.m:
        macro.execute(config, args.m)

if __name__ == "__main__":
    main()
