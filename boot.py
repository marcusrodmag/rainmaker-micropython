# https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/
# https://docs.micropython.org/en/latest/esp8266/quickref.html

# from mqtt.umqttsimple import MQTTClient
import time
import ubinascii
import machine
import micropython
import network
import esp
import gc

esp.osdebug(None)
gc.collect()

print("Carregando sistema ...")
print("CPU: " + str(machine.freq()/10000000) + "MHz")

led_amarelo = machine.Pin(5, machine.Pin.OUT)
led_board = machine.Pin(2, machine.Pin.OUT)

wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Conectando a rede batraquio ...")
wifi_client.connect("batraquio", "Tucuna@G7") # Connect to an AP
print("Validando conexão com a rede WiFi ...")
count = 1
while (wifi_client.isconnected() is False):
    led_amarelo.value(0)
    print("Tentativa: " + str(count))
    count = count + 1
    time.sleep(1)
    led_amarelo.value(1)
    time.sleep(1)

device_ip, device_mask, device_router, device_dns = wifi_client.ifconfig()

print("Device IP: " + device_ip)

mqtt_server = "192.168.128.180"
mqtt_user = "moskitto"
mqtt_pass = "moskitto"
# topic_sub = b'homeassistant/arduino/rainmaker/command'
topic_sub = 'homeassistant/arduino/rainmaker/command'
topic_pub = 'homeassistant/arduino/rainmaker/report'

client_id = machine.unique_id()

last_message = 0
message_interval = 5
counter = 0