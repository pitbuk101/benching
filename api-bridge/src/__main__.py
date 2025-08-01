from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.auth_middleware import JWTAuthenticationMiddleware

from src.routers.bridge import bridge_router

# App
app = FastAPI()


app.add_middleware(JWTAuthenticationMiddleware)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(router=bridge_router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}