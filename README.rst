==============
samsung_remote
==============

A Samsung TV Remote Control Python Script

Description
===========

samsung_remote is a script writen in Python that can remotely control your Samsung Smart TV thru wifi. It supports some nice features, such as:

- scan the network to find all available TV's;
- turn off all the found TV's with one command;
- specify which TV's to send commands;
- save common routines in a macro file to be executed latter. (video of a macro being executed: https://youtu.be/UXxBB7BOMDM)

Usage
=====

usage: samsung_remote.py [-h] [-s] [-k KEY] [-p] [-m MACRO] [-l] [-q]
                         [-i IP | -a]

optional arguments:
  -h, --help            show this help message and exit
  -s, --scan            scans the TV on the network
  -k KEY, --key KEY     the key to be sent to TV
  -p, --poweroff        search all TV's in the network and turn them off
  -m MACRO, --macro MACRO
                        the macro file with commands to be sent to TV
  -l, --legacy          use legacy method instead of default mode (websocket)
  -q, --quiet           do not print messages to console
  -i IP, --ip IP        defines the ip of the TV that will receive the command
  -a, --auto            sends the command to the first TV available

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
- https://gist.github.com/danielfaust/998441
- Regular expression to get the XML namespace https://stackoverflow.com/a/12946675/2383657 
- Correctly parse XML with namespaces https://codereview.stackexchange.com/a/51132
