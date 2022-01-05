from mqttclient import MQTTClient
import network
import sys
import time

"""
Get measurement results from microphyton board and plot on host computer.
Use in combination with mqtt_plot_mpy.py.

Install paho MQTT client and matplotlib on host, e.g.
    $ pip install paho-mqtt
    $ pip install matplotlib

Start this program first on the host from a terminal prompt, e.g.
    $ python mqtt_plot_host.py
then run mqtt_plot_mpy.py on the ESP32.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

session = 'testtopic/andeproject'
BROKER = 'broker.mqttdashboard.com'
qos = 0
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port=1883)
print("Connected!")
while True:
    temp = ""
    weather = ""
    humidity = ""
    AQI = ""
    def mqtt_callback(topic, msg):
        print("RECEIVE topic = {}, msg = {}".format(topic.decode('utf-8'), msg.decode('utf-8')))
        message = msg.decode('utf-8')
        list = message.split(",")
        global temp, weather, humidity, AQI
        print(list[0])
        temp = list[0]
        weather = list[1]
        humidity = list[2]
        AQI = list[3]
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(session +"/data")
    print("waiting for data ...")
    mqtt.wait_msg()
    time.sleep(40)