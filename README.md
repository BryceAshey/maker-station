# HuePi
Integrating Hue, a Pi, and some pushbutton switches

## Setup

### Setup python and i2c on the pi
		sudo apt-get update
		
		sudo apt-get install python3 python3-pip git
		
		sudo pip3 install smbus2
		
		sudo apt-get install -y i2c-tools

### Setup hue
Install the phue lib

		sudo pip3 install phue

Set an environ var of HUE_BRIDGE_IP to the IP of your hue bridge
Set an environ var of HUE_BRIDGE_USERNAME to an authorized username from your Hue. 
To get a username from your hue: https://www.sitebase.be/generate-phillips-hue-api-token/

### Setup megaio
This will setup megaio from the command line and for use by python

		~$ git clone https://github.com/SequentMicrosystems/megaio-rpi.git
		
		~$ cd megaio-rpi/
		
		~/megaio-rpi$ sudo make install