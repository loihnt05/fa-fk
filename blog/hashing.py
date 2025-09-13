from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash():
    def bcrypt_hash(password: str) -> str:
        return pwd_context.hash(password)