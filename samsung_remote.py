#!/usr/bin/env python3.5

import time
import socket
import base64
import argparse
import ipaddress
import sys
import csv

encoding =  'utf-8'
mac      = b'00-AB-11-11-11-11' # mac of remote
remote   = b'python remote'     # remote name
dst      =  '10.0.1.10'         # ip of tv
app      =  'python'            # iphone..iapp.samsung
tv       =  'LE32C650'          # iphone.LE32C650.iapp.samsung
port     =  55000

# got this code from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/28950776#28950776
# just need to change port 0 to 1 for some reason to work on Mac OS X
def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip 

def scan_network(silent, key):
  try:
    if (not silent):
      print("Scanning network...")

    my_mask = get_my_ip() + '/24'
    interface = ipaddress.IPv4Interface(my_mask).network
    socket.setdefaulttimeout(0.1)

    # start looking in the first valid ip
    for addr in interface:
      ip = str(addr)
      if (push(ip, key)):
        if (silent):
          break
        else:
          print("TV found in ip: " + ip)

  except KeyboardInterrupt:
    print (' was pressed. Search interrupted by user')

def push(ip, key, wait_time = 100.0):
  try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    src      = bytes(client_socket.getsockname()[0], encoding)
    byte_key = bytes(key, encoding)

    encoded_key    = base64.b64encode(byte_key).decode(encoding)
    encoded_src    = base64.b64encode(src).decode(encoding)
    encoded_mac    = base64.b64encode(mac).decode(encoding)
    encoded_remote = base64.b64encode(remote).decode(encoding)
    
    msg =  chr(0x64) + chr(0x00)    +\
           chr(len(encoded_src))    + chr(0x00) + encoded_src +\
           chr(len(encoded_mac))    + chr(0x00) + encoded_mac +\
           chr(len(encoded_remote)) + chr(0x00) + encoded_remote 

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
     scan_network(False, 'PING')
  if args.ip:
     global dst
     dst = args.ip
  if args.key:
     if args.auto:
       scan_network(True, args.key)
     else:
       push(dst, args.key)
  if args.poweroff:
     scan_network(False, 'KEY_POWEROFF')
  if args.macro:
     execute_macro(args.macro)

if __name__ == "__main__": main()
