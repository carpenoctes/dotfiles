import os

def e(command): 
    return os.popen(command).read()[:-1]

def makeDictionaries():
    commands=[]
    #path=os.getcwd()+str(loc)+"\keybindings_data.txt"
    filedir =os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(filedir, 'keybindings_data.txt')
    file1 = open(filename, 'r')

    Lines = file1.readlines()
      
    count = -1
    # Strips the newline character
    for line in Lines:
        line=line.strip()
        if(line[:3]=='App'):
            appname=line[4:]
            count+=1
            commands.append({'display':appname, 'command':[]})
            commands[count]['command'].append({'display':'Back', 'command':'back'})
            
        else:
            commands[count]['command'].append({'display':line, 'command':''})
    # for i in range(len(commands)):
    #     for j in range(len(commands[i])):
    #         print(commands[i][j])
    #     print()
    return commands

def menu(commands, prev_list=[], prompt = 'Search'):
    command_names = []
    command_actions = []

    for command in commands:
        command_names.append(command['display'])
        command_actions.append(command['command'])
    c = 'echo "{}" | rofi -dmenu -format i -theme waybarlike -i -p "{}"'.format("\n".join(command_names), prompt)

    index = e(c)

    if index != '':
        index = int(index)
        action = command_actions[index]            
        if type(action) == list:
            menu(action,commands, command_names[index])
        elif action=='back':
            menu(prev_list,commands)
        else:
            os.system(action)

commands = makeDictionaries()
menu(commands)