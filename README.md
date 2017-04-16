# samsung_remote.py
A Samsung TV Remote Control Python Script

## Description
samsung_remote is a script writen in python 3.5 that can remotely control your Samsung Smart TV thru wifi. It supports:

- scan the network for TV's;
- turn off all the TV's;
- specify which TV's to send commands;
- save common routines in a macro file to be executed latter.

Project forked from (https://gist.github.com/danielfaust/998441)

## Usage
./samsung_remote.py [-h] [-s] [-k KEY] [-p] [-i IP] [-a] [-m MACRO]

  -h, --help              show this help message and exit
  
  -s, --scan              scans the TV on the network
  
  -k KEY, --key KEY       the key to be sent to TV
  
  -p, --poweroff          search all TV's in the network and turn them off
  
  -i IP, --ip IP          defines the ip of the TV that will receive the command
  
  -a, --auto              sends the command to the first TV available
  
  -m MACRO, --macro MACRO the macro file with commands to be sent to TV

## Dependecies
samsung_remote.py needs python 3.5 to work. Tested on Linux and Mac OS X.
