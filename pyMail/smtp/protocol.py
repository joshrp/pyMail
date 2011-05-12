from twisted.protocols import basic
from twisted.internet import protocol
from message import messageTransport
from address import Address

class serverProtocol(basic.LineOnlyReceiver):    
    
    def connectionMade(self):
        self.fulldata = []
        self._body = []
        self.mode = 'COMMAND'
        print 'Connection Received from: %s on Port %s' % (self.transport.getPeer().host, self.transport.getPeer().port)
        
        self.sendCode(220, 'mail.dev.com ESMTP pyMail')
        #self.transport.loseConnection()
    
    def lineReceived(self, line):
        self.fulldata.append(line)  
        print 'C: ' + line
        func = getattr(self, 'state_%s' % (self.mode), None)
        func(line)
            
    def sendCode(self, code, message):
        resp = '%s - %s\n' % (code, message)
        self.transport.write(resp)
        print 'S: : %s' % (resp)
        
    def state_COMMAND(self, command):
        """Called when awaiting new command form client"""
        if command.strip() == '':
            self.consecutiveErrors = self.consecutiveErrors + 1;
            if self.consecutiveErrors == 10:
                self.sendCode(221, 'Too Many Consectutive Protocol Errors (Your talking shit, Go Away)')
                self.do_QUIT()
            return False;
        self.consecutiveErrors = 0
        splits = command.split(None)
        method = getattr(self, 'do_' + splits[0].upper(), None)
        if method is not None:
            method(splits[1:])
        else:
            self.sendCode(500, 'Command Not Implemented')
            
    def do_EHLO(self, args):
        self.helo = ' '.join(args)
        self.sendCode(250, '%s - %s' % (self.settings['welcome'], ' '.join(args))) 
        
    def do_QUIT(self, args):
        self.sendCode(221, "Goodbye!!")
        self.transport.loseConnection()       
    
    def do_MAIL(self, args):        
        splits = args[0].split(':')        
        if (splits[0].upper() == 'FROM'):
            """TODO:: Mail from check"""
            self._from = Address(splits[1])
        print type(str(self._from))
        self.sendCode(250, 'Ok Sending as from %s' % (self._from))
    
    def do_RCPT(self, args):
        splits = args[0].split(':')
        if ( splits[0] == 'TO' ):
            """TODO::check rcpt agaist domains and whatnot"""
            addr = Address(splits[1])
            valid, reason = addr.isValidEmail()
            if not valid:
                self.sendCode(500, 'Unnaccepted: Not a valid Address %s' % reason)
            else:
                self._to = addr 
                self.sendCode(250, 'Ok %s Added to Receipient list' % (self._to))
        
    
    def do_DATA(self, args):
        if self._from is not None and self._to is not None:
            self.mode = 'DATA'
            self.message = messageTransport(self._from, self._to, self.helo)
            self.sendCode(354, 'End data with <CR><LF>.<CR><LF>')
        else:
            self.sendCode(503, 'Need to have Valid MAIL FROM and RCPT TO')
            
    def state_DATA(self, data):
        """Called on new lines when in DATA mode"""
        if data == '.':
            self.mode = 'COMMAND'
            self.sendCode(250, " OK Queued as some message I'll neer deliver :)")
            self.queue.add(self.message)
            return
        """remove buffed periods"""        
        if( len(data) > 0 and data[0] == '.' ): 
            data = data[1:]
        
        self.message.addLine(data)

        
class serverFactory(protocol.ServerFactory):
    protocol = serverProtocol
    def __init__(self, settings, queue, portal=None):
        self.settings = settings
        self.portal = portal
        self.queue = queue
        
    def buildProtocol(self, addr):
        p = protocol.ServerFactory.buildProtocol(self, addr)
        p.settings = self.settings
        p.portal = self.portal
        p.queue = self.queue
        return p

class clientProtocol:
    def __init__(self):
        pass

class clientFactory:
    protocol = clientProtocol
