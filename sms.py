from data import secrets
import smtplib

carrier_email_extensions = {
	'att': '@mms.att.net',
	'sprint': '@page.nextel.com',
	'tmobile': '@tmomail.net',
	'verizon': '@vtext.com'
}

def send(message):
	recipient_address = secrets.recipient_phone_number[0] + carrier_email_extensions[secrets.recipient_phone_number[1]]
	auth = (secrets.gmail_address, secrets.gmail_password)

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(auth[0], auth[1])

	server.sendmail( auth[0], recipient_address, message)
