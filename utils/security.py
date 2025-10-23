# utils/security.py
from passlib.context import CryptContext

# Verify both bcrypt_sha256 and bcrypt; create new hashes with bcrypt_sha256
pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto",
    bcrypt_sha256__rounds=12,  # tune if you like
    bcrypt__rounds=12,
)

def hash_mpin(mpin: str) -> str:
    # Optional: enforce MPIN policy (e.g., 4–8 digits)
    if not mpin.isdigit() or not (4 <= len(mpin) <= 8):
        raise ValueError("MPIN must be 4–8 digits")
    return pwd_context.hash(mpin)

def verify_mpin(plain_mpin: str, hashed_mpin: str) -> bool:
    if not plain_mpin.isdigit() or not (4 <= len(plain_mpin) <= 8):
        return False
    return pwd_context.verify(plain_mpin, hashed_mpin)

# Password helpers (can be longer than 72 bytes safely via bcrypt_sha256)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
