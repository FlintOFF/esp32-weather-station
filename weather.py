import json
import network
import urequests
from machine import I2C, Pin
from time import sleep_ms

import sys
sys.path.append('/pyboard/lib')

from esp8266_i2c_lcd import I2cLcd

f = open('config.json', 'r')
config = json.loads(f.read())

WEATHER_CITY = config['WEATHER']['CITY']
WEATHER_API_KEY = config['WEATHER']['API_KEY']
WIFI_SSID = config['WIFI']['SSID']
WIFI_PASS = config['WIFI']['PASSWORD']

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

def display_init():
    i2c = I2C(scl=Pin(19), sda=Pin(18), freq=100000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    return lcd

def display_debug(lcd, text):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(text)

def display_update(lcd, temp, temp_feelslike, humidity, wind_kph, text):
    lcd.clear()

    lcd.move_to(0, 0)
    lcd.putstr("T:")
    lcd.move_to(2, 0)
    lcd.putstr("%2d" % round(temp))

    lcd.move_to(5, 0)
    lcd.putstr("H:")
    lcd.move_to(7, 0)
    lcd.putstr("%2d" % humidity)

    lcd.move_to(10, 0)
    lcd.putstr("TF:")
    lcd.move_to(13, 0)
    lcd.putstr("%2d" % round(temp_feelslike))

    lcd.move_to(0, 1)
    lcd.putstr(text)

lsd = display_init()

display_debug(lsd, 'Start')

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_SSID, WIFI_PASS)

display_debug(lsd, 'WIFI conecting')

while True:
    if station.isconnected():
        break

display_debug(lsd, station.ifconfig()[0])
sleep_ms(5 * 1000) # 5 sec

while True:
    response = urequests.get("http://api.apixu.com/v1/current.json?key=%s&q=%s" % (WEATHER_API_KEY, WEATHER_CITY))
    if response.status_code != 200:
        display_debug(lsd, 'Error status code: %n' % response.status_code)
        sleep_ms(1 * 60 * 1000)  # 1min
        display_debug(lsd, '')
        continue

    data = response.json()
    temp = data['current']['temp_c']
    humidity = data['current']['humidity']
    temp_feelslike = data['current']['feelslike_c']
    wind_kph = data['current']['wind_kph']
    text = data['current']['condition']['text']

    display_update(lsd, temp, temp_feelslike, humidity, wind_kph, text)
    print("UPDATED")
    sleep_ms(10 * 60 * 1000) # 10min
