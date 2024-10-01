#Schemata
import datetime
import subprocess
import json
import os
import argparse

# =========================================================================
# Support functions
# =========================================================================

# run rofi with provided data and extra commands
def runRofi(items, extraFlags=[],sendExitCode=False):
    rofiCommand = ['rofi', '-dmenu','-markup-rows','-regex','-tokenize','-i','-window-title','Schemata', '-theme', conf['theme']]
    if len(extraFlags):  
        rofiCommand.extend(extraFlags)
    rofiProcess = subprocess.run(rofiCommand, input=items.encode('utf-8'), capture_output=True)
    item = rofiProcess.stdout.decode('utf-8').strip()
    if sendExitCode:
        exitcode = rofiProcess.returncode
        return item, exitcode
    return item

# Make string to display task data in Edit-mode
def showEventData(idx):
    event = eventlist['upcoming'][idx];
    msg = ""
    keys = ["title","date","starttime","endtime","highpriority","reminders","created","place","url","comment"]
    for key in keys:
        if key in event:
            if key== "highpriority": 
                val = "Yes" if event['highpriority']==1 else "No"
            elif key == "reminders":
                if len(event[key])>1:
                    val = "\n"+"\n".join(sorted(event[key].values()))
                else:
                    val = list(event[key].values())[0]
            else: 
                val = event[key]
            if key in ['title','date','starttime','url','reminders'] or (key=='highpriority' and val=='Yes'):
                msg += key.capitalize() + ': <span color="' + accentColor + '">' + val + '</span>\n'
            else:
                msg += key.capitalize() + ': ' + val + '\n'

    msg = msg.strip()
    return msg

# =========================================================================
# Reminder functions
# =========================================================================

# Add reminder
def addReminder(idx):
    # Create lists for dates and times for Rofi
    startdate = eventlist['upcoming'][idx]['date']
    starttime = eventlist['upcoming'][idx]['starttime']
    dateObject = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    timeObject = datetime.datetime.strptime(starttime, '%H:%M')
    dates = []
    times = []

    for _ in range(24):
        if dateObject.date() >= datetime.datetime.today().date():
            dates.append(dateObject.strftime('%Y-%m-%d'))
        times.append(timeObject.strftime('%H:%M'))

        dateObject -= datetime.timedelta(days=1)
        timeObject -= datetime.timedelta(hours=1)

    remDate = runRofi("\n".join(dates), ['-p','Reminder date:'])
    remTime = runRofi("\n".join(times), ['-p','Reminder time:'])
    remDateTime = remTime+" "+remDate
    # Craft the reminder message
    response = createReminder(idx,remDateTime)
    if response is not False:
        storeReminder(idx,response,remDateTime)
    
def createReminder(idx,remDateTime):
    title = eventlist['upcoming'][idx]['title']
    time = eventlist['upcoming'][idx]['date']+" "+eventlist['upcoming'][idx]['starttime']
    notify = 'echo "notify-send -app Schemata \'' +title+'\' \''+ time +'\'"'
    if eventlist['upcoming'][idx]['highpriority'] == 1:
        notify += '-u critical'
    at = 'at ' + remDateTime
    command = notify + " | " + at
    proc = subprocess.run(command, shell=True, capture_output=True, text=True)
    response = proc.stderr
    exitcode = proc.returncode
    if exitcode==0: # Successful
        return response
    print(response)
    return False

def storeReminder(idx, response, remDateTime):
    response = response.splitlines()
    jobno = response[-1].split(" ")[1]
    remDateTimeList = remDateTime.split(" ")
    remDateTime = remDateTimeList[1]+" "+remDateTimeList[0]
    if "reminders" not in eventlist['upcoming'][idx]:
        eventlist['upcoming'][idx]['reminders'] = {}
    eventlist['upcoming'][idx]['reminders'][jobno] = remDateTime

# Remove reminder
def removeReminder(idx):
    rem = eventlist['upcoming'][idx]['reminders']
    if len(rem) == 1:
        jobno = list(rem.keys()).pop()
        del eventlist['upcoming'][idx]['reminders']
    else:
        joblist = list(rem.keys())
        rofistring = "\n".join(rem.values())
        remindex = runRofi(rofistring.strip(), ['-format','i','-p','Remove reminder','-only-match'])
        jobno = joblist[int(remindex)]
        del eventlist['upcoming'][idx]['reminders'][jobno]
    os.system('atrm '+jobno)
    return 

def updateReminders(idx):
    event = eventlist['upcoming'][idx]
    reminders = event['reminders']
    del eventlist['upcoming'][idx]['reminders']
    for jobno, remDateTime in reminders.items():
        remDateTimeList = remDateTime.split(" ")
        remDateTime = remDateTimeList[1]+" "+remDateTimeList[0]
        response = createReminder(idx,remDateTime)
        if response is not False:
            os.system('atrm '+jobno)
            storeReminder(idx,response,remDateTime)
        else: print(response, remDateTime)

