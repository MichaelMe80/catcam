
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
 
def mailphoto(MAILFROMADDRESS, MAILFROMPASS, MAILTOADDRESS):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(MAILFROMADDRESS, MAILFROMPASS)

  msg = MIMEMultipart()
  msg['Subject'] = 'Katzenalarm'
  msg['From'] = MAILFROMADDRESS
  msg['To'] = MAILTOADDRESS
  msg.preamble = 'Katze mag rein'

  fp = open('/home/pi/image.jpg', 'rb')
  img = MIMEImage(fp.read())
  msg.attach(img)

  server.send_message(msg)
  server.quit()
