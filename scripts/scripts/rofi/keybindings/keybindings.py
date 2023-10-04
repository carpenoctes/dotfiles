import os
import subprocess
import json

def runRofi(items, prompt="Search"):
    rofiCommand = ['rofi', '-dmenu', '-format', 'i', '-i', '-theme','keybindings','-p', prompt]
    rofiProcess = subprocess.run(rofiCommand, input=items.encode('utf-8'), capture_output=True)
    item = rofiProcess.stdout.decode('utf-8').strip()
    return item

def makeDictionaries():
    commands=[]
    #path=os.getcwd()+str(loc)+"\keybindings_data.txt"
    filedir =os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(filedir, 'keybindings_data.json')
    with open(filename) as file:
        data = json.load(file)["apps"]
    i=0
    apps = []
    kb = []
    for item in data:
        apps.append(item['app'])
        keybindings = []
        for key, val in item['keybindings'].items():
            keybindings.append([key, val])
        kbString=[]
        widths = [max(map(len, col)) for col in zip(*keybindings)]
        for item in keybindings:
            kbString.append("  ".join((val.ljust(width+3) for val, width in zip(item, widths))))
        widths = [max(map(len, col)) for col in zip(*data)]
        kb.append(kbString)

    return apps, kb

def menu(apps, keybindings):
    rofistring = "\n".join(apps)
    idx = runRofi(rofistring)
    if idx != "":
        return kbmenu(keybindings[int(idx)])
    else:
        exit()
def kbmenu(keybindings):
    rofistring = "Back to main menu\n"
    rofistring += "\n".join(keybindings)
    idx = runRofi(rofistring)
    if idx == "0":
        return True
    return False

def main(apps, keybindings):
    ans = True
    while ans: 
        ans = menu(apps, keybindings)

apps, keybindings = makeDictionaries()

main(apps, keybindings)