# =========================================================================
# Initiating scripts
# =========================================================================

# Read config file and return parameters
def readConf():
    filename = os.path.realpath(__file__)[:-11]+"config.json"
    print(filename)
    f = open(filename,'r')
    conf = json.load(f)
    return conf

# Read file with tasks
def readData(filename="schemata.json"):
    file = filename
    f = open(file,'r')
    data = json.load(f)['events']
    return data

# Make a list of all events
def makeEventLists(data):
    eventList = dict()
    eventList['upcoming'] = []
    eventList['finished'] = []
    # eventList['recurring'] = []
    for event in data:
        if event['date']+" "+ event['starttime'] > datetime.datetime.today().strftime('%Y-%m-%d %H:%M'):
            status = "upcoming"
        else:
            status = "finished"
        eventList[status].append(event)
    eventList['upcoming'] = sorted(eventList['upcoming'], key=lambda k: "%s %s %s %s" % (k['date'], k['starttime'], abs(k['highpriority']-1), k['title'])) 
    eventList['finished'] = sorted(eventList['finished'], key=lambda k: "%s %s %s" % (k['date'], k['starttime'], k['title']), reverse=True) 
    return eventList

# Stringify provided list of events
def makeEvents(eventlist,eventtype="upcoming"):
    data = []
    events = []
    prio=""
    icons=""
    if eventtype=='upcoming':
        for item in eventlist:
            dt = item['date']+" "+item['starttime']
            if item['endtime']  != '':
                dt+="-"+item['endtime']
            prio = "[!] " if item['highpriority']==1 else "    "
            prio += '[\uf0f3]' if "reminders" in item and len(item['reminders'])>0 else ""
            prio += "[L]" if item['url']!="" else ""
            data.append([prio,dt,item['title'],item['comment']])
    elif eventtype=='finished':
        for item in eventlist:
            dt = item['date']+" "+item['starttime']+"-"+item['endtime']
            data.append([dt,item['title']])

    # make left justified columns based on longest item in column
    widths = [max(map(len, col)) for col in zip(*data)]
    for item in data:
        events.append("  ".join((val.ljust(width+1) for val, width in zip(item, widths))))

    return events


# =========================================================================
# Manage tasks
# =========================================================================

def addEvent():
    created = datetime.datetime.today().strftime('%Y-%m-%d')
    if (title := runRofi('', ['-p','Title*'])) == "":
        return
    if (priority := runRofi("No\nYes", ['-p','High priority*','-format','i'])) =="":
        return
    current_date = datetime.datetime.now().date()
    dates=[]
    for x in range(10):
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += datetime.timedelta(days=1)
    dates = "\n".join(dates)
    if (date := runRofi(dates.strip(), ['-p','Date'])) == "":
        return 
    starttime = runRofi('', ['-p','Start time [HH:MM]'])
    endtime = runRofi('', ['-p','End time [HH:MM]'])
    place = runRofi('', ['-p','Place'])
    url = runRofi('', ['-p','URL'])
    comment = runRofi('', ['-p','Additional information'])
    newEvent = dict(title = title, created = created, date = date, starttime = starttime, endtime = endtime, highpriority = int(priority), comment = comment,place = place, url = url)
    eventlist['upcoming'].append(newEvent)
    renewEventlists(True, False)

def editEvent(idx):
    event = eventlist['upcoming'][idx]
    if (title := runRofi('', ['-p','Title*','-filter',event['title']])) == "":
        return
    if (priority := runRofi("No\nYes", ['-p','High priority*','-format','i'])) =="":
        return
    current_date = datetime.datetime.now().date()
    dates=[]
    for x in range(30):
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += datetime.timedelta(days=1)
    dates = "\n".join(dates)
    if (date := runRofi(dates.strip(), ['-p','Date'])) == "":
        return 
    starttime = runRofi('', ['-p','Start time [HH:MM]','-filter',event['starttime']])
    endtime = runRofi('', ['-p','End time [HH:MM]','-filter',event['endtime']])
    place = runRofi('', ['-p','Place','-filter',event['place']])
    url = runRofi('', ['-p','URL','-filter',event['url']])
    comment = runRofi('', ['-p','Additional information','-filter',event['comment']])
    eventlist['upcoming'][idx]['title'] = title
    eventlist['upcoming'][idx]['highpriority'] = int(priority)
    eventlist['upcoming'][idx]['date'] = date
    eventlist['upcoming'][idx]['starttime'] = starttime
    eventlist['upcoming'][idx]['endtime'] = endtime
    eventlist['upcoming'][idx]['place'] = place
    eventlist['upcoming'][idx]['url'] = url
    eventlist['upcoming'][idx]['comment'] = comment
    if "reminders" in event and len(event['reminders'])>0:
        updateReminders(idx)

def togglePriority(idx):
    eventlist['upcoming'][idx]['highpriority'] = abs(int(eventlist['upcoming'][idx]['highpriority'])-1)
    renewEventlists(True, False)

