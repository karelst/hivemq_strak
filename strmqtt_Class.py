
import paho.mqtt.client as mqtt
import ssl
import time
from dotenv import load_dotenv
import os


class MqttApp:
    def __init__(self):
        self.client = None
        self.connection_ok = False

        # slovník posledních hodnot témat
        self.topic_values = {
            "STRAKbeep": "none",
            "STRAKbeepSubs": "none",
            "InfoUpdate": "none",
            "TeplarnaOnOff": -1,
            "TeplarnaOnOffSubs": "none",
            "isalive": -1,
            "TeplarnaStav": "none",
            "teploty": "none",
            "pir": "none",
            "WillTopic": "none"
        }

        self.topics = list(self.topic_values.keys())

    # ==================================================
    # MQTT CALLBACKS
    # ==================================================
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

        for topic in self.topics:
            client.subscribe(topic)
        
        client.publish('InfoUpdate','1')

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()

        if msg.topic not in ("isalive", "WillTopic"):
            print(f"Received topic '{msg.topic}' = '{payload}'")
        else:
            print(".", end="", flush=True)

        self.topic_values[msg.topic] = payload
        self.check_connection()

    # ==================================================
    # CONNECTION MANAGEMENT
    # ==================================================
    def connect_broker(self):
    #    print(">>>>>>>>>> connect_broker() START >>>>>>>>>>")

        if self.connection_ok:
            #print(">>>>>>>>>> connection already OK >>>>>>>>>>")
            return 

        print("---------- NEW CONNECTION ----------")

        self.client = mqtt.Client()

        # TLS / SSL
        self.client.tls_set(
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        load_dotenv()  # loads variables from .env into environment

        hive_user = os.getenv("MQ_USERNAME")
        hive_psw = os.getenv("MQ_PSW")
       
        self.client.username_pw_set(hive_user, hive_psw )
        # print(f">>>>>>>>>>>>>>>\\\hive_user, hive_psw...{hive_user},{hive_psw}")
        # callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        
        broker = os.getenv("MQ_URL")
        nport = 8883
        mport = int(os.getenv("PORT"))
        print(f">>>>>>>>broker,port..{broker} , {mport}")
        # self.client.connect(broker, port, 60)
        self.client.connect(broker, 8883, 60)
        self.client.loop_start()

        time.sleep(1)
        self.connection_ok = self.client.is_connected()

    def check_connection(self):
        if self.client:
            self.connection_ok = self.client.is_connected()
        return self.connection_ok

    def disconnect_broker(self):
        if not self.client:
            return

        print("Exiting...")
        self.client.loop_stop()
        self.client.disconnect()
        self.connection_ok = False

    # ==================================================
    # PUBLISH / ACCESSORS
    # ==================================================
    def publish(self, topic, message):
        if not self.check_connection():
            print("⚠️  Not connected, publish skipped")
            return

        print(f"*** publish({topic}, {message}) ***")
        result = self.client.publish(topic, message)
        print(f"Publish result: {result}")

    def get_topic_values(self):
        return self.topic_values.copy()



if __name__ == "__main__":
    app = MqttApp()

    app.connect_broker()

    print("---------- SLEEP 25 ----------")
    time.sleep(25)

    print("---------- DISCONNECT ----------")
    app.disconnect_broker()
