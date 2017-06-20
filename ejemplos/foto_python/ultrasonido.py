#
# K3os based Ubuntu Mate
#
# @Fabeltranm
# @luiszener
# @raparram
#
# >>> DEMO ULTRASONIC PHOTO
#
# PREVIOUS STEPS:
# 1. Install the latest version of the library directly from PyPI:   
#   $ sudo apt-get install python-dev python-pip
#   $ sudo pip install max7219
# 2. Please check camera and SPI operation.
#
# PINES:
# > Ultrasound HC-SR04:
#   - ECHO: GPIO 23
#   - TRIG: GPIO 24
# > LED Matrix with MAX7219:
#   - DIN: SPI_MOSI (GPIO 10)
#   - CS : SPI_CE0 (GPIO 8)
#   - CLK: SPI_CLK (GPIO 11)

#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import RPi.GPIO as GPIO                    
import time
import picamera
import max7219.led as led
from PIL import Image

def tomar_foto():
  pc.start_preview()
  display = led.matrix()
  display.show_message("3 2 1 *") 
  name = time.strftime("%Y%m%d_%H%M%S")
  name = name+".jpg"
  pc.capture(name)
  pc.stop_preview()
  pic = Image.open(name)
  print "Mostrando foto ..."+name
  pic.show()
  time.sleep(10)

def distancia():
  print "Esperando para tomar foto ....."
  GPIO.output(TRIG, True)                    #TRIG en estado alto
  time.sleep(0.00001)                        #Delay de 0.00001 segundos
  GPIO.output(TRIG, False)                   #TRIG en estado bajo
  pulse_1 = time.time()
  pulse_start = time.time()
  while GPIO.input(ECHO)==0:                 #Comprueba si ECHO está en estado bajo
     pulse_start = time.time()                #Guarda el tiempo transcurrido, mientras esta en estado bajo
  while GPIO.input(ECHO)==1:                 #Comprueba si ECHO está en estado alto
     pulse_end = time.time()                  #Guarda el tiempo transcurrido, mientras esta en estado alto
  t = pulse_end - pulse_start                #Se obtienen la duración del pulso, calculando la diferencia entre pulse_start  y pulse_end
  distancia = t * (V/2)                      #Se multiplica la duración del pulso, por 17150, para obetener la distancia
  distancia = round(distancia, 2)            #Se redondea a dos decimales

  if distancia > 2 and distancia < 400:      #Comprueba si la distancia está dentro del rango
    print "Distancia: ",distancia,"cm"       #Imprime la distancia 
    if distancia  < 50:                      # toma foto
      tomar_foto()


GPIO.setmode(GPIO.BCM)                     

TRIG = 23                                  #pin 23 como TRIG
ECHO = 24                                  #pin 24 como ECHO
V    = 34300			    			   # Velocidad del sonido 34300cm/s	
pc=picamera.PiCamera()
print "Medicion de la distancia en curso"

GPIO.setup(TRIG,GPIO.OUT)                  #TRIG como salida
GPIO.setup(ECHO,GPIO.IN)                   #ECHO como entrada

GPIO.output(TRIG, False)                   #TRIG en estado bajo
print "Espere que el sensor se estabilice"
time.sleep(2)                              #Esperar 2 segundos

while (True):
  distancia()  
  
GPIO.cleanup()							   #Limpia los pines	
