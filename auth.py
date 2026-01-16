from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from config import Setting

def create_access_token(data:dict , expires_detla: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_detla:
        expire = datetime.now() + expires_detla
    else:
        expire = datetime.now() + timedelta(minutes=Setting.access_token_expires)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Setting.secret_key, algorithm=Setting.algorithm)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, Setting.secret_key, algorithms=[Setting.algorithm])
        return payload
    except JWTError:
        return None