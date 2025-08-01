from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.auth_middleware import JWTAuthenticationMiddleware
from src.routers.text2sql_service import text2sql_router

app = FastAPI()


# app.add_middleware(JWTAuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=text2sql_router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}