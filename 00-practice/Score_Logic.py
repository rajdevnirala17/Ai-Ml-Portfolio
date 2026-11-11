
def Score(Attempt):
    if Attempt>=1 and Attempt <=2:
        return 100
    elif Attempt>=3 and Attempt <=4:
        return 75
    elif Attempt>=5 and Attempt <=6:
        return 50
    elif Attempt == 7:
        return 25
    else:
        return "Better Luck! Next Time"