
class DataValidator:

    @classmethod
    def isNotNull(self,val):
        if(val == None or val == "" ):
            return False
        else:    
            return True    

    @classmethod
    def isNull(self,val):
        if(val == None or val == "" ):
            return True
        else:    
            return False    

    @classmethod
    def isInt(self,val):
        if(val == 0 ):
            return False
        else:    
            return True  