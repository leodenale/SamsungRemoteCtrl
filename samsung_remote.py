import time
import socket
import base64

src      = b'10.0.1.3'          # ip of remote
mac      = b'00-AB-11-11-11-11' # mac of remote
remote   = b'python remote'     # remote name
dst      = '10.0.1.13'          # ip of tv
app      = 'python'             # iphone..iapp.samsung
tv       = 'LE32C650'           # iphone.LE32C650.iapp.samsung
encoding = 'utf-8'
port     = 55000

def push(key):
  try:
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.connect((dst, port))
    byte_key = bytes(key, encoding)

    msg =  chr(0x64) + chr(0x00) +\
           chr(len(base64.b64encode(src).decode(encoding))) +\
           chr(0x00) + base64.b64encode(src).decode(encoding) +\
           chr(len(base64.b64encode(mac).decode(encoding))) +\
           chr(0x00) + base64.b64encode(mac).decode(encoding) +\
           chr(len(base64.b64encode(remote).decode(encoding))) +\
           chr(0x00) + base64.b64encode(remote).decode(encoding)

    pkt =  chr(0x00) + chr(len(app)) + chr(0x00) + app + chr(len(msg)) +\
           chr(0x00) + msg

    new.send(bytes(pkt, encoding))

    msg =  chr(0x00) + chr(0x00) + chr(0x00) +\
           chr(len(base64.b64encode(byte_key).decode(encoding))) +\
           chr(0x00) + base64.b64encode(byte_key).decode(encoding)

    pkt =  chr(0x00) + chr(len(tv)) + chr(0x00) + tv + chr(len(msg)) +\
           chr(0x00) + msg

    new.send(bytes(pkt, encoding))
    new.close()
    time.sleep(0.1)
    return True
  except socket.error:
    return False

def main():
  if push('PING'):
    print ('pingo que eh uma blza')
    push('KEY_VOLDOWN')
  else:
    print ('ti fode trouxa')

if __name__ == "__main__": main()
