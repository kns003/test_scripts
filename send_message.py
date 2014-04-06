import requests
import urllib
import smtplib
import json

#Variable declaration
TOKEN = ''  # your Access token here. You can get it @ 'https://developers.facebook.com/tools/explorer/'
USERNAME = '' # your FB username
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
sender = '' #your gmail id
message = 'Hi, This is a test message.'#Message here
password = '' #Your Gmail password

def sendMessage():
	payload = {'access_token': TOKEN}
	response = requests.get('https://graph.facebook.com/'+USERNAME+'/friends?fields=username',params = payload)
	result = json.loads(response.text)
	print result
	email_lists = []
	for user in result['data']:
		try:
			email_lists.append(user['username']+"@facebook.com")
		except Exception,e:
			print "Error :"+ str(e)
	print email_lists
	print len(email_lists)
	for email_list in email_lists:
		session = smtplib.SMTP('smtp.gmail.com',587)
		session.ehlo()
		session.starttls()
		session.ehlo()
		session.login(sender, password)
		session.sendmail(sender,str(email_list),message)
		print 'Message sent to'+str(email_list)
		session.quit()
		
if __name__ == '__main__':
    sendMessage()

		
