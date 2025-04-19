#f3d0981b4d84442f9406f8b208f421b0.s1.eu.hivemq.cloud
#broker = "f3d0981b4d84442f9406f8b208f421b0.s1.eu.hivemq.cloud" 
#
#//UsedTopics:
# //&S"STRAKbeep"
# //&S"STRAKbeepSubs"
# //&S"InfoUpdate"
# //&S"TeplarnaOnOff"
# //&S"TeplarnaOnOffSubs"
# //&S"isalive"
# //&S"TeplarnaStav"
# //&S"teploty"
# //&S"pir"
# //&S"WillTopic"
import paho.mqtt.client as mqtt
import ssl
import time





# Define the MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to topics (you can add more topics as needed)

    client.subscribe("STRAKbeep")
    client.subscribe("STRAKbeepSubs")
    client.subscribe("InfoUpdate")
    client.subscribe("TeplarnaOnOff")    #, qos=1)
    client.subscribe("TeplarnaOnOffSubs")  #, qos=1)
    client.subscribe("isalive")
    client.subscribe("TeplarnaStav")  #, qos=1)
    client.subscribe("teploty")
    client.subscribe("pir")
    client.subscribe("WillTopic")

# "STRAKbeep",
# "STRAKbeepSubs",
# "InfoUpdate",
# "TeplarnaOnOff",    #, qos=1,
# "TeplarnaOnOffSubs",  #, qos=1,
# "isalive",
# "TeplarnaStav",  #, qos=1,
# "teploty",
# "pir",
# "WillTopic",

def get_topic_values():
    return topic_values


topic_values = { #dictionary
"STRAKbeep":"none",
"STRAKbeepSubs":"none",
"InfoUpdate":"none",
"TeplarnaOnOff":-1, 
"TeplarnaOnOffSubs":"none",
"isalive":-1,
"TeplarnaStav":"none",
"teploty":"none",
"pir":"none",
"WillTopic":"none"
}

def on_message(client, userdata, msg):
    print(f"Received topic '{msg.topic}' = '{msg.payload.decode()}'")
    # Save into "topic_values" dictionary
    topic_values[msg.topic] =msg.payload.decode()
    # print(f"+++topic_values[{msg.topic}] ='{topic_values[msg.topic]}'")

    # if msg.topic == 'STRAKbeep':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'STRAKbeepSubs':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'InfoUpdate':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'TeplarnaOnOff':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'TeplarnaOnOffSubs':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'isalive':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'TeplarnaStav':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'teploty':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'pir':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # elif msg.topic == 'WillTopic':
    #     print(f"found {msg.topic} = {msg.payload.decode()}")
    # else:
    #     print("Text not found")


def connect_broker(client):
    print(f"connect_broker() START")
     # Set up the client
    # client = mqtt.Client()

    # Set SSL context for secure connection
    client.tls_set(
    #    ca_certs="path_to_ca_cert.pem",  # Path to the CA certificate (for server verification)
        # certfile=None,                   # Path to client certificate if needed (for client auth)
        # keyfile=None,                    # Path to client key if needed (for client auth)
        tls_version=ssl.PROTOCOL_TLSv1_2  # TLS version (usually v1.2 is preferred)
    )

    # If the broker requires username/password, set them
    client.username_pw_set("dashboard2", "Legolas007")

    # Assign the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the HiveMQ broker using SSL
    #broker = "broker.hivemq.com"  # Public HiveMQ broker (SSL-enabled)
    broker = "f3d0981b4d84442f9406f8b208f421b0.s1.eu.hivemq.cloud" 
    port = 8883  # SSL port for HiveMQ (default is 8883 for secure connections)

    client.connect(broker, port, 60)

    # Loop forever to keep the connection alive and listen for messages
    #print(f"connect_broker() LOOP>>>>>>>>>>>>>>")
    client.loop_start()

def disconnect_broker(client):
    print("Exiting...")
    client.loop_stop()  # Stop the loop when exiting
    client.disconnect()  # Disconnect from the broker
    
    
def create_client ():   #(client):
    client = mqtt.Client()
    return client
    # return create_client

def publish(client, topic, message):
    client.publish(topic, message)
    
if __name__ == "__main__":
    client = mqtt.Client()

    connect_broker(client)
    time.sleep(25)  # Simulate other work
    disconnect_broker(client)