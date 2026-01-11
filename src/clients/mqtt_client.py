import random
import time
import json
from paho.mqtt import client as mqtt_client
from src.configuration.configuration import Configuration
# "MQTT_Server": "",
# "MQTT_Port": 0,
# "MQTT_Login": "",
# "MQTT_Pass": ""


# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'

class MqttClient:

    def connect_mqtt():
        FIRST_RECONNECT_DELAY = 1
        RECONNECT_RATE = 2
        MAX_RECONNECT_COUNT = 12
        MAX_RECONNECT_DELAY = 60
        def on_disconnect(client, userdata, rc):
            print(f"Disconnected with result code: `{rc}`")
            reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
            while reconnect_count < MAX_RECONNECT_COUNT:
                print(f"Reconnecting in `{reconnect_delay}` seconds...")
                time.sleep(reconnect_delay)
                try:
                    client.reconnect()
                    print(f"Reconnected successfully!")
                    return
                except Exception as err:
                    print(f"`{err}`. Reconnect failed. Retrying...")

                reconnect_delay *= RECONNECT_RATE
                reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
                reconnect_count += 1
            print(f"Reconnect failed after `{reconnect_delay}` attempts. Exiting...")
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        with open('/data/options.json') as options_file:
            json_settings = json.load(options_file)
        username = json_settings["MQTT_Login"]
        print(f"Login: `{username}`")
        password = json_settings["MQTT_Pass"]
        broker = json_settings["MQTT_Server"]
        print(f"Broker: `{broker}`")
        port = json_settings["MQTT_Port"]
        print(f"Port: `{port}`")
        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        client.on_disconnect = on_disconnect    
        return client
        
    def publish_tree(client,topic,msg):
            def step_through_json(data, parent_key=''):
                if isinstance(data, dict):
                    for key, value in data.items():
                        current_key_path = f"{parent_key}.{key}" if parent_key else key
                        step_through_json(value, current_key_path)
                elif isinstance(data, list):
                    for index, item in enumerate(data):
                        current_key_path = f"{parent_key}[{index}]"
                        step_through_json(item, current_key_path)
                else:
                    #print(f"Key Path: '{parent_key}', Value: '{data}', Type: {type(data).__name__}")
                    topicsend=topic+"/"+parent_key.replace(".","/")
                    topicsend=topicsend.replace("[","/")
                    topicsend=topicsend.replace("]","")
                    if data == None:
                        data = 0
                    result = client.publish(topicsend, data)
                    status = result[0]
                    if status == 0:
                        a = 0
                        #print(f"Sent `{data}` to topic `{topicsend}`")
                    else:
                        print(f"Failed to send message to `{topicsend}`")
            step_through_json(msg)

    def publish_single(client,topic,msg):
                    #print(f"Key Path: '{parent_key}', Value: '{data}', Type: {type(data).__name__}")
                    topicsend=topic.replace(".","/")
                    topicsend=topicsend.replace("[","/")
                    topicsend=topicsend.replace("]","")
                    if msg == None:
                        data = 0
                    else:
                        data = msg  
                    result = client.publish(topicsend, data)
                    status = result[0]
                    if status == 0:
                        a = 0
                        #print(f"Sent `{data}` to topic `{topicsend}`")
                    else:
                        print(f"Failed to send message to `{topicsend}`")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(f"Topic: {msg.topic}")
        print(f"Message: {msg.payload.decode()}")
        # You can add further processing logic here
        # e.g., storing data in a database, triggering an action


    def disconnect(client):
        client.disconnect() 

    def subscribe(client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        client.subscribe(topic)
        client.on_message = on_message

