#Todofi
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
    rofiCommand = ['rofi', '-dmenu', '-markup-rows','-regex','-tokenize','-i', '-theme', conf['theme']]
    if len(extraFlags):  
        rofiCommand.extend(extraFlags)
    rofiProcess = subprocess.run(rofiCommand, input=items.encode('utf-8'), capture_output=True)
    item = rofiProcess.stdout.decode('utf-8').strip()
    if sendExitCode:
        exitcode = rofiProcess.returncode
        return item, exitcode
    return item

# Make string to display task data in Edit-mode
def showTaskData(idx):
    task = tasklists['todo'][idx];
    msg = ""
    keys = ["caption","priority","created","deadline","group","tags","comment"]
    for key in keys:
        if key in task:
            if key== "priority": val = conf['priorities'][int(task['priority'])-1]
            else: val = task[key]
            if key in ['caption','priority','deadline']:
                msg += key.capitalize() + ': <span color="' + accentColor + '">' + val + '</span>\n'
            else:
                msg += key.capitalize() + ': ' + val + '\n'

    msg = msg.strip()
    return msg

# Calculate days between two days
def calcDays(startdate, enddate=datetime.datetime.today().strftime('%Y-%m-%d')):
    dateformat = "%Y-%m-%d"  # Specify the format of the dates
    startdatetime = datetime.datetime.strptime(startdate, dateformat)
    enddatetime = datetime.datetime.strptime(enddate, dateformat)
    timedifference = enddatetime - startdatetime
    return str(timedifference.days)

# =========================================================================
# Initiating scripts
# =========================================================================

# Read config file and return parameters
def readConf():
    filename = os.path.realpath(__file__)[:-9]+"config.json"
    f = open(filename,'r')
    conf = json.load(f)
    return conf

# Read file with tasks
def readData(filename="todofi.json"):
    file = conf['taskfileslocation']+filename
    f = open(file,'r')
    data = json.load(f)['tasks']
    return data

# Make three lists of tasks, depending on status (todo, completed and deferred)
def makeTaskLists(data):
    tasklists = dict()
    tasklists['todo'] = []
    tasklists['completed'] = []
    tasklists['deferred'] = []
    for task in data:
        tasklists[task['status']].append(task)
    tasklists['todo'] = sorted(tasklists['todo'], key=lambda k: "%s %s %s" % (k['priority'], k['group'], k['caption'])) 
    tasklists['completed'] = sorted(tasklists['completed'], key=lambda k: "%s %s %s" % (k['finished'], k['group'], k['caption'])) 
    tasklists['deferred'] = sorted(tasklists['deferred'], key=lambda k: "%s %s %s" % (k['deferred'], k['group'], k['caption'])) 
    return tasklists

# Collect all distinct groups and tags
def makeGroupsAndTags(data):
    groups = []
    tags = []
    for item in data:        
        if item['group'] not in groups:
            groups.append(item['group'])
        for tag in item['tags'].split(','):
            if tag.strip() not in tags:
                tags.append(tag.strip())
    groups.sort()
    tags.sort()
    return [groups, tags]

# Stringify provided list of tasks
def makeTasks(tasklist,tasktype="todo"):
    data = []
    tasks = []
    if tasktype=='todo':
        for item in tasklist:
            priority = conf['priorities'][int(item['priority'])-1]
            priority = priority+' [DL]' if priority[-4:] != '[DL]' and 'deadline' in item else priority
            data.append([priority,item['group'],calcDays(item['created']),item['caption'],item['tags']])
    elif tasktype=='completed':
        for item in tasklist:
            data.append([item['finished'],item['group'],item['caption'],item['tags'],calcDays(item['created'],item['finished'])+" days"])
    elif tasktype=='deferred':
        for item in tasklist:
            data.append([item['deferred'],item['group'],item['caption'],item['tags'],calcDays(item['created'],item['deferred'])+" days"])

    # make left justified columns based on longest item in column
    widths = [max(map(len, col)) for col in zip(*data)]
    for item in data:
        tasks.append("  ".join((val.ljust(width+1) for val, width in zip(item, widths))))

    return tasks


# =========================================================================
# Manage tasks
# =========================================================================

def addTask():
    created = datetime.datetime.today().strftime('%Y-%m-%d')
    if (caption := runRofi('', ['-p','Task caption*'])) == "":
        return
    prioList = "\n".join(conf['priorities'])
    if (priority := runRofi(prioList, ['-p','Priority*','-format','i'])) =="":
        return
    priority = str(int(priority)+1)
    if (group := runRofi("\n".join(allGroups), ['-p','Group* (start with +)'])) =="":
        return
    tags = runRofi("\n".join(allTags), ['-p','Tags (start with #)','-multi-select'])
    tags = tags.replace("\n",", ").strip()
    comment = runRofi('', ['-p','Additional information'])
    newTask = dict(caption = caption, comment = comment, created = created, group = group, priority = priority, status = "todo", tags = tags)
    tasklists['todo'].append(newTask)
    renewTasklists(True, False, False)

