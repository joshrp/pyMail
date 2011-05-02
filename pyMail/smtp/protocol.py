from twisted.protocols import basic
from twisted.internet import protocol
from message import messageTransport
from address import Address

class SMTPProtocol(basic.LineOnlyReceiver):    
    
    def connectionMade(self):
        self.fulldata = []
        self._body = []
        self.mode = 'COMMAND'
        print 'Connection Received from: %s on Port %s' % (self.transport.getPeer().host, self.transport.getPeer().port)
        
        self.transport.write('220 mail.dev.com ESMTP pyMail\n')
        #self.transport.loseConnection()
    
    def lineReceived(self, line):
        self.fulldata.append(line)  
        print 'C: ' + line
        func = getattr(self, 'state_%s' % (self.mode), None)
        func(line)
            
    def sendCode(self, code, message):
        resp = '%s - %s' % (code, message)
        self.transport.write(resp)
        print 'S: : %s' % (resp)
        
    def state_COMMAND(self, command):
        """Called when awaiting new command form client"""
        splits = command.split(None)
        method = getattr(self, 'do_' + splits[0].upper(), None)
        if method is not None:
            method(splits[1:])
        else:
            self.sendCode(500, 'Command Not Implemented')
            
    def do_EHLO(self, args):
        self.helo = ' '.join(args)
        self.sendCode(250, '%s - %s \n' % (self.settings['welcome'], ' '.join(args))) 
        
    def do_QUIT(self, args):
        self.sendCode(221, "Goodbye!!\n\n")
        self.transport.loseConnection()       
    
    def do_MAIL(self, args):        
        splits = args[0].split(':')        
        if (splits[0] == 'FROM'):
            """TODO:: Mail from check"""
            self._from = Address(splits[1])
        print type(str(self._from))
        self.sendCode(250, 'Ok Sending as from %s \n' % (self._from))
    
    def do_RCPT(self, args):
        splits = args[0].split(':')
        if ( splits[0] == 'TO' ):
            """TODO::check rcpt agaist domains and whatnot"""
            self._to =  Address(splits[1]) 
        self.sendCode(250, 'Ok %s Added to Receipient list \n' % (self._to))
        
    
    def do_DATA(self, args):
        if self._from is not None and self._to is not None:
            self.mode = 'DATA'
            self.message = messageTransport(self._from, self._to, self.helo)
            self.sendCode(354, 'End data with <CR><LF>.<CR><LF>\n')
        else:
            self.sendCode(503, 'Need to have Valid MAIL FROM and RCPT TO')
            
    def state_DATA(self, data):
        """Called on new lines when in DATA mode"""
        if data == '.':
            self.mode = 'COMMAND'
            self.sendCode(250, " OK Queued as some message I'll neer deliver :)\n")
            self.queue.add(self.message)
            return
        """remove buffed periods"""        
        if( len(data) > 0 and data[0] == '.' ): 
            data = data[1:]
        
        self.message.addLine(data)

        
class factory(protocol.ServerFactory):
    protocol = SMTPProtocol
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
    
