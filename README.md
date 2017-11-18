# esp32-weather-station
ESP32 Weather station with I2C 1602 LCD display

# install
* git clone git@github.com:FlintOFF/esp32-weather-station.git
* cp example_config.json config.json
* nano config.json
  * Create acocunt on https://www.apixu.com/ and copy API KEY
  * Write API KEY to "API_KEY"
  * Write your city/country to "CITY" (ex. "Cherkasy,UA")
  * Fill field "SSID"
  * Fill field "PASSWORD"
  * save end exit
* connect to USB
* rshell --buffer-size=30 -p /dev/ttyUSB0
* cp -r ./ /pyboard
* unplug
* connect LCD display to ESP32. 
  * SDA to pin 18
  * SCL to pin 19
  * VCC & GND to external power supply
* done
