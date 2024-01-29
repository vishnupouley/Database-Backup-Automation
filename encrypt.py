from cryptography.fernet import Fernet
from send_mail import load_key

def encrypt_message(message: str, filename: str) -> None:
    """
    Encrypts a message and saves it to a file.

    Args:
        message (str): The message to be encrypted.
        filename (str): The name of the file to save the encrypted message.
    Returns:
        None
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    with open(filename, 'wb') as file:
        file.write(encrypted_message)

if __name__ == "__main__":
    message = "" # type the password to be encrypted
    filename = "" # type the filename to save the encrypted message
    encrypt_message(message, filename)