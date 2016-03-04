import time
import socket
import base64
import argparse

encoding = 'utf-8'
src      = b'10.0.1.3'          # ip of remote
mac      = b'00-AB-11-11-11-11' # mac of remote
remote   = b'python remote'     # remote name
dst      = '10.0.1.13'           # ip of tv
app      = 'python'             # iphone..iapp.samsung
tv       = 'LE32C650'           # iphone.LE32C650.iapp.samsung
port     = 55000

def scan_network():
    print("Scanning network...")

def push(key):
  try:
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.connect((dst, port))

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
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--scan", help="scans the TV on yhe network", action="store_true")
  parser.add_argument("-k", "--key", help="the key to be sent to TV", default="KEY_VOLDOWN")
  args = parser.parse_args()

  if args.scan:
     scan_network()
  else:
     push(args.key)

if __name__ == "__main__": main()
