from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback, PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
import pubnub


import datetime
from time import sleep
from Phidgets.Devices.InterfaceKit import InterfaceKit

from sense_hat import SenseHat


sense = SenseHat()

interfaceKit = InterfaceKit()
interfaceKit.openPhidget(327060)

pnconf = PNConfiguration()  
sleep(2)


pnconf.publish_key = 'pub-c-23235607-897e-4e8c-8b96-409d2a0ce710'       # set pubnub publish_key
pnconf.subscribe_key = 'sub-c-7b8840c4-f940-11e8-ba8a-aef4d14eb57e'     # set pubnub subscibe_key
 
pubnub = PubNub(pnconf)                     # create pubnub_object using pubnub_configuration_object

def my_publish_callback(envelope, status):
	if not status.is_error():
    	pass
	else:
		pass

channel='senseHat'                         # provide pubnub channel_name


data = {                                    # sample data to be published
    'Temperature': '16',
    'Humidity' : '88'
}

class MyListener(SubscribeCallback):        # Not need for working of this program
	def status(self, pubnub, status):
		if status.category == PNStatusCategory.PNConnectedCategory:
			pubnub.publish().channel(channel).message({'fieldA': 'awesome', 'fieldB': 10}).sync()
 
	def message(self, pubnub, message):
		print(message)
 
	def presence(self, pubnub, presence):
		pass

my_listener = SubscribeListener()                   # create listner_object to read the msg from the Broker/Server
pubnub.add_listener(my_listener)                    # add listner_object to pubnub_object to subscribe it
pubnub.subscribe().channels(channel).execute()      # subscribe the channel (Runs in background)


my_listener.wait_for_connect()                      # wait for the listner_obj to connect to the Broker.Channel 
print('connected')                                  # print confirmation msg


while(1):
	
	humidity = round((sense.get_humidity()*64)/100,1)
	temperature = round(sense.get_temperature(),1)
	pressure = round(sense.get_pressure(),1)

	
	pubnub.publish().channel(channel).message(
        	{"eon":{
            	'temperature': temperature,
            	'humidity': humidity,
            	'pressure': pressure
		}}
    	).async(my_publish_callback)
	
	

	print
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print("Ambient Temperature: " + str(temperature) + " degrees Celcius")
	print("Relative Humidity: " + str(humidity) + "%")
	print("Pressure: " + str(pressure) + " bars")

	sleep(5)


while True:                                                 # Infinite loop
	result = my_listener.wait_for_message_on(channel)       # Read the new msg on the channel
	print(result.message)                                   # print the new msg


# Close the interfaces
interfaceKit.closePhidget()
