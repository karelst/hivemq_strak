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


def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

# Set up the client
client = mqtt.Client()

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
client.loop_forever()
