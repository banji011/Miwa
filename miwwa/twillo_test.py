# from flask import Flask 
from twilio.rest import Client

# app = Flask(__name__)


# Your Account Sid and Auth Token from twilio.com/console
account_sid = "AC4a9cb2d3499e217f981a695d9f0a4804"
auth_token = "629ff0858132845bfc5ea4deae9400f9"
client = Client(account_sid, auth_token)
message = client.messages.create(
 body='This is a test message to Yeblo !',
 from_='+12563843897',
 to='+2347065907455'
 )
print(message.sid)




# if __name__=='__main__':
#     manager.run()