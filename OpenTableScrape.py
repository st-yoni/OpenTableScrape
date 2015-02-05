from bs4 import BeautifulSoup
from urllib2 import urlopen
import smtplib
import sys

BASE_URL = "http://www.opentable.com/"
GMAIL_ACCOUNT = "" #gmail account of the sender
GMAIL_PASSWORD = "" #password of the sender


def get_status(ConvertedURL):
    html = urlopen(ConvertedURL).read()
    soup = BeautifulSoup(html, "lxml")
    avail = soup.find("ul", "dtp-results-times list-left")
    availTimes = []
    if avail == None:
    	return []
    for x in avail.findAll("li"):
    	if len(x.a["class"])==2:
    		availTimes.append(x.a["data-datetime"])
    return availTimes

def convert_time(Time):
	converted_time_results = []
	converted_time_results.append("20" + Time[0]+Time[1])
	converted_time_results.append("3A" + Time[3]+Time[4])
	return converted_time_results

def convert_URL(DateTime,Covers,ConvertedTime,RestName):
	return BASE_URL+ RestName+"?DateTime="+DateTime+"%"+ConvertedTime[0]+"%"+ConvertedTime[1]+"&Covers="+Covers


def send_email(availTimes, ConvertedURL, RestName):
            gmail_user = GMAIL_ACCOUNT
            gmail_pwd = GMAIL_PASSWORD
            FROM = 'The Open Table bot'
            TO = [''] #must be a list
            SUBJECT = "I Found a Table at %s" %RestName + "!"
            tempText =""
            for x in availTimes:
                tempText = tempText + "%s" %x + "\n"
            TEXT = "Hi, I managed to find a table at: \n"  + tempText + "Book it here: %s" %ConvertedURL

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"

def convert_rest_name(RestName):
    RestName = RestName.lower()
    RestName = RestName.replace(" ","-")    
    return RestName

if __name__ == "__main__":
    argNum = len(sys.argv) #OpenTableScrape.py <Rest Name> <Date> <Time> <Party Size>
    if argNum==2: #only new rest
        RestName = str(sys.argv[1])
        DateTime = "2015-02-23"
        Covers = "2"
        Time = "20:00"
    elif argNum == 3: #only new rest and date
        RestName = str(sys.argv[1])
        DateTime = str(sys.argv[2])
        Time = "20:00"
        Covers = "2"
    elif argNum == 4: #only new rest, date and time
        RestName = str(sys.argv[1])
        DateTime = str(sys.argv[2])
        Time = str(sys.argv[3])
        Covers = "2"
    elif argNum ==5: #all new
        RestName = str(sys.argv[1])
        DateTime = str(sys.argv[2])
        Time = str(sys.argv[3])
        Covers = str(sys.argv[4])
    else:  #all old
        RestName = "Eleven Madison Park"
        DateTime = "2015-02-23"
        Covers = "2"
        Time = "20:00"
    ConvertedRestName = convert_rest_name(RestName)
    ConvertedTime = convert_time(Time)
    ConvertedURL = convert_URL(DateTime,Covers,ConvertedTime,ConvertedRestName)
    availTimes = get_status(ConvertedURL)
    if availTimes == []:
        print "Sorry, no availablity"
    else:
        send_email(availTimes,ConvertedURL,RestName)
        print "yes!"
    sys.exit