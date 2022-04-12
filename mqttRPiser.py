import paho.mqtt.client as mqtt
import os
import time
import sys
import json
import statistics
import numpy as np
from gpiozero import CPUTemperature

MASTER_ADDRESS = '192.168.0.178'
MQTT_USER = 'toi2022'
MQTT_PASS = 'toi2022'
MQTT_TOPIC = 'toi/+/+'

MQTT_ADDRESS = '147.229.12.176'
ACCESS_TOKEN = 'SmmvQKIggOMmT22ZWpk2'

#Array of 10 temperatures
allMasterTemperatures = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype=float)

allSlaveTemperatures  = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype=float)

allRPiTemperatures  = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0], dtype=float)


masterIdx = 0
slaveIdx = 0
rpiIdx = 0

sensor_data = {'ESP32_avg': 0,
               'ESP32_max': 0,
               'ESP32_min': 0,
               'ESP32_med': 0,
               'RPi_avg':   0,
               'RPi_max':   0,
               'RPi_min':   0,
               'RPi_med':   0}

def on_connect(client, userdata, flags, rc):
    print('Connected with result code' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global masterIdx
    global slaveIdx
    if msg.topic == "toi/master/temp":
        sensor_data['temp1'] = str(msg.payload)
        
        allMasterTemperatures[masterIdx] = float(msg.payload)
        masterIdx = masterIdx + 1
        
        if masterIdx == 10:
            masterIdx = 0
        
    if msg.topic == "toi/slave/temp":
        sensor_data['temp2'] = str(msg.payload)
        
        allSlaveTemperatures[slaveIdx] = float(msg.payload)
        slaveIdx = slaveIdx + 1
        
        if slaveIdx == 10:
            slaveIdx = 0
        
    print(msg.topic + " " + str(msg.payload))

def main():
    #ESP client
    esp_client = mqtt.Client()
    esp_client.username_pw_set(MQTT_USER, MQTT_PASS)
    esp_client.on_connect = on_connect
    esp_client.on_message = on_message
    esp_client.connect(MASTER_ADDRESS, 1883, 60)
    esp_client.loop_start()
    
    #Thingsboard client
    thingsboard_client = mqtt.Client()
    thingsboard_client.username_pw_set(ACCESS_TOKEN)
    thingsboard_client.connect(MQTT_ADDRESS, 1883, 60)
    thingsboard_client.loop_start()
    
    try:
        while True:
            #Get RPi CPU temp
            #cpu = CPUTemperature()
            #print(cpu.temperature)
            #allRPiTemperatures[rpiIdx] = "{:.3f}".format(cpu.temperature)
            #rpiIdx = rpiIdx + 1
        
            #if rpiIdx == 10:
                #rpiIdx = 0
            
            #Count average temp
            sensor_data['ESP32_avg'] = "{:.3f}".format((np.average(allMasterTemperatures) + np.average(allSlaveTemperatures))/2)
            #sensor_data['RPi_avg'] = "{:.3f}".format((np.average(allRPiTemperatures))
            
            #Count max temp
            sensor_data['ESP32_max'] = "{:.3f}".format(max(np.amax(allMasterTemperatures), np.amax(allSlaveTemperatures)))
            #sensor_data['RPi_max'] = "{:.3f}".format(np.amax(allRPiTemperatures))
            
            #Count min temp
            sensor_data['ESP32_min'] = "{:.3f}".format(max(np.amin(allMasterTemperatures), np.amin(allSlaveTemperatures)))
            #sensor_data['RPi_min'] = "{:.3f}".format(np.amin(allRPiTemperatures))
            
            #Count min med
            sensor_data['ESP32_med'] = "{:.3f}".format(statistics.median([np.median(allMasterTemperatures), np.median(allSlaveTemperatures)]))
            #sensor_data['RPi_med'] = "{:.3f}".format(np.median(allRPiTemperatures))
            
            #Send data to server
            thingsboard_client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
            time.sleep(5)
            
    except:
        print("ERROR")

    thingsboard_client.loop_stop()
    thingsboard_client.disconnect()

if __name__ == '__main__':
    print("MQTT to THINGSBOARD started.\n")
    main()