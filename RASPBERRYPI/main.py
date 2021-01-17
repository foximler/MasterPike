import serial
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input $
import Adafruit_DHT
sensor = Adafruit_DHT.DHT22
pin = 4
import requests
import time
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[20:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial
def getlonglat():
   
   ser=serial.Serial('/dev/ttyUSB0',115200)
   readedText = ser.readline()
   lat = readedText[16:24].decode('utf-8')
   long = readedText[29:35].decode('utf-8').replace(':','')
   ser.close()
   return lat, long

def getweather():
   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
   return humidity, temperature


while True: # Run forever
    lat, long = getlonglat()
    humidity, temperature = getweather()
    uuid = getserial()
    currenttime = int(time.time())
    if GPIO.input(8) == GPIO.HIGH:
        print("Button was pushed!")
        r = requests.get(f"http://masterbait.fish:5000/api?uuid={uuid}&temp={temperature}&humid={humidity}&alert=1&lat={lat}&long={long}&time={currenttime}")
        print(r.status_code, r.reason)
    else:
        r = requests.get(f"http://masterbait.fish:5000/api?uuid={uuid}&temp={temperature}&humid={humidity}&alert=0&lat={lat}&long={long}&time={currenttime}")
        print(r.status_code, r.reason)
        print(uuid)
        print(temperature)
        print(humidity)
        print(lat)
        print(long)
        print(int(time.time()))

    time.sleep(30)
