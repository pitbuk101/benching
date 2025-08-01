import datetime
import os
import jwt

SECRET_KEY = os.getenv('AZML_SECRET_KEY')

def generate_jwt():
    payload = {
        "user": "AZ_ML_ENDPOINT",  # Issuer
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=30),  # Expiry
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
