import inspect
class console:
    db = None
    conn = None
    @staticmethod
    def log(msg): 
    	stack = inspect.stack()
    	rFile = stack[1][1].split('/')[-1]
    	print '(%s:%s::%s): %s' % (rFile, stack[1][2], stack[1][3], msg)
        return True
