from pyMail.smtp import protocol

mail = protocol.ESMTPSender()

print mail.send('mail.google.com')