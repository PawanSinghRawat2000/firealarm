import conf,json,time
from boltiot import Bolt,Sms

mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
sms=Sms(conf.SSID,conf.AUTH_TOKEN,conf.TO_NUMBER,conf.FROM_NUMBER)
threshold=30

while True:
    print("Reading sensor value")
    response=mybolt.analogRead('A0')
    data=json.loads(response)

    try:
        sensor_value=int(data['value'])
        temperature=str((sensor_value*100)/1024)
        if(float(temperature)>threshold):
            print("Alert! Temperature value is:" +temperature,"C","Making twillio to send sms")
            mybolt.digitalWrite('1','HIGH')      #make buzzer on
            response=sms.send_sms("Alert! Fire in the company.")
            mybolt.digitalWrite('2','HIGH')      #make led on
            print("Response received from twillio:" + str(response.status))
            time.sleep(10)
        else:
            mybolt.digitalWrite('1','LOW')
            mybolt.digitalWrite('1','LOW')
            print("The temperature is:" +temperature)
            time.sleep(10)
    except Exception as e:
        print("Error occured: ",e)
        time.sleep(10)

