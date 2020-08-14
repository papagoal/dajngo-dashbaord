# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC41aa72d651f6093a29cf3dcacf1337e5'
auth_token = '5b375d348575321f9d44ab63b634a269'
client = Client(account_sid, auth_token)


numbers_to_message = ['+12048070812', '+12048986508', "+12046980784"]
for number in numbers_to_message:
    message = client.messages.create(
        body="Please ignore, testing message",
        from_='+15817016599',
        to=number,
    )

print(message.sid)

