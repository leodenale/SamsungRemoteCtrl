==============
samsung_remote
==============

A Samsung TV Remote Control Python Script

Description
===========

samsung_remote is a script writen in Python that can remotely control your Samsung Smart TV thru wifi. It uses the great `samsungctl <https://github.com/Ape/samsungctl>`_ project to send the commands to TV and supports some nice features, such as:

- scan the network to find all available TV's;
- turn off all the TV's with one command;
- specify which TV to send commands;
- save common routines in a macro file to be executed latter. (video of a macro being executed: https://youtu.be/UXxBB7BOMDM)

Usage
=====

usage: samsung_remote.py [-h] [-a | -i ip] [-k key] [-l] [-m <file>] [-p] [-q]
                         [-s]

optional arguments:
  -h, --help  show this help message and exit
  -a          sends the command to the first TV available
  -i ip       defines the ip of the TV that will receive the command
  -k key      the key to be sent to TV
  -l          use legacy method instead of default mode (websocket)
  -m <file>   the macro file with commands to be sent to TV
  -p          search all TV's in the network and turn them off
  -q          do not print messages to console
  -s          scans the network and print all the TV's found

Dependecies
===========

- Python 3
- `samsungctl <https://github.com/Ape/samsungctl>`_ 
- `websocket-client`

you can install the dependencies running:

# pip3 install -r requirements.txt 

References
==========

- SSDP discovery https://gist.github.com/dankrause/6000248 and http://forum.micasaverde.com/index.php?topic=7878.15
- Regular expression to get the XML namespace https://stackoverflow.com/a/12946675/2383657 
- Correctly parse XML with namespaces https://codereview.stackexchange.com/a/51132