def deleteEvent(idx):
    ans = runRofi('Yes\nNo',['-mesg','Do you want to delete this event?'])
    if ans=='Yes':
        del eventlist['upcoming'][idx]
        renewEventlists(True, False)
        return True
    return False

def gotoUrl(url):
    subprocess.Popen(['firefox', '-new-tab',url])
# =========================================================================
# Manage lists
# =========================================================================

def renewEventlists(renewUpcoming=True, renewFinished=False):
    global eventlist
    if renewUpcoming:
        eventlist['upcoming'] = sorted(eventlist['upcoming'], key=lambda k: "%s %s %s %s" % (k['date'], k['starttime'], k['highpriority'], k['title'])) 
    if renewFinished:
        eventlist['finished'] = sorted(eventlist['finished'], key=lambda k: "%s %s %s" % (k['date'], k['starttime'], k['title']), reverse=True)        
    
def updateJson(filename="schemata.json"):
    file = filename
    data = eventlist['upcoming'] + eventlist['finished']
    myDict = {'events': data}
    json_data = json.dumps(myDict, indent=4)
    with open(file,"w") as f:
        f.write(json_data)

# =========================================================================
# Main menus
# =========================================================================
def menuUpcoming():
    events = makeEvents(eventlist['upcoming'])
    rofistring = '<span color="' + accentColor + '">[\uea60] Add new event</span>\n'
    rofistring += "\n".join(events)
    msg = '<span color="' + accentColor + '">[Alt+Space]</span> Go to URL - '
    msg +='<span color="' + accentColor + '">[Alt+P]</span> Toggle priority - '
    msg +='<span color="' + accentColor + '">[Alt+D]</span> Show past events'
    idx, exitcode = runRofi(rofistring, ['-format','i','-p','Schemata ('+str(len(events))+')','-mesg',msg,'-kb-custom-1','Alt+space','-kb-custom-2','Alt+d','-kb-custom-3','Alt+p','-kb-custom-4','Ctrl+s'], True)
    if exitcode==10:     # Alt+Space
        gotoUrl(eventlist['upcoming'][int(idx)-1]['url']);
    elif exitcode==11:   #Alt+D
        ans = menuFinished()
        return ans
    elif exitcode ==12: #Alt+P
        togglePriority(int(idx)-1)
    elif exitcode == 13: # Ctrl+S
        updateJson(taskfile)
    else:
        if idx=='':
            return False
        elif int(idx) == 0:
            addEvent()
        else:
            editMenu(int(idx)-1)
    return True

# Menu when on Finished view
def menuFinished():
    events = makeEvents(eventlist['finished'], 'finished')
    rofistring = '<span color="' + accentColor + '">\uf053Back to upcoming events</span>\n'
    rofistring += "\n".join(events)
    msg = '<span color="' + accentColor + '">'+str(len(events))+'</span> Events - '
    #msg += '<span color="' + accentColor + '">[Alt+Space]</span> Send to To-Do list - '
    msg +='<span color="' + accentColor + '">[Alt+D]</span> Upcoming events'
    idx, exitcode = runRofi(rofistring, ['-format','i','-p','Past events','-kb-custom-1','Alt+space','-kb-custom-2','Alt+d', '-mesg',msg], True)
    if exitcode==10:
        changeDate(str(datetime.datetime.now() + datetime.timedelta(days=1)),int(idx)-1)
        menuFinished()
    elif exitcode==11:
        return True
    elif idx=='':
        return False
    return True

# Menu for editing chosen task in todo-list
def editMenu(idx):
    editChoice=0
    event = eventlist['upcoming'][idx];
    while editChoice != "":
        msg = showEventData(idx)
        if "reminders" in event and len(event['reminders'])>0:
            choices = '\uf053  Return\n1. Toggle priority\n2. Edit event\n3. Add reminder\n4. Remove reminder\n5. Delete event'
        else:    
            choices = '\uf053  Return\n1. Toggle priority\n2. Edit event\n3. Add reminder\n4. Delete event'
        editChoice = runRofi(choices, ['-mesg',msg,'-p','Event'])

        if editChoice == '1. Toggle priority': 
            togglePriority(idx)
        elif editChoice == '2. Edit event': editEvent(idx)
        elif editChoice == '3. Add reminder': addReminder(idx)
        elif editChoice == '4. Remove reminder': removeReminder(idx)
        elif editChoice == '5. Delete event' or editChoice == '4. Delete event': 
            if deleteEvent(idx):
                break
        else: editChoice=""

# =========================================================================
# Run program
# =========================================================================
def main():
    ans = True
    while ans: 
        ans = menuUpcoming()
    updateJson(datafile)

if __name__ == "__main__":
    conf = readConf()
    accentColor = conf['accent']
    datafile = conf['datafile']
    #if 'taskfiles' in conf and len(conf['taskfiles'])>1:
    data = readData(datafile)
    eventlist = makeEventLists(data)
    main()