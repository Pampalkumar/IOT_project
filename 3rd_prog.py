import urllib.request
import json
import vonage 
import time as t
import RPi.GPIO as a

a.setwarnings(False)
a.setmode(a.BOARD)
a.setup(24, a.OUT)
a.setup(26, a.OUT)
a.output(26, a.LOW)

print("waiting for data upload....")
t.sleep(15)
print("data is uploaded successfully..")
t.sleep(10)

c = urllib.request.Request("https://api.thingspeak.com/channels/2623787/fields/2/last.json?api_key=U5UIRVFDOI4779S3")
r = urllib.request.urlopen(c)
r1 = r.read()
dat = json.loads(r1)
data = int(float(dat['field2']))
print("Retrieved data is: ", data)

if data >= 30:
    print("data is more than the threshold value...")
    t.sleep(2)
    print("sending the text msg to phone...")
    client = vonage.Client(key="723d2d91", secret="aLRoKdZ7YbO8NmIf")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "916203313124",
            "text": "A text message sent using the Nexmo SMS API",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    t.sleep(5)
    print("Turning on the fan..")
    t.sleep(1)
    a.output(24, a.HIGH)
    t.sleep(10)
    a.output(24, a.LOW)
    t.sleep(2)
else:
    print("Temperature is normal...")
    print("Thank You")
