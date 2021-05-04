# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid[:]
    def get_title(self):
        return self.title[:]
    def get_description(self):
        return self.description[:]
    def get_link(self):
        return self.link[:]
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
#evaluate method on a newsStory object and returns true if an alert should be generated
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    def get_phrase(self):
        return self.phrase
    def is_phrase_in(self, text):
        text = text.lower()
        phrase = self.get_phrase()
        # replace all punctuation with a space
        for i in string.punctuation:
            text = text.replace(i, " ")
        words_in_text = text.split()
        words_in_phrase = phrase.split()
        #I want to take the first word in phrase, then check it is in words_in_text
        counter = 0
        if words_in_phrase[0] in words_in_text:
            counter += 1
            index = words_in_text.index(words_in_phrase[0])
            for i in range(1,len(words_in_phrase)):
                if index + i >= len(words_in_text):
                    return False
                if words_in_phrase[i] == words_in_text[index + i]:
                    counter += 1
        return counter == len(words_in_phrase)

                    
        #Get the index of the words_in_text
        #Check if the same words in words_in_phrase follow in words_in_text
        # return true if they do
               
    

# Problem 3
# TODO: TitleTrigger
class TitleTrigger (PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger (PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    #Date is a string in format: 3 Oct 2016 17:00:10
    def __init__(self, date):
        date = datetime.strptime(date, "%d %b %Y %H:%M:%S")
        self.date = date.replace(tzinfo=pytz.UTC)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        # pubdate = pytz.utc.localize(story.get_pubdate())
        pubdate = story.get_pubdate()
        pubdate = pubdate.replace(tzinfo=pytz.UTC)
        return pubdate < self.date
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        pubdate=pubdate.replace(tzinfo=pytz.UTC)
        return pubdate > self.date
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger2.evaluate(story) and self.trigger1.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger2.evaluate(story) or self.trigger1.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    relevant_stories = []
    for i in stories:
        for j in triggerlist:
            if j.evaluate(i):
                relevant_stories.append(i)
    return relevant_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_list = []
    trigger_dictionary = {}
    for i in lines:
        if i.startswith("ADD", 0, 3):
            next_index = 0
            #Repeat for every comma, taking the first index from the nth comma
            while i.find(",", next_index) != -1:
                #get the first index of the comma
                index = i.find(",", next_index)
                #get the second index comma
                next_index = i.find(",", index + 1)
                #For last value (so don't miss out the last letter)
                if next_index == -1:
                    trigger_list.append(trigger_dictionary[i[index + 1:]])
                else:
                    #get value inbetween indexes and add the corresponding value from the dictionary to the trigger_list
                    trigger_list.append(trigger_dictionary[i[index + 1:next_index]])      
        else: 
            index = i.find(",")
            next_index = i.find(",",index + 1)
            last_index = i.find(",",next_index + 1)
            trigger_type = i[index + 1:next_index] 
            if trigger_type == "TITLE":
                trigger_dictionary[i[:index]] = TitleTrigger(i[next_index + 1:])
            elif trigger_type == "DESCRIPTION":
                trigger_dictionary[i[:index]] = DescriptionTrigger(i[next_index + 1:])
            elif trigger_type == "AFTER":
                trigger_dictionary[i[:index]] = AfterTrigger(i[next_index + 1:])
            elif trigger_type == "BEFORE":
                trigger_dictionary[i[:index]] = BeforeTrigger(i[next_index + 1:])
            elif trigger_type == "NOT":
                trigger_dictionary[i[:index]] = NotTrigger(trigger_dictionary[i[index:next_index]])
            elif trigger_type == "AND":
                trigger_dictionary[i[:index]] = AndTrigger(trigger_dictionary[i[next_index +1:last_index]],trigger_dictionary[i[last_index + 1:]])
            elif trigger_type == "OR":
                trigger_dictionary[i[:index]] = OrTrigger(trigger_dictionary[i[next_index +1:last_index]],trigger_dictionary[i[last_index + 1:]])
    # print(lines) # for now, print it so you see what it contains!
    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("covid")
        t2 = DescriptionTrigger("Boris")
        t3 = DescriptionTrigger("lockdown")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

