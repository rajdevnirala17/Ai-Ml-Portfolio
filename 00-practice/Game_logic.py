
#--------------------------------------

def Guess(Player_guess,random_num):
    if Player_guess == random_num:
         #correct guess
        return 1
    elif Player_guess > random_num:
         # too high
        return 2
    elif Player_guess < random_num:
         # too low
        return 3

