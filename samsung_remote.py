import time
import socket
import base64
from errno import ECONNREFUSED

src     = '10.0.1.3' 	      # ip of remote
mac     = '00-AB-11-11-11-11' # mac of remote
remote  = 'python remote'     # remote name
dst     = '10.0.1.9'   	      # ip of tv
app     = 'python'            # iphone..iapp.samsung
tv      = 'LE32C650'          # iphone.LE32C650.iapp.samsung

def push(key):
  try:
  	new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  	new.connect((dst, 55000))
  	msg = 	chr(0x64) + chr(0x00) +\
        	chr(len(base64.b64encode(src)))    + chr(0x00) + base64.b64encode(src) +\
        	chr(len(base64.b64encode(mac)))    + chr(0x00) + base64.b64encode(mac) +\
        	chr(len(base64.b64encode(remote))) + chr(0x00) + base64.b64encode(remote)
  	pkt = 	chr(0x00) +\
        	chr(len(app)) + chr(0x00) + app +\
        	chr(len(msg)) + chr(0x00) + msg
  	new.send(pkt)
  	msg = 	chr(0x00) + chr(0x00) + chr(0x00) +\
        	chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
  	pkt = 	chr(0x00) +\
        	chr(len(tv))  + chr(0x00) + tv +\
        	chr(len(msg)) + chr(0x00) + msg
  	new.send(pkt)
  	new.close()
  	time.sleep(0.1)
	return True
  except socket.error as err:
        if err.errno == ECONNREFUSED:
            return False
def main():
  if push("PING"):
  	print "pingo que eh uma blza"
	push("KEY_VOLDOWN")
  else:
  	print "ti fode trouxa"

if __name__ == "__main__": main()
