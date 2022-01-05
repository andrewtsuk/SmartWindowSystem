from time import sleep
from machine import Pin, PWM, DEC, Timer, I2C
from hcsr04 import HCSR04
from mqttclient import MQTTClient
import network
import sys
import time

status = ""
change= False
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
temp = ""
weather = ""
humidity = ""
AQI = ""
p1 = Pin(15, mode=Pin.IN)
p2 = Pin(33, mode=Pin.IN)
dec = DEC(0,p1,p2)
sensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)
m1 = PWM(Pin(14),freq=200,duty=0,timer=1)
m2 = PWM(Pin(32),freq=200,duty=0,timer=1)
while True:
    f = open('response.txt', 'r')
    status= f.read()
    print(status)
    f.close()
    def mqtt_callback(topic, msg):
        print("RECEIVE topic = {}, msg = {}".format(topic.decode('utf-8'), msg.decode('utf-8')))
        message = msg.decode('utf-8')
        list = message.split(",")
        global temp, weather, humidity, AQI
        temp = list[0]
        weather = list[1]
        humidity = list[2]
        AQI = list[3]
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(session +"/data")
    print("waiting for data ...")
    mqtt.wait_msg()
    time.sleep(30)
    highT = 85
    lowT = 65
    AQIsetting = 80
    print("settings")
    if int(AQI) > AQIsetting:
        if status == "open":
            change = True
            status = "closed"
    if (float(temp) < lowT or float(temp) > highT) and change == False:
        if status == "open":
            change = True
            status = "closed"
    conditions = ["clear", "rain,", "cloud"]
    if change == False:
        for x in range(0,len(conditions)-1):
            if weather.find(conditions[x]) != -1:
                if status == "closed":
                    change == True
                    status == "open"
                break
    if change == True:
        if status == "open":
            complete = False
            print("opening")
            while complete == False:
                dec.clear()
                m1.duty(50)
                sleep(1)
                m1.duty(0)
                sleep(1)
                try:
                    distance = sensor.distance_cm()
                    print(distance)
                    if distance > 10:
                        complete = True
                except KeyboardInterrupt:
                    pass
            f = open('response.txt', 'w')
            f.write("open")
            f.close()
        else:
            complete = False
            print("closing")
            while complete == False:
                dec.clear()
                m2.duty(50)
                sleep(1)
                m2.duty(0)
                sleep(1)
                try:
                    distance = sensor.distance_cm()
                    print(distance)
                    if distance < 3:
                        complete = True
                except KeyboardInterrupt:
                    pass
            f = open('response.txt', 'w')
            f.write("closed")
            f.close()
    adafruitIoUrl = 'io.adafruit.com'
    adafruitUsername = 'andrewtsuk'
    adafruitAioKey = 'aio_kvHL51xFRLTmFAreZ4KR4QGIi5Wh'

    def sub_cb(topic, msg):
        print((topic, msg))

    print("Connecting to Adafruit")
    mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
    time.sleep(0.5)
    print("Connected!")

    mqtt.set_callback(sub_cb)

    feedName = "andrewtsuk/feeds/project"
    testMessage = "Status: " + status + ", Temperature: " + temp + "F, Weather: " + weather + ", AQI: " + AQI + ", Humidity" + humidity +"%"
    mqtt.publish(feedName,testMessage)
    print("Published {} to {}.".format(testMessage,feedName))

    mqtt.subscribe(feedName)
    sleep(600)
