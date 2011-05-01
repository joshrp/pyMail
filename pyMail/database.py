from pymongo import Connection
class database:
    db = None
    conn = None
    @staticmethod
    def instance(): 
        s = database
        if s.conn is None or s.db is None:
            s.conn = Connection()
            s.db = s.conn.pymail
            
        return s.db