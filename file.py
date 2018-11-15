f = open("Twitter_Accounts","r")

if f.mode == "r":
    contents = f.read().splitlines()
    
for content in contents:
        print(content)
