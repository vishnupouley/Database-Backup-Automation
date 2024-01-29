# Instructions to utilize this automation tool

## Setup for this PLESK AUTOMATION

### **1. Make sure Python 3.11 and pip are installed using these commands**

*For python*

```bash
python --version
```

*For pip*

```bash
pip --version
```

if not installed you need to install Python 3.11 to download Python and pip

### **2. After that, download the necessary packages of Python 3.11**

```bash
pip install -r requirements.txt
```

### **3. Then make sure all of these support files are located in the same directory**

### **4. Add this data.exe to the task scheduler and make it run as per your preference**

## Edit the password for changing the Plesk account password

### 1. Go to the encrypt.py and fill in the file name and the password in this part

```python
if __name__ == "__main__":
    message = "" # Type the password to be encrypted
    filename = "" # Type the filename to save the encrypted message
    encrypt_message(message, filename)
```

### 2. Edit the file name in the data.py in this part

```python
    username = driver.find_element(By.NAME, 'login_name')
    password = driver.find_element(By.NAME, 'passwd')
    login_button = driver.find_element(By.XPATH, "//button[@name='send']")

    passwd = decrypt_message(file='passwd.txt') # Change the file name if changed

    username.send_keys('m******r')
    password.send_keys(passwd)
    # password.send_keys(Keys.RETURN)
    login_button.click()
```

## Edit the password for changing the mail account and its password

### 1. Go to the encrypt.py and fill in the file name and the password in this part

```python
if __name__ == "__main__":
    message = "" # Type the password to be encrypted
    filename = "" # Type the filename to save the encrypted message
    encrypt_message(message, filename)
```

### 2. Edit the file name in the send_mail.py as well as change the mail in this part

```python
    # Set up email credentials
    email = "from_mail@gmail.com"
    to_email = "to_mail@gmail.com" 

    # Decrypt the password
    password = decrypt_message(file="password.txt") # Change the file name if changed

    # Create an SMTP_SSL object with the Gmail SMTP server and port number
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
```

## Procedures after editing inside the code - Making it an executable file

### 1. Open the command prompt from where the python files are located

### 2. Run this command to make the executable file

```bash
pyinstaller --onefile data.py send_mail.py
```

### 3. Go to the dist folder and you will find the .exe executable file. Copy and paste it into the main folder

### 4. Delete all other files which are created along with the executable file

"# Automation" 
