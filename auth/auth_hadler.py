import time
import jwt

JWT_SECRET = '8d334cfeeb428b004fc30569fc2c4091b61c558eb2b9593f8ef878013eaa7493'
JWT_ALGORITHM = 'HS256'


def token_response(token):
    return {
        "access_token": token
    }


def signJWT(login, employer, id):
    payload = {
        'id': id,
        'login': login,
        'employer': employer,
        'expires': time.time() + 3600 * 24
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}


def JWTtoJSON(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
