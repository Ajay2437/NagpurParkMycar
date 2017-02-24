import paho.mqtt.client as paho
import pymysql
import json,urllib

db = pymysql.connect(host="technothon1.ceg3ohfqhx8p.ap-south-1.rds.amazonaws.com", user="technothon1", passwd="technothon123", db="technothon_park_mycar")
cur = db.cursor()
def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscribed: '+str(mid)+' '+str(granted_qos))

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    #print userdata

def on_message(client, userdata, msg):
    print(msg.topic+' '+str(msg.qos)+' '+str(msg.payload))
    data = json.loads(msg.payload)
    if(msg.topic=='raspberry1234/data1234/distance'):
        #data = json.loads(msg.payload)
        slotid=data["slotid"]
        flag=data["flag"]
        print('slotid:'+slotid+'flag='+flag)
        cur.execute("UPDATE slot_table SET flag=%s where slotId=%s",(flag, slotid))
        db.commit()
        var=0
        cur.execute("SELECT min(slotId) FROM slot_table where flag=0")
        for row in cur.fetchall():
            if(row[0]==None):
                #global var
                var=1000
            else:
                #global var
                var=int(row[0])
        (rc, mid) = client.publish("raspberry1234/getmin1234", str(var), qos=1)

    elif(msg.topic=='raspberry1234/data1234/transaction'):
        data = json.loads(msg.payload)
        slotId=data["slotid"]
        inTime=data["intime"]
        outTime=data["outtime"]
        print('slotid:'+slotId+'intime='+inTime+'outtime='+outTime)
        if(outTime=='abcd'):
                cur.execute("INSERT INTO transaction (slotId,in_time,out_time) VALUES(%s, %s)", (slotId, inTime))
                db.commit()
        else:
                cur.execute("UPDATE transaction SET out_time=%s where slotId=%s and out_time is NULL", (outTime, slotId))
                db.commit()

client = paho.Client()
client.on_publish = on_publish
client.connect('broker.mqttdashboard.com', 1883)
#var=0
#(rc, mid) = client.publish("raspberry1234/getmin1234", str(var), qos=1)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.subscribe('raspberry1234/data1234/#', qos=1)
