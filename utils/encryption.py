import bcrypt

def hashpw(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def checkpw(password: str, hashed_password: bytes | memoryview):
    if isinstance(hashed_password, memoryview):
        hashed_password = hashed_password.tobytes()

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
