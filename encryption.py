from cryptography.fernet import Fernet
from config import PASSWORD_KEY

fernet = Fernet(PASSWORD_KEY)

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token) -> str:
    if isinstance(token, str):
        try:
            return fernet.decrypt(token.encode()).decode()
        except Exception as e:
            return token 
    return token  
