import RPi.GPIO as GPIO 
import time
from gpiozero import LED
from time import sleep
from gpiozero import MotionSensor
import datetime

mini=-1
#PAHO settings
import paho.mqtt.client as paho
import time
 
def on_publish(client, userdata, mid):
    print('mid: '+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    global mini
    mini=int(msg.payload)


client = paho.Client() 
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('broker.mqttdashboard.com', 1883)
client.subscribe('raspberry1234/getmin1234', qos=1)
client.on_publish = on_publish
client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Sensor 1
TRIG1=18
ECHO1=23

#Sensor 2
TRIG2=27
ECHO2=22

#Sensor 3
TRIG3=19
ECHO3=26

#Sensor 4
TRIG4=5
ECHO4=6

led1 = LED(17)  #LED Yellow
led11 = LED(11)  #LED Green

led2 = LED(24)  #LED Yellow
led21 = LED(9)  #LED Green

led3 = LED(13)  #LED Yellow
led31 = LED(10)  #LED Green

led4 = LED(21)  #LED Yellow
led41 = LED(20)  #LED Green

#Direction LEDs
dirLED0 = LED(14)
dirLED1 = LED(15)
dirLED2 = LED(25)
dirLED3 = LED(8)


#for Yellow LED to on for all slots
led1.on()
led2.on()
led3.on()
led4.on()


print "Distance measurement is in progress"

#Pin setup of sensor 1
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.output(TRIG1,False)        #change of code made here.
GPIO.setup(ECHO1,GPIO.IN)

#Pin setup of sensor 2
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.output(TRIG2,False)        # change of code made here.
GPIO.setup(ECHO2,GPIO.IN)

#Pin setup of sensor 3
GPIO.setup(TRIG3,GPIO.OUT)
GPIO.output(TRIG3,False)        # change of code made here.
GPIO.setup(ECHO3,GPIO.IN)

#Pin setup of sensor 4
GPIO.setup(TRIG4,GPIO.OUT)
GPIO.output(TRIG4,False)        # change of code made here.
GPIO.setup(ECHO4,GPIO.IN)


#Switch off Direction LEDs
def dirOff():
    dirLED0.off()
    dirLED1.off()
    dirLED2.off()
    dirLED3.off()
#PIR MOTION SENSOR MODULE
def pir():
    pir = MotionSensor(16)
    if pir.motion_detected:
        sleep(0.85);
        print("Motion detected!")
        global mini
        print "mini="
        print mini
        if(mini==1000):
            print "Parking Full"
            #break
        else:
            global mini
            x=mini
            dIndicator=x/5
            if(dIndicator==0):
                dirLED0.on()
            elif(dIndicator==1):
                dirLED0.on()
                dirLED1.on()
            elif(dIndicator==2):
                dirLED0.on()
                dirLED1.on()
                dirLED2.on()
            elif(dIndicator==3):
                dirLED0.on()
                dirLED1.on()
                dirLED2.on()
                dirLED3.on()
        if(mini!=1000):
            if(x==0):
                print "green 0"
                led11.on()

            if(x==1):
                led21.on()
                          
            if(x==2):
                led31.on()

            if(x==3):
                led41.on()


# Main Sensor Codes
flag0_0=0
flag0_1=0
flag1_0=0
flag1_1=0
flag2_0=0
flag2_1=0
flag3_0=0
flag3_1=0
while True:
    print "Waiting for sensor to settle"
    pir()
##	print "value: "+st

#Codes for SENSOR 1:
    time.sleep(0.7)	#code change made here
	
    GPIO.output(TRIG1,True)
    #GPIO.output(TRIG2,True)
    time.sleep(0.00001)
    GPIO.output(TRIG1,False)
    #GPIO.output(TRIG2,False)
	
    while GPIO.input(ECHO1)==0:
            pulse_start1 = time.time()
	
		
    while GPIO.input(ECHO1) == 1:
            pulse_end1 = time.time()

    pulse_duration1 = pulse_end1-pulse_start1

    distance1 = pulse_duration1 * 17150
    distance1 = round(distance1,2)

    if distance1 > 2 and distance1 < 30:
            print "Sensor 1:- Distance:",distance1 - 0.5,"cm"
            led1.off()
            led11.off()

            data1 = '{"slotid":"0","flag":"1"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            
                
##		if flag0_1 == 0:
##                    print "hello"
            if(flag0_1==0):
                ts=time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                data2='{"slotid":"0","intime":"2017-02-21 10:34:09","outtime":"abcd"}'
                (rc, mid) = client.publish('raspberry1234/data1234/transaction', str(data2), qos=1)

                dirOff()
                flag0_0=1
                flag0_1=1
    else:
            print "Sensor 1: No Object"
            led1.on()

            data1 = '{"slotid":"0","flag":"0"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            if(flag0_0!=0):
                ts=time.time()
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                flag0_0=0
                flag0_1=0
		
		

#Code for sensor 2:
    time.sleep(0.7)
    GPIO.output(TRIG2,True)
    time.sleep(0.00001)
    GPIO.output(TRIG2,False)
    while GPIO.input(ECHO2)==0:
            pulse_start2 = time.time()

    while GPIO.input(ECHO2) == 1:
            pulse_end2 = time.time()

    pulse_duration2 = pulse_end2-pulse_start2

    distance2 = pulse_duration2 * 17150
    distance2 = round(distance2,2)

    if distance2 > 2 and distance2 < 30:
            print "Sensor 2:- Distance:",distance2 - 0.5,"cm"
            led2.off()
            led21.off()

            data1 = '{"slotid":"1","flag":"1"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            
            if(flag1_1==0):
                ts=time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                dirOff()
                flag1_0=1
                flag1_1=1

    else:
            print "Sensor 2: No Object"
            led2.on()

            data1 = '{"slotid":"1","flag":"0"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            if(flag1_0!=0):
                ts=time.time()
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                flag1_0=0
                flag1_1=0


#Code for sensor 3:
    time.sleep(0.7)
    GPIO.output(TRIG3,True)
    time.sleep(0.00001)
    GPIO.output(TRIG3,False)
    while GPIO.input(ECHO3)==0:
            pulse_start3 = time.time()

    while GPIO.input(ECHO3) == 1:
            pulse_end3 = time.time()

    pulse_duration3 = pulse_end3-pulse_start3

    distance3 = pulse_duration3 * 17150
    distance3 = round(distance3,2)

    if distance3 > 2 and distance3 < 30:
            print "Sensor 3:- Distance:",distance3 - 0.5,"cm"
            led3.off()
            led31.off()

            data1 = '{"slotid":"2","flag":"1"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            dirOff()
            if(flag2_1==0):
                ts=time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                dirOff()
                flag2_0=1
                flag2_1=1

    else:
            print "Sensor 3: No Object"
            led3.on()

            data1 = '{"slotid":"2","flag":"0"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            if(flag2_0!=0):
                ts=time.time()
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                flag2_0=0
                flag2_1=0
    

#Code for sensor 4:
    time.sleep(0.7)
    GPIO.output(TRIG4,True)
    time.sleep(0.00001)
    GPIO.output(TRIG4,False)
    while GPIO.input(ECHO4)==0:
            pulse_start4 = time.time()

    while GPIO.input(ECHO4) == 1:
            pulse_end4 = time.time()

    pulse_duration4 = pulse_end4-pulse_start4

    distance4 = pulse_duration4 * 17150
    distance4 = round(distance4,2)

    if distance4 > 2 and distance4 < 30:
            print "Sensor 4:- Distance:",distance4 - 0.5,"cm"
            led4.off()
            led41.off()

            data1 = '{"slotid":"3","flag":"1"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            dirOff()
            if(flag3_1==0):
                ts=time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                dirOff()
                flag3_0=1
                flag3_1=1

    else:
            print "Sensor 4: No Object"
            led4.on()
            data1 = '{"slotid":"3","flag":"0"}'
            (rc, mid) = client.publish('raspberry1234/data1234/distance', str(data1), qos=1)
            if(flag3_0!=0):
                ts=time.time()
                st2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                flag3_0=0
                flag3_1=0

        
GPIO.cleanup()

