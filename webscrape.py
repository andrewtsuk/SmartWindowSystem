import requests
import urllib.request
import time
from urllib.request import urlopen
import paho.mqtt.client as mqtt

session = 'testtopic/andeproject'
BROKER = 'broker.mqttdashboard.com'

print("Connecting to MQTT broker", BROKER, "...", end="")
client = mqtt.Client(session)
client.connect(BROKER,1883)
print("Connected!")

while True:
    cityh= "berkeley"
    url = "https://www.iqair.com/us/usa/california/" + cityh
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    temp0_index = html.find('Temperature')
    temp_index = temp0_index+40
    digits = -1
    for x in range(6):
        if html[temp_index+x:temp_index+x+1] != "C":
            digits = digits + 1
        else:
            break
    temp = float(html[temp_index:temp_index+digits])
    print("Temperature: "+ str(temp)+"F")
    weather0_index=html.find('="">Weather')
    firstindex = weather0_index+40
    lastindex = 0
    for x in range(30):
        if html[firstindex+x:firstindex+x+1] != "<":
            pass
        else:
            lastindex=firstindex+x
            break
    weather = html[firstindex:lastindex]
    print("Weather Status: " + weather)
    humidity0_index=html.find('Humidity')
    firstindex = humidity0_index+37
    lastindex = 0
    for x in range(4):
        if html[firstindex+x:firstindex+x+1] != "%":
            pass
        else:
            lastindex=firstindex+x
            break
    humidity=int(html[firstindex:lastindex])
    print("humidity: "+str(humidity)+"%")
    aqi0_index = html.find('aqi-value__value"')
    aqi0=html[aqi0_index:aqi0_index+50]
    aqi_index = aqi0.find('>')
    skip = 0;
    for x in range(4):
        test = html[aqi0_index+aqi_index+x:aqi0_index+aqi_index+1+x]
        if test != "0" and test != "1" and test != "2" and test != "3" and test != "4" and test != "5" and test != "6" and test != "7" and test != "8" and test != "9":
            skip = skip + 1
        else:
            break
    AQI= int(html[aqi0_index+aqi_index+1:aqi0_index+aqi_index+1+skip])
    print("AQI: "+str(AQI))
    topic = "{}/data".format(session)
    data = "{},{},{},{}".format(str(temp),weather,str(humidity),str(AQI))
    print("send topic='{}' data='{}'".format(topic, data))
    client.publish(topic, data)
    time.sleep(10)