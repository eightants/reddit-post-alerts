channelid = 0
subs = []
keywords = []

with open("./post-alert-bot/config.txt", "r") as rfile: 
    content = rfile.readlines()
    counter = 0
    for line in content:
        if line[0] != '#':
            if counter == 0:
                channelid = int(line)
                counter += 1
            elif counter == 1:
                subs = line.strip("\n").split(',')
                counter += 1
            elif counter == 2:
                keywords = line.lower().strip("\n").split(',')

print(channelid)
print(subs)
print(keywords)
    
