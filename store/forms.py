def validate(amnt):
    if amnt != "" and int(amnt) > 0:
        return True
    else:
        return False
    
def validateRate(amnt):
    if amnt != "" and float(amnt) > 0:
        return True
    else:
        return False