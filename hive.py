import paho.mqtt.client as mqtt

# Define the MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # You can subscribe to topics here
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

# Set up the client
client = mqtt.Client()

# Set the username and password if necessary (optional)
# client.username_pw_set("your_username", "your_password")

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the HiveMQ broker (use the appropriate broker URL and port)
broker = "broker.hivemq.com"  # Public HiveMQ broker
port = 1883  # MQTT default port
client.connect(broker, port, 60)

# Loop forever to keep the connection alive and listen for messages
client.loop_forever()