def editTask(idx):
    task = tasklists['todo'][idx]
    if (caption := runRofi('', ['-p','Caption','-filter',task['caption']])) == "":
        return
    if (group := runRofi("\n".join(allGroups), ['-p','Group','-filter',task['group']])) =="":
        return
    tags = runRofi("\n".join(allTags), ['-p','Tags','-filter',task['tags'],'-multi-select'])
    tags = tags.replace("\n",", ").strip()
    cmt = task['comment'] if "comment" in task else ""
    comment = runRofi('', ['-p','Comment','-filter',cmt])
    tasklists['todo'][idx]['caption'] = caption
    tasklists['todo'][idx]['group'] = group
    tasklists['todo'][idx]['tags'] = tags
    tasklists['todo'][idx]['comment'] = comment

def changeStatus(fromStatus, toStatus, idx):
    task = tasklists[fromStatus][idx]
    del tasklists[fromStatus][idx]
    if toStatus == 'todo':
        if 'finished' in task: del task['finished']
        if 'deferred' in task: del task['deferred']
    elif toStatus == 'completed':
        task['finished'] = datetime.datetime.today().strftime('%Y-%m-%d')
    elif toStatus == 'deferred':
        task['deferred'] = datetime.datetime.today().strftime('%Y-%m-%d')
    task['status'] = toStatus
    tasklists[toStatus].append(task)
    renewTasklists(True, True, True)

def changePriority(idx):
    prioList = "\n".join(conf['priorities'])
    if (priority := runRofi(prioList, ['-p','Priority*','-format','i'])) =="":
        return
    tasklists['todo'][idx]['priority'] = str(int(priority)+1)

def setPriority(idx, val):
    tasklists['todo'][idx]['priority'] = val
    renewTasklists(True, False, False)

def setDeadline(idx):
    current_date = datetime.datetime.now().date()
    if 'deadline' in tasklists['todo'][idx]:
        dates=["Remove deadline"]
    else:
        dates=[]
    for x in range(10):
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += datetime.timedelta(days=1)
    dates = "\n".join(dates)
    if (deadline := runRofi(dates.strip(), ['-p','Deadline'])) =="":
        return
    if deadline == 'Remove deadline':
        del tasklists['todo'][idx]['deadline']
    else:
        tasklists['todo'][idx]['deadline'] = deadline 

def deleteTask(idx):
    ans = runRofi('Yes\nNo',['-mesg','Do you want to delete this task?'])
    if ans=='Yes':
        del tasklists['todo'][idx]
        renewTasklists(True, False, False)
        return True
    return False

# =========================================================================
# Manage lists
# =========================================================================

def renewTasklists(renewTodo=True, renewCompleted=False, renewDeferred=False):
    global tasklists, allGroups, allTags
    if renewTodo:
        tasklists['todo'] = sorted(tasklists['todo'], key=lambda k: "%s %s %s" % (k['priority'], k['group'], k['caption']))        
    if renewCompleted:
        tasklists['completed'] = sorted(tasklists['completed'] , key=lambda k: "%s %s %s" % (k['finished'], k['group'], k['caption']))
    if renewDeferred:
        tasklists['deferred'] = sorted(tasklists['deferred'] , key=lambda k: "%s %s %s" % (k['deferred'], k['group'], k['caption']))

def updateJson(filename="todofi.json"):
    file = conf['taskfileslocation']+filename
    data = tasklists['todo'] + tasklists['completed'] +tasklists['deferred']
    myDict = {'tasks': data}
    json_data = json.dumps(myDict, indent=4)
    with open(file,"w") as f:
        f.write(json_data)

def cycleTaskfiles():
    global data, tasklists, allGroups, allTags, taskfile
    updateJson(taskfile)
    try:
        n = conf['taskfiles'].index(taskfile)
    except:
        n=0
    if totalTaskfiles > n+1:
        taskfile = conf['taskfiles'][n+1]
    else:
        taskfile = conf['taskfiles'][0]
    data = readData(taskfile)
    tasklists = makeTaskLists(data)
    [allGroups, allTags] = makeGroupsAndTags(data)
    return True


