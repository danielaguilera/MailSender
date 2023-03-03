import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_log_file(receivers : str, result : bool):
    file = open("info.log", 'w')
    for receiver in receivers.split(','):
        file.write(f"resultado-envio={result} to {receiver} \n")
    file.close()

def read_conf_file(filename : str):
    file = open(filename, 'r')
    receivers, mail_subject, mail_content = file.readline().strip().split(',')
    file.close()
    receivers = receivers[0:len(receivers)-1].replace(';', ',')
    return (receivers, mail_subject, mail_content)

def read_credentials_file(filename : str):
    file = open(filename, 'r')
    sender_address, sender_pass = file.readline().strip().split(',')
    file.close()
    return (sender_address, sender_pass)

if __name__ == '__main__':
    receivers, mail_subject, mail_content = read_conf_file('conf_tx_transito.txt')
    try:
        sender_address, sender_pass = read_credentials_file('credentials.txt')
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receivers
        message['Subject'] = mail_subject #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.send_message(message)
        session.quit()
        generate_log_file(receivers=receivers, result=True)
        print('Mail sent succesfully')
    except Exception:
        generate_log_file(receivers=receivers, result=False)
        print('Mail failed to send')
    
        



