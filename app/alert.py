import geocoder
from twilio.rest import Client


def sendAlert():
    nums = ['+911234567890', '+911234567890', '+911234567890', '+911234567890']
    g = geocoder.ip('me')
    msg = "Accident detected at "+g.address+". Lattitude: " + \
        str(g.latlng[0])+", Longitude: "+str(g.latlng[1])
    account_sid = '' #twillio account sid here
    auth_token = '' #twillio auth_token here
    client = Client(account_sid, auth_token)
    for i in nums:
        try:
            message = client.messages.create(
                body=msg,
                from_='', #your twillio number here
                to=i
            )
            print(message.sid)
        except:
            print("Unable to send message to ", i)


# import requests

# def get_location(lat, lon):
#     url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key=YOUR_API_KEY'
#     response = requests.get(url)
#     data = response.json()
#     if data['status'] == 'OK':
#         result = data['results'][0]['formatted_address']
#         return result
#     else:
#         return None
