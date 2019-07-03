Lleidabeer(Index)
=================

This practice is structured in the following way:

- Folder called brewery:
	· File brewery.py
	· File __init__.py
- Folder called  notifications
	· File notifications.py
	· File __init__.py
- Main archive called lleidabeer.py
- File lleidabeer.yaml
- File dht11.py


In order to have an orderly structure, we create a folder called brewery and another called notifications with a file in each called __init__.py,in order to access the corresponding codes from different programs, we will only have to import it with the name of the folder.

How run the program:
=========================

To start turn on the Raspberrypi and connect the ESP, configure the network to the two machines for communication,configure the token, the user, the pins and the alarm values desired in the file Lleidabeer.yaml using the pattern lleidabeer-sample.yaml and from the terminal of the Raspberrypi we run the program lleidabeer.py. Once we have done this process it appears in the terminal a set of orders:

We decided to use just one input argument because is more easy to implement and easy to work, than two arguments, the commands to send via telegram will be:


To Sensors:

/temp: They send us the value of all temperature sensors.

/temp*ambient: They send us the value of the ambient temperature sensors.


To Raspberry relays:

/onheater*Heaterwort: Turns on just the heaterwort relay.

/onheater: Turns  on all the heaters relays. 

/offheater*heaterwort: Turns off just the heaterwort relay.

/offheater: Turns  of all the heaters relays.

/onmixer*mixerone: Turns on just the mixerone relay. 

/onmixer: Turns on all the mixers relays. 

/offmixer*mixerone: Turns off just the mixerone relay. 

/offmixer: Turns off  all the mixers relays.


To Esp8266 relays:


/onmqttheater:  Turns on the arduino heater sending an 1 to the ESP.

/offmqttheater: Turns off the arduino heater sending an 2 to the ESP.

/onmqttmixer: Turns on the arduino mixer sending an 3 to the ESP.

/offmqttmixer: Turns off the arduino mixer sending an 4 to the ESP.


Others commands:

/help: give some help



To work, in this code we will use 2 diferent topics:

- Topic sensors: This topic is used to send temperatures from the ESP to the Raspberry

- Topic relays: This topic will be used to send orders from the Raspberry to the ESP








Lleidabeer(Purpose of activity):
================================

The purpose of this practice is to know a set of current data in order to be able to make home-made beer,also you have control of some of the devices such as the valves, with the help of reels.

Lleidabeer(Programs to install):
================================

We will have the  DHT11.py(library) file, and install the Paho and Mosquitto for the correct working.

To install requeriments.txt we use this command:

$pip install -r requeriments.txt

- aiohttp==3.5.4
- async-timeout==3.0.1
- attrs==18.2.0
- awesome-slugify==1.6.5
- chardet==3.0.4
- idna==2.8
- multidict==4.5.2
- PyYAML==3.13
- regex==2019.3.12
- telepot==12.7
- Unidecode==0.4.21
- urllib3==1.24.1
- yar1==1.3.0


To install mosquitto:

$sudo apt update
$sudo apt upgrade
$sudo apt install mosquitto

	- To check the state:
	$sudo systemctl status mosquitto

	- To stop the server:
	$sudo systemctl stop mosquitto


	- To run the server:
	$sudo systemctl start mosquitto


To install Paho.Mqtt:

$sudo pip install paho-mqtt

Material necessary:
========

- A Raspberry
- An ESP8266(Arduino)
- A cable USB micro
- An HDMI cable if you do not want to work for ssh.
- Four relays
- Two temperature sensor dht11
- Protoboard and wire

