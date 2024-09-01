from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(input_password: str, user_password):
    return pwd_context.verify(input_password, user_password)