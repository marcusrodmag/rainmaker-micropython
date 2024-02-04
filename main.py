import time
import network
from broker.mqtt import MQTTClient
import machine

def sub_cb(topic, msg):
  msg_string = msg.decode("utf-8")
  msg_int = int(msg_string)
  print("Command received: " + str(msg_int))
  led_amarelo.value(msg_int)
  # if topic == b'notification' and msg == b'received':
  #   print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  print("Conectando ao Broker")
  client_id = "123321"
  print("Cliente ID: " + client_id)
  print("Server: " + mqtt_server)
  print("Topic: " + topic_sub)
  time.sleep(4)
  client = MQTTClient(client_id, mqtt_server, port=1883, user=mqtt_user, password=mqtt_pass)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  print("Um erro ocorreu durante a conexão com o broker")
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      led_board.value(0)
      client.publish(topic_pub, msg)
      last_message = time.time()
      led_board.value(1)
      counter += 1
  except OSError as e:
    restart_and_reconnect()
  time.sleep(1)