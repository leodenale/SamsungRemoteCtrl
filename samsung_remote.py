#!/usr/bin/env python3

import time
import socket
import argparse
import sys
import csv
import ssdp
import re
import samsungctl
import urllib.request
import xml.etree.ElementTree as ET
import logging
import websocket


def getMethod(model):
    # model dict... this should be updated to all samsung models
    models = {'F': 'legacy'}
    method = models.get(model[4], 'websocket')
    logging.debug('Model: ' + model[4] + ' returns method: ' + method)
    return method


def namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''


def getTVinfo(url):
    ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    xmlinfo = urllib.request.urlopen(url)
    xmlstr = xmlinfo.read().decode('utf-8')
    root = ET.fromstring(xmlstr)
    ns = namespace(root)
    fn = root.find('.//{}friendlyName'.format(ns)).text
    model = root.find('.//{}modelName'.format(ns)).text
    return {'fn': fn, 'ip': ip.group(0), 'model': model}


def push(config, key, wait_time=100.0):
    try:
        with samsungctl.Remote(config) as remote:
            remote.control(key)

        time.sleep(wait_time / 1000.0)
        return True

    except socket.error:
        return False
    except websocket._exceptions.WebSocketConnectionClosedException:
        logging.error("Websocket error! Maybe try sending with legacy (-l)?")
        return False


def scan_network_ssdp(verbose, wait=0.3):
    try:
        tv_list = []
        tvs_found = ssdp.discover(
            "urn:samsung.com:device:RemoteControlReceiver:1",
            timeout=wait)
        for tv in tvs_found:
            info = getTVinfo(tv.location)
            tv_list.append(info)
            if verbose:
                logging.info(
                    info['fn'] +
                    " model " +
                    info['model'] +
                    " found in ip " +
                    info['ip'])
            else:
                logging.debug(
                    info['fn'] +
                    " model " +
                    info['model'] +
                    " found in ip " +
                    info['ip'])
        return tv_list

    except KeyboardInterrupt:
        logging.info(' was pressed. Search interrupted by user')


def execute_macro(config, filename):
    try:
        with open(filename, newline='') as macro_file:
            reader = csv.DictReader(macro_file, ("key", "time"))

            with samsungctl.Remote(config) as remote:
                for line in reader:
                    key = line['key']
                    if (key.startswith('#')):
                        continue
                    remote.control(key)
                    time.sleep(float(line['time'] or 500.0) / 1000.0)

    except (FileNotFoundError, IOError):
        logging.error('No such macro file: ' + filename)


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
    parser.add_argument("-s", "--scan", action="store_true",
                        help="scans the TV on the network")
    parser.add_argument("-k", "--key",
                        help="the key to be sent to TV")
    parser.add_argument(
        "-p",
        "--poweroff",
        action="store_true",
        help="search all TV's in the network and turn them off")
    parser.add_argument("-m", "--macro",
                        help="the macro file with commands to be sent to TV")
    parser.add_argument(
        "-l",
        "--legacy",
        action="store_true",
        help="use legacy method instead of default mode (websocket)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="do not print messages to console")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--ip",
        help="defines the ip of the TV that will receive the command")
    group.add_argument("-a", "--auto", action="store_true",
                       help="sends the command to the first TV available")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    loadLog(args.quiet)
    logging.debug('Program started with: %s', sys.argv)

    if args.scan:
        logging.info("Scanning network...")
        tvs = scan_network_ssdp(True, wait=1)
        if not tvs:
            # try again, with a higher timeout
            tvs = scan_network_ssdp(True, wait=2)
        if not tvs:
            logging.info("No Samsung TV's found in the network")
        sys.exit(0)

    config = {
        "name": "python remote",
        "ip": "10.0.1.2",
        "mac": "00-AB-11-11-11-11",
        "description": "samsungctl",
        "id": "PC",
        "host": "",
        "port": 55000,
        "method": "websocket",
        "timeout": 0,
    }

    if args.ip:
        config['host'] = args.ip
    else:
        # no need to scan network if ip is passed as parameter
        tvs = scan_network_ssdp(False)
        if not tvs:
            # try again, with a higher timeout
            logging.error(
                "No Samsung TV found in the first run, trying again...")
            tvs = scan_network_ssdp(False, wait=1)
            if not tvs:
                logging.error("No Samsung TV found in the network.")
                sys.exit(0)

    if args.auto:
        config['host'] = tvs[0]['ip']
        config['method'] = getMethod(tvs[0]['model'])
        logging.info('Sending command to first TV found: ' + tvs[0]['fn'])

    if args.legacy:
        config['method'] = "legacy"

    if args.key:
        push(config, args.key)

    if args.poweroff:
        for tv in tvs:
            config['host'] = tv['ip']
            config['method'] = getMethod(tv['model'])
            if push(config, 'KEY_POWEROFF'):
                logging.info("Turning off " + tv['fn'] + " succeed")
            else:
                logging.error("Turning off " + tv['fn'] + " failed")

    if args.macro:
        execute_macro(config, args.macro)


if __name__ == "__main__":
    main()