# =========================================================================
# Main menus
# =========================================================================
def menuTodoTasks():
    tasks = makeTasks(tasklists['todo'])
    rofistring = '<span color="' + accentColor + '">[\uea60] New task</span>\n'
    rofistring += "\n".join(tasks)
    msg = '<span color="' + accentColor + '">[Alt+Space]</span> Mark as done - '
    msg +='<span color="' + accentColor + '">[Alt+(1-6)]</span> Change priority - '
    msg +='<span color="' + accentColor + '">[Alt+D]</span> Show completed tasks - '
    if totalTaskfiles > 1:
        msg +='<span color="' + accentColor + '">[Alt+C]</span> Cycle taskfiles'
    idx, exitcode = runRofi(rofistring, ['-format','i','-p','Todofi ('+str(len(tasks))+')','-mesg',msg,'-kb-custom-1','Alt+space','-kb-custom-2','Alt+d','-kb-custom-3','Alt+1','-kb-custom-4','Alt+2','-kb-custom-5','Alt+3','-kb-custom-6','Alt+4','-kb-custom-7','Alt+5','-kb-custom-8','Alt+6','-kb-custom-9','Ctrl+s','-kb-custom-10','Alt+c'], True)
    if exitcode==10:
        changeStatus('todo','completed',int(idx)-1)
    elif exitcode==11:
        ans = menuOtherTasks('completed')
        return ans
    elif 12 <= exitcode <= 17:
        setPriority(int(idx)-1,exitcode-11)
    elif exitcode == 18: # Ctrl+S
        updateJson(taskfile)
    elif exitcode == 19: # Alt+C
        cycleTaskfiles()
    else:
        if idx=='':
            return False
        elif int(idx) == 0:
            addTask()
        else:
            editMenu(int(idx)-1)
    return True

# Menu when on Completed tasks view or Deferred tasks view
def menuOtherTasks(status):
    tasks = makeTasks(tasklists[status], status)
    switchto = 'completed' if status=='deferred' else 'deferred'

    rofistring = '<span color="' + accentColor + '">\uf053  Current tasks</span>\n'
    rofistring += "\n".join(tasks)
    msg = '<span color="' + accentColor + '">'+str(len(tasks))+'</span> Tasks - '
    msg += '<span color="' + accentColor + '">[Alt+Space]</span> Send to To-Do list - '
    msg +='<span color="' + accentColor + '">[Alt+D]</span> Show ' + switchto + ' tasks'
    idx, exitcode = runRofi(rofistring, ['-format','i','-p',status.capitalize()+' tasks','-kb-custom-1','Alt+space','-kb-custom-2','Alt+d', '-mesg',msg], True)
    if exitcode==10:
        changeStatus(status,'todo',int(idx)-1)
        menuOtherTasks(status)
    elif exitcode==11:
        ans = menuOtherTasks(switchto)
    elif idx=='':
        return False
    return True

# Menu for editing chosen task in todo-list
def editMenu(idx):
    editChoice=0
    task = tasklists['todo'][idx];
    while editChoice != "":
        msg = showTaskData(idx)
        if 'deadline' in task:
            choices = '\uf053  Return\n1. Mark as completed\n2. Change priority\n3. Change deadline\n4. Edit task\n5. Mark as deferred\n6. Delete task'
        else:
            choices = '\uf053  Return\n1. Mark as completed\n2. Change priority\n3. Set deadline\n4. Edit task\n5. Mark as deferred\n6. Delete task'
        editChoice = runRofi(choices, ['-mesg',msg,'-p','Edit task'])

        if editChoice == '1. Mark as completed': 
            changeStatus('todo','completed',idx)
            break
        elif editChoice == '2. Change priority': 
            changePriority(idx)
        elif editChoice == '3. Set deadline': setDeadline(idx)
        elif editChoice == '3. Change deadline': setDeadline(idx)
        elif editChoice == '4. Edit task': editTask(idx)
        elif editChoice == '5. Mark as deferred': 
            changeStatus('todo','deferred',idx)
            break
        elif editChoice == '6. Delete task': 
            if deleteTask(idx):
                break
        else: editChoice=""

# =========================================================================
# Run program
# =========================================================================
def main():
    ans = True
    while ans: 
        ans = menuTodoTasks()
    updateJson(taskfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', nargs='?', type=str)
    parser.add_argument('--n', nargs='?', type=int)
    args = parser.parse_args()
    conf = readConf()
    totalTaskfiles = len(conf['taskfiles'])
    accentColor = conf['accent']
    #if 'taskfiles' in conf and len(conf['taskfiles'])>1:

    if args.file and os.path.exists(conf['taskfileslocation']+args.file):
        taskfile = file
    elif args.n and totalTaskfiles>=args.n and os.path.exists(conf['taskfileslocation']+conf['taskfiles'][args.n-1]):
        taskfile = conf['taskfiles'][args.n-1]
    else:
        taskfile = "todofi.json"
    data = readData(taskfile)
    tasklists = makeTaskLists(data)
    [allGroups, allTags] = makeGroupsAndTags(data)
    main()