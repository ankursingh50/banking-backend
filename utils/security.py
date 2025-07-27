# utils/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_mpin(mpin: str) -> str:
    return pwd_context.hash(mpin)

def verify_mpin(plain_mpin: str, hashed_mpin: str) -> bool:
    return pwd_context.verify(plain_mpin, hashed_mpin)

# ✅ Add this for password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
