#!/usr/bin/env python3.5

import time
import socket
import base64
import argparse
import sys
import csv
import ssdp
import re

encoding = 'utf-8'
mac      = '00-AB-11-11-11-11' # mac of remote
remote   = 'python remote'     # remote name
dst      = '10.0.1.10'         # ip of tv
app      = 'python'            # iphone..iapp.samsung
tv       = 'LE32C650'          # iphone.LE32C650.iapp.samsung
port     =  55000
key_off  = 'KEY_POWEROFF'

def scan_network_ssdp(verbose):
  try:
    tv_ips = []
    if (verbose):
      print("Scanning network...")
    tvs_found = ssdp.discover("urn:samsung.com:device:RemoteControlReceiver:1", timeout=1);
    for tv in tvs_found:
      ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', tv.location)
      tv_ips.append(ip.group(0))
      if (verbose):
        print("TV found in ip: " + ip.group(0))

  except KeyboardInterrupt:
    print (' was pressed. Search interrupted by user')

def push(ip, key, wait_time = 100.0):
  try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    src         = client_socket.getsockname()[0]
    byte_key    = bytes(key, encoding)
    encoded_key = base64.b64encode(byte_key).decode(encoding)
    
    msg =  chr(0x64)        + chr(0x00) +\
           chr(len(src))    + chr(0x00) + src +\
           chr(len(mac))    + chr(0x00) + mac +\
           chr(len(remote)) + chr(0x00) + remote 

    pkt =  chr(0x00) +\
           chr(len(app)) + chr(0x00) + app +\
           chr(len(msg)) + chr(0x00) + msg

    client_socket.send(bytes(pkt, encoding))

    msg =  chr(0x00) + chr(0x00) + chr(0x00) +\
           chr(len(encoded_key)) + chr(0x00) + encoded_key

    pkt =  chr(0x00) + chr(len(tv)) + chr(0x00) + tv + chr(len(msg)) +\
           chr(0x00) + msg

    client_socket.send(bytes(pkt, encoding))
    client_socket.close()
    time.sleep(wait_time / 1000.0)
    return True
  except socket.error:
    return False

def execute_macro(filename):
  try:
    with open(filename, newline='') as macro_file:
       reader = csv.DictReader(macro_file, ("key", "time"))
       for line in reader:
          if (line['key'].startswith('#')):
             continue
          push(dst, line['key'], float(line['time'] or 1000.0))
  except (FileNotFoundError, IOError):
    print('No such macro file: ' + filename) 

def main():
  parser = argparse.ArgumentParser(description='Controls your Samsumg SmartTV thru Wifi')
  parser.add_argument("-s", "--scan", help="scans the TV on the network", action="store_true")
  parser.add_argument("-k", "--key", help="the key to be sent to TV")
  parser.add_argument("-p", "--poweroff", help="search all TV's in the network and turn them off", action="store_true")
  parser.add_argument("-i", "--ip", help="defines the ip of the TV that will receive the command")
  parser.add_argument("-a", "--auto", help="sends the command to the first TV available", action="store_true")
  parser.add_argument("-m", "--macro", help="the macro file with commands to be sent to TV")

  if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()

  if args.scan:
     scan_network_ssdp(True)

  if args.auto:
     scan_network(True, key_ping)

  if args.ip:
     global dst
     dst = args.ip

  if args.key:
     push(dst, args.key)

  if args.poweroff:
     scan_network(False, key_off)

  if args.macro:
     execute_macro(args.macro)

if __name__ == "__main__": main()
