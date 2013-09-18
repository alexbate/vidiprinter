import imaplib, re, time, sys, gdata, datetime, os, httplib2, urllib2, feedparser, shelve
from twitter import *
from email.parser import HeaderParser

def output_line(text):
  for char in text:
    sys.stdout.write( '%s' % char )
    sys.stdout.flush()
    time.sleep(0.1)
  print ''

storage = shelve.open('.VidiprinterCreds')

def paramNotFound(key):
	storage[key] = raw_input("Please enter your " + key + ": ")
	storage.sync()
	
if storage.has_key('gmailLogin'):
	gmailLogin = storage['gmailLogin']
else:
	paramNotFound('gmailLogin') 
	
if storage.has_key('gmailPass'):
	gmailPass = storage['gmailPass']
else:
	paramNotFound('gmailPass') 

#Setup Gmail
g=imaplib.IMAP4_SSL('imap.gmail.com')
g.login(gmailLogin, gmailPass)
g.select("inbox")


def fetch_unread_email(mail):
	result, data = mail.search(None, '(UNSEEN)')
	emailIDs = data[0]
	id_list = emailIDs.split()
	try:
		latest_email_id = id_list[-1]
		result, data = mail.fetch(latest_email_id, "(RFC822)" )

		raw_email = HeaderParser().parsestr(data[0][1])
		output_line('New email from ' + raw_email['From'])
		output_line('Subject: ' + raw_email['Subject'])
	except:
		time.sleep(1)

global FBurl

if storage.has_key('FBurl'):
	FBurl = storage['FBurl']
else:
	paramNotFound('FBurl') 

def facebook():
  global FBurl
  global lastFbTitle
  rawNotifs=urllib2.urlopen(FBurl)
  parsedNotifs=feedparser.parse(rawNotifs)
  
  return parsedNotifs.entries[0].title


#Setup Twitter
#Setup program OAuth keys
if storage.has_key('consumer_key'):
	consumer_key = storage['consumer_key']
else:
	paramNotFound('consumer_key') 

if storage.has_key('consumer_secret'):
	consumer_secret = storage['consumer_secret']
else:
	paramNotFound('consumer_secret')

#Login twitter
TwitterCreds = os.path.expanduser('~/.my_app_credentials')
if not os.path.exists(TwitterCreds):
	oauth_dance("Vidiprinter Twitter Service", consumer_key, consumer_secret, TwitterCreds)
	
token_key, token_secret = read_token_file(TwitterCreds)

twitter = Twitter(
			auth=OAuth(token_key, token_secret, consumer_key, consumer_secret)
			)
  
os.system( [ 'clear','cls'][os.name == 'nt' ] )      
lastUpdate = datetime.datetime.utcnow()
lastFbTitle = facebook()
output_line('Vidiprinter online as of ' + datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S'))

while True:
  SkyTweets = twitter.statuses.user_timeline(id='SkyNewsBreak')
  if datetime.datetime.strptime(SkyTweets[0]['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > lastUpdate:
	output_line('New tweet from @SkyNewsBreak: ' + SkyTweets[0]['text'])

  fetch_unread_email(g)
	
  FBnotif = facebook()
  if FBnotif != lastFbTitle:
    output_line('New Facebook notification: ' + FBnotif)
    lastFbTitle = FBnotif
    
  if datetime.datetime.now().minute % 15  == 0:
    output_line('The time is now ' + datetime.datetime.strftime(datetime.datetime.now(), '%H:%M'))
   
  lastUpdate = datetime.datetime.utcnow() 
  time.sleep(60)
