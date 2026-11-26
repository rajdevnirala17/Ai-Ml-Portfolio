locations=["phagwara","jalandhar","ludhiyana","delhi"]

goal=input("enter destination: ")

print("ai is serching for the  destination...")

found = False 

for location in locations:
    print("checking: ",location)

    if location == goal:
        found = True
        break

if found:
    print("ai result:destination found:",goal)

else:
    print("ai result:destination not found:",goal)