import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from cryptography.fernet import Fernet

def load_key() -> bytes:

    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    return key

def decrypt_message(file) -> str:

    # Load the key from a file
    encryption_key = load_key()

    # Create a Fernet object with the key
    f = Fernet(encryption_key)

    # Read the encrypted message from a file
    with open(file, "rb") as encrypted_file:
        encrypted_message = encrypted_file.read()

    # Decrypt the message
    decrypted_message = f.decrypt(encrypted_message)

    # Return the decrypted message as a string
    return decrypted_message.decode()

def send_mail(status: dict) -> bool:

    # Set up email credentials
    email = "jr_developer2@mazenetsolution.com"
    to_email = "ashokraj@mazenetsolution.com" # My testing mail - "vishnupouleymz@gmail.com"

    # Decrypt the password
    password = decrypt_message(file="password.txt") # Change the file name if changed

    # Create an SMTP_SSL object with the Gmail SMTP server and port number
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Establish a connection with the server
    server.ehlo()

    # Log in to the email account using the provided email and decrypted password
    server.login(email, password)

    # Create a MIMEMultipart object for composing the email
    msg = MIMEMultipart()

    # Set the sender's email address
    msg["From"] = "Database Backup Automation Service"

    # Set the recipient's email address
    msg["To"] = to_email

    # Get the current date and time and format it
    currentDT = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Set the subject of the email
    msg["Subject"] = "Download Backup Status - " + currentDT

    body = ""

    for key, value in status.items():
        # Create the body of the email
        if value[0] == True:
            body += f'Database "{key}" Backup Download was Success\n\n'

        elif value[0] == False:
            if key:
                body += f'Database "{key}" Backup Download was Failed\nError: {value[1]}\n\n'
            else:
                body = f'Database Backup Download was Failed\nError: {value[1]}\n\n'

    # Attach the body to the email
    msg.attach(MIMEText(body, "plain"))

    # Convert the MIMEMultipart object to a string
    mail = msg.as_string()

    try:
        # Send the email
        server.sendmail(email, to_email, mail)

        print("Send Success")

        # Return True if the email is sent successfully
        return True

    except Exception as e:
        # Print the error message if an error occurs while sending the email
        print("Error occurred while sending email: ", str(e))
        return False