import random
import Score_Logic as SL
import Game_logic as GL
print("Welcome to the Game of Guessing let's see how lucky! you are :)")
random_num = random.randint(2,100) #generating random number
print(random_num)
Attempt = 0 
for i in range(1,8):
    a = int(input("Enter your Guess upto 100 or Enter 1 to Exit :"))
    if a == 1:
        print("Thankyou for Choosing Our Game")
        break
    G1 = GL.Guess(a,random_num)
    if G1 == 1:
        Attempt += 1
        print("'correct' Your number is: ",a)
        print("Your Attempts are : ",Attempt)
        S1 = SL.Score(Attempt)
        break
                #S1 = SL.Score(Attempt)
    elif G1 == 2:
        Attempt += 1
        print("Too high")
        print("Guess Remaining ",7-i)
        
    else: 
        Attempt+= 1
        print("Too low")
        print("Guess Remaining ",7-i)
        
if G1 == 1:
    print("Your Score is :",S1)
else:
    print("Better luck! next time")
    print("The secret number was ",random_num)
    