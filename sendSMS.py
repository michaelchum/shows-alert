import os

def send_sms(to,subject):

	twilio_sid = 'AC33cb0baf0ccabcc8d455bbf304b6c3c4'
	twilio_auth = '569364d21628a50c22a6861d78178ef8'
	twilio_url = 'https://api.twilio.com/2010-04-01/Accounts/%(twilio_sid)s/SMS/Messages.json' % locals()

	twilio_data = {
		'From': '+14387937949',
		'To' : to,
		'Body': subject
	}

	t = requests.post(twilio_url, data=twilio_data, auth=(twilio_sid, twilio_auth))

	print t
