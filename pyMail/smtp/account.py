from address import address
from pymail.database import database
class account:
    def __init__(self, addr):
        if !isinstance(addr, address):
            try:
                addr = address(addr)
            except e:
                raise e
        
    
