from machine import Pin, PWM, DEC, Timer
from time import sleep

# Decode signals from rotary encoder
p1 = Pin(15, mode=Pin.IN)
p2 = Pin(33, mode=Pin.IN)
dec = DEC(0,p1,p2)

# Set up motor control PWM pins

# Initially forward at 50% speed
print('Encoder reading: {}'.format(dec.count()))
print('Forward 50%')
m1 = PWM(Pin(14),freq=200,duty=50,timer=1)
m2 = PWM(Pin(32),freq=200,duty=0,timer=3)
sleep(5)
print('Encoder reading: {}'.format(dec.count()))

# Reverse at 20% speed
dec.clear()
print('Encoder reading: {}'.format(dec.count()))
print('Reverse 20%')
m1.duty(0)
m2.duty(20)
sleep(5)
m2.duty(0)
print('Encoder reading: {}'.format(dec.count()))
dec.clear()