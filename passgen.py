import bcrypt
import uuid

def passgen():  
    # example password 
    password = '123'
    
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 
    
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    
    print("pass:",hash)
    
def idgen():
    unique_id = uuid.uuid4()
    print(unique_id)