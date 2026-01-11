import os
import json
import requests
import threading
import logging
import traceback
from src.clients.mqtt_client import MqttClient as mqttclient
from datetime import datetime

# Define console colors for readability
class ConsoleColor:    
    OKBLUE = "\033[34m"
    OKCYAN = "\033[36m"
    OKGREEN = "\033[32m"        
    MAGENTA = "\033[35m"
    WARNING = "\033[33m"
    FAIL = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"    

# Configure logging
logging.basicConfig(filename="solar_script.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Get current date & time
VarCurrentDate = datetime.now()

# Load settings from JSON file
try:
    with open('/data/options.json') as options_file:
        json_settings = json.load(options_file)
except Exception as e:
    logging.error(f"Failed to load settings: {e}")
    print(ConsoleColor.FAIL + "Error loading settings.json. Ensure the file exists and is valid JSON." + ConsoleColor.ENDC)
    exit()

# Retrieve inverter serials
inverterserials = str(json_settings['sunsynk_serial']).split(";")

# Function to safely fetch data using threading


#Start the Loop
print("------------------------------------------------------------------------------")
print("-- " + ConsoleColor.MAGENTA + f"Running Script SolarSynkMqqttoHAPublishing" + ConsoleColor.ENDC)
print("-- https://github.com/gdwaterworth/sunsynkmqqt_to_ha_publish")
print("------------------------------------------------------------------------------")   
# Connect MQTT
client = mqttclient.connect_mqtt()

# Standard Layouts
# Sensor 
def_layout_sensor = {
    "state_class": "measurement",
    "device_class": "power",
    "unit_of_measurement": "W",
    "state_topic": "",
    "json_attributes_topic": ""
}  

for serialitem in inverterserials:
    print(ConsoleColor.OKCYAN + f"Getting {serialitem} @ {VarCurrentDate}" + ConsoleColor.ENDC)
    print("Script refresh rate set to: " + ConsoleColor.OKCYAN + str(json_settings['Refresh_rate']) + ConsoleColor.ENDC + " milliseconds")
    mqttclient.publish(client,"sunsynk/"+serialitem+"/inverterinfo",getapi.GetInverterInfo(BearerToken,serialitem))
    mqttclient.publish(client,"sunsynk/"+serialitem+"/pv",getapi.GetPvData(BearerToken,serialitem))
    mqttclient.publish(client,"sunsynk/"+serialitem+"/grid",getapi.GetGridData(BearerToken,serialitem))
    mqttclient.publish(client,"sunsynk/"+serialitem+"/battery",getapi.GetBatteryData(BearerToken,serialitem))
    mqttclient.publish(client,"sunsynk/"+serialitem+"/load",getapi.GetLoadData(BearerToken,serialitem))
    mqttclient.publish(client,"sunsynk/"+serialitem+"/output",getapi.GetOutputData(BearerToken,serialitem))
    mqttclient.publish(client,"sunsynk/"+serialitem+"/settings",getapi.GetInverterSettingsData(BearerToken,serialitem))

    print(ConsoleColor.OKGREEN + "All API calls completed successfully!" + ConsoleColor.ENDC)

    # Script completion time
    VarCurrentDate = datetime.now()
    print(f"Script completion time: {ConsoleColor.OKBLUE} {VarCurrentDate} {ConsoleColor.ENDC}") 

mqttclient.disconnect(client)

print(ConsoleColor.OKBLUE + "Script execution completed." + ConsoleColor.ENDC)
