import imaplib, re, time, sys, gdata, datetime, os, httplib2, urllib2, feedparser, shelve, gdata
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

def googleCalendarLogin(calendar):
	calendar.email = gmailLogin
	calendar.password = gmailPass
	calendar.ProgrammaticLogin()
	
gCal = gdata.calendar.service.CalendarService()
googleCalendarLogin(gCal)	

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
calendarReminders = []

def UpdateCalendarEvents(calendar, reminderList):
	#Thanks to http://julien.danjou.info/blog/2012/google-calendar-pynotify
	eventFeed = calendar.GetCalendarEventFeed()
	now = datetime.datetime.now()
	reminderList=[]
	for event in feed.entry:
		#Check status of event
		if event.event_status.calue != 'CONFIRMED':
			continue
		#Iterate through event dates (for recurring)
		for when in event.when:
			try:
				start_time = datetime.datetime.strptime(when.start_time.split(".")[0], "%Y-%m-%dT%H:%M:%S")
				end_time = datetime.datetime.strptime(when.end_time.split(".")[0], "%Y-%m-%dT%H:%M:%S")
			except ValueError: #All day events
				continue
			
			if end_time > now:
				#Check each reminder
				if reminder.method == "alert":
					reminderList = reminderList.append(start_time - datetime.timedelta(0, 60 * int(reminder.minutes)))
					
	reminderList.sort()

if storage.has_key('RSSurl'):
	RSSurl = storage['RSSurl']
else:
	paramNotFound('RSSurl') 

if storage.has_key('FBurl'):
	FBurl = storage['FBurl']
else:
	paramNotFound('FBurl') 

def facebook():
  global FBurl
  rawNotifs=urllib2.urlopen(FBurl)
  parsedNotifs=feedparser.parse(rawNotifs)
  
  return parsedNotifs.entries[0].title

def LatestRSSHeadline(url):
  rawNotifs=urllib2.urlopen(url)
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
lastRSS = LatestRSSHeadline(RSSurl)
UpdateCalendarEvents(calendarReminders)

output_line(str(calendarReminders[0]))

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
    
  RSSHeadline = LatestRSSHeadline(RSSurl)
  if RSSHeadline != lastRSS:
	  output_line('RSS update: ' + RSSHeadline)
	  lastRSS = RSSHeadline
    
  if datetime.datetime.now().minute % 15  == 0:
    output_line('The time is now ' + datetime.datetime.strftime(datetime.datetime.now(), '%H:%M'))
   
  lastUpdate = datetime.datetime.utcnow() 
  time.sleep(60)
