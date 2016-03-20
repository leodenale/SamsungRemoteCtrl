#!/usr/bin/env python3.5

import time
import socket
import base64
import argparse
import ipaddress
import sys

encoding =  'utf-8'
mac      = b'00-AB-11-11-11-11' # mac of remote
remote   = b'python remote'     # remote name
dst      =  '10.0.1.10'         # ip of tv
app      =  'python'            # iphone..iapp.samsung
tv       =  'LE32C650'          # iphone.LE32C650.iapp.samsung
port     =  55000

def scan_network(silent, key):
  print("Scanning network...")
  my_mask = socket.gethostbyname(socket.getfqdn()) + '/24'
  interface = ipaddress.IPv4Interface(my_mask).network
  socket.setdefaulttimeout(0.1)
  # start looking in the first valid ip
  for addr in interface:
    ip = str(addr)
    if (push(ip, key)):
      if (not silent):
        print("TV found in ip: " + ip)

def push(ip, key):
  try:
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.connect((ip, port))

    src      = bytes(new.getsockname()[0], encoding)
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

    new.send(bytes(pkt, encoding))

    msg =  chr(0x00) + chr(0x00) + chr(0x00) +\
           chr(len(encoded_key)) + chr(0x00) + encoded_key

    pkt =  chr(0x00) + chr(len(tv)) + chr(0x00) + tv + chr(len(msg)) +\
           chr(0x00) + msg

    new.send(bytes(pkt, encoding))
    new.close()
    time.sleep(0.1)
    return True
  except socket.error:
    return False

def main():
  parser = argparse.ArgumentParser(description='Controls your Samsumg SmartTV thru Wifi')
  parser.add_argument("-s", "--scan", help="scans the TV on the network", action="store_true")
  parser.add_argument("-k", "--key", help="the key to be sent to TV")
  parser.add_argument("-p", "--poweroff", help="search all TV's in the network and turn them off", action="store_true")

  if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()

  if args.scan:
     scan_network(False, 'PING')
  if args.key:
     push(dst, args.key)
  if args.poweroff:
     scan_network(False, 'KEY_POWEROFF')

if __name__ == "__main__": main()
