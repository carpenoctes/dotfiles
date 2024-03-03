import subprocess
import os

def addReminder():

    command1 = 'notify-send -app Schemata "Träffa Aces" "2023-07-17 15:30\nJust a friendly reminder"' 
    command2 ='at 23:00'
    #comm1 = ['notify-send','"Traffa Ace"']
    comm1 = ['echo', '"notify-send \'Traffa Ace\'"']

    comm2 = ['at now + 1 min']
    comm = comm1+["|"]+comm2
    command = command1+" | "+command2
    command = 'echo "notify-send -app Schemata \'Träffa Aces\' \'2023-07-17 15:30\nJust a friendly reminder\'" | '+command2

    #response = subprocess.getoutput(command)
    #response = os.system(command)
    proc = subprocess.run(command, shell=True, capture_output=True, text=True)
    #resp = proc.communicate()
    response = proc.stderr
    exitcode = proc.returncode
    #return "\n".split(proc)
    return response, exitcode
response,exitcode  = addReminder()
# if ecitcode != None:
#     print("Exitcode: "+exitcode)
print(response.splitlines())
print("Exitcode: ",exitcode)

