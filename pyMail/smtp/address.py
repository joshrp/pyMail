
class Address:
    def __init__(self, addr):
        self.fullAddress = addr
    
    def isValidEmail(self):
        return True
     
    def __str__(self):
        return self.fullAddress    
