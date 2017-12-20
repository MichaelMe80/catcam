
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
 
def mailphoto(USER, PASSWORD):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(USER, PASSWORD)

  msg = MIMEMultipart()
  msg['Subject'] = 'Katzenalarm'
  msg['From'] = 'michael.messingschlager@googlemail.com'
  msg['To'] = 'm.messingschlager@me.com'
  msg.preamble = 'Katze mag rein'

  fp = open('/home/pi/image.jpg', 'rb')
  img = MIMEImage(fp.read())
  msg.attach(img)

  server.send_message(msg)
  server.quit()
