from pymongo import Connection
class database:
    db = None
    conn = None
    @staticmethod
    def instance(): 
        s = database
        if s.conn is None or s.db is None:
            print 'I just recconected to the DB'
            s.conn = Connection()
            s.db = s.conn.pymail
            
        return s.db