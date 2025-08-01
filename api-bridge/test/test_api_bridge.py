import httpx
from datetime import datetime, timedelta, timezone
import jwt
import time

SECRET_KEY = "FBm_ctFvzTMPnWfapsyxCoQi8wv8BTpTghbnkqtxaXb0Ah1rOh_UacePTCLwyaNpfKgCccCpbu7rV8L5rHJH0A"
def generate_jwt():
    payload = {
        "user": "AZ_ML_ENDPOINT",  # Issuer
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=30),  # Expiry
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token 


if __name__ == "__main__":
    with httpx.Client(timeout=100) as client:
        token = generate_jwt()
        print(token)
        start = time.time()
        response = client.post(
            url= "https://dev-sourceai.mckinsey.com/v1/query",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json","service":"api-bridge-service"},
            json={"query": "how much is my tail spend and how many vendors I have?"}
        )
        print(f"Took {time.time() - start} seconds")
        print(response.status_code)
        print(response.json())