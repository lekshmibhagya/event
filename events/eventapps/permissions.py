from . models import *

def userPermissions(profile_obj,event_obj):
    if(profile_obj==event_obj.owner):
        return True
    else:
        return False
def profilePermissions(user_obj,profile_obj):
    if(user_obj==profile_obj.user):
        return True
    else:
        return False
def deletePermissions(profile_obj,event_obj):
    if(profile_obj==event_obj.owner):
        return True
    else:
        return False


           
    
    
    

    
    
    