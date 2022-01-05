from machine import Pin, PWM, DEC, Timer
from time import sleep

# Decode signals from rotary encoder
p1 = Pin(15, mode=Pin.IN)
p2 = Pin(33, mode=Pin.IN)
dec = DEC(0,p1,p2)

# Set up motor control PWM pins

# Initially forward at 50% speed
dec.clear()
print('Encoder reading: {}'.format(dec.count()))
print('Forward 50%')
m1 = PWM(Pin(14),freq=200,duty=50,timer=2)
m2 = PWM(Pin(32),freq=200,duty=0,timer=3)
sleep(5)
print('Encoder reading: {}'.format(dec.count()))

# Fast current decay
print('Fast current decay')
encoder_before_stop = dec.count()
m1.duty(0)
sleep(2)
encoder_after_stop = dec.count()
print('Encoder reading: {}'.format(encoder_after_stop))
print('Encoder motion during deceleration: {}'.format(encoder_after_stop-encoder_before_stop))
print('')

# Forward at 50%
dec.clear()
print('Encoder reading: {}'.format(dec.count()))
print('Forward 50%')
m1.duty(50)
sleep(5)
print('Encoder reading: {}'.format(dec.count()))

# Slow current decay - braking
print('Slow current decay')
encoder_before_stop = dec.count()
m1.duty(100)
m2.duty(100)
sleep(2)
encoder_after_stop = dec.count()
print('Encoder reading: {}'.format(dec.count()))
print('Encoder motion during deceleration: {}'.format(encoder_after_stop-encoder_before_stop))
print('')

# Reverse at 20% speed
dec.clear()
print('Encoder reading: {}'.format(dec.count()))
print('Reverse 20%')
m1.duty(0)
m2.duty(20)
sleep(5)
print('Encoder reading: {}'.format(dec.count()))

# Fast current decay
print('Fast current decay')
m2.duty(0)
sleep(1)
print('Encoder reading: {}'.format(dec.count()))
print('')

# Forward at 5% speed
dec.clear()
print('Encoder reading: {}'.format(dec.count()))
print('Forward 5%')
m1.duty(5)
sleep(5)
print('Encoder reading: {}'.format(dec.count()))

print('Fast current decay')
m1.duty(0)
print('Encoder reading: {}'.format(dec.count()))
print('')

# dec.count()
# dec.count_and_clear()
# dec.clear()
# dec.pause()
# dec.resume()

# def tcb(timer):
#
#     global dec
#     print(dec.count())
#
# t1 = Timer(1)
# t1.init(period=500, mode=t1.PERIODIC, callback=tcb)
