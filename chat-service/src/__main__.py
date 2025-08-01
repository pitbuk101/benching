from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.auth_middleware import JWTAuthenticationMiddleware
from src.routers.chat_service import chat_router
from src.routers.docai_service import docai_router
from src.routers.thread_service import thread_router

app = FastAPI()


app.add_middleware(JWTAuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=chat_router, prefix="/v1")
app.include_router(router=docai_router, prefix="/v1")
app.include_router(router=thread_router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}