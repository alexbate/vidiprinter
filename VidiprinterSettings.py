import shelve, os

def printOptions():
	print 'Welcome to Vidiprinter Settings'
	print ''
	print 'Please select an option:'
	print '1: Change Gmail Login'
	print '2: Change Gmail Password'
	print '3: Change Facebook Notifications RSS URL'
	print '4: Change Twitter consumer key'
	print '5: Change Twitter consumer secret'
	print '6: Reset Twitter login details'
	print '99: Exit'
	print ''

storage = shelve.open('.VidiprinterCreds')	
numInput = 0

while numInput != 99:
	#Setup Input
	printOptions()
	numInput = int(raw_input())
	
	if numInput == 1:
		storage['gmailLogin'] = raw_input('Please enter your new Gmail login: ')
	elif numInput == 2:
		storage['gmailPass'] = raw_input('Please enter your new Gmail password: ')
	elif numInput == 3:
		storage['FBurl'] = raw_input('Please enter your new Facebook notifications RSS URL: ')
	elif numInput == 4:
		storage['consumer_key'] = raw_input('Please enter your new Twitter consumer key: ')
	elif numInput == 5:
		storage['consumer_secret'] = raw_input('Please enter your new Twitter consumer secret: ')
	elif numInput == 6:
		os.remove(os.path.expanduser('~/.my_app_credentials'))
		print 'You will be prompted for new Twitter login details next time you launch the main Vidiprinter file'
	elif numInput != 99:
		print "Input not accepted. Please try again"

print "Thank you for using Vidiprinter Settings"
storage.close()		
