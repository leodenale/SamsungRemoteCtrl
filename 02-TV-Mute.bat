:: search all TV's in the network and turn them off
python samsung_remote.py -k KEY_MUTE
pause
:: 
:: 
:: https://github.com/leodenale/SamsungRemoteCtrl
:: Usage: samsung_remote.py [-h] [-a | -i ip] [-k key] [-l] [-m <file>] [-p] [-q] [-s]
:: 
:: optional arguments:
:: -h, --help	show this help message and exit
:: -a	sends the command to the first TV available
:: -i ip	defines the ip of the TV that will receive the command
:: -k key	the key to be sent to TV
:: -l	use legacy method instead of default mode (websocket)
:: -m <file>	the macro file with commands to be sent to TV
:: -p	search all TV's in the network and turn them off
:: -q	do not print messages to console
:: -s	scans the network and print all the TV's found
:: 
:: https://github.com/Ape/samsungctl
:: Key codes
:: The list of accepted keys may vary depending on the TV model, but the following list has some common key codes and their descriptions.
:: 
:: Key code	Description
:: KEY_POWEROFF	Power off
:: KEY_UP	Up
:: KEY_DOWN	Down
:: KEY_LEFT	Left
:: KEY_RIGHT	Right
:: KEY_CHUP	P Up
:: KEY_CHDOWN	P Down
:: KEY_ENTER	Enter
:: KEY_RETURN	Return
:: KEY_CH_LIST	Channel List
:: KEY_MENU	Menu
:: KEY_SOURCE	Source
:: KEY_GUIDE	Guide
:: KEY_TOOLS	Tools
:: KEY_INFO	Info
:: KEY_RED	A / Red
:: KEY_GREEN	B / Green
:: KEY_YELLOW	C / Yellow
:: KEY_BLUE	D / Blue
:: KEY_PANNEL_CHDOWN	3D
:: KEY_VOLUP	Volume Up
:: KEY_VOLDOWN	Volume Down
:: KEY_MUTE	Mute
:: KEY_0	0
:: KEY_1	1
:: KEY_2	2
:: KEY_3	3
:: KEY_4	4
:: KEY_5	5
:: KEY_6	6
:: KEY_7	7
:: KEY_8	8
:: KEY_9	9
:: KEY_DTV	TV Source
:: KEY_HDMI	HDMI Source
:: KEY_CONTENTS	SmartHub
:: Please note that some codes are different on the 2016+ TVs. For example, KEY_POWEROFF is KEY_POWER on the newer TVs.