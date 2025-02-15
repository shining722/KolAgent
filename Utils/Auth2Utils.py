import hashlib
import base64
import secrets

# 生成随机的 code_verifier
def generate_code_verifier(length=128):
    return secrets.token_urlsafe(length)[:length]

# 生成 code_challenge
def generate_code_challenge(code_verifier):
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(hashed).decode('utf-8').replace('=', '')


