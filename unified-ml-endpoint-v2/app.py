from fastapi import FastAPI, HTTPException, Request
from src.ada.azml_realtime_deployments import intent_model_v2_deployment
from src.middleware.authentication import JWTAuthenticationMiddleware
from ada.utils.logs.logger import get_logger
from starlette.middleware.cors import CORSMiddleware
import asyncio
log = get_logger("SPS Unified ML endpoint")

app = FastAPI()
app.add_middleware(JWTAuthenticationMiddleware)

intent_model_v2_deployment.init()  # This will initialize the model

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def read_root(request: Request):
    try:
        # Run the coroutine to get JSON data synchronously
        json_data = asyncio.run(request.json())
        log.info(f"Received request data: {json_data}")
        # Check if intent_model_v2_deployment.run is a coroutine
        if callable(getattr(intent_model_v2_deployment.run, "__await__", None)):
            response = asyncio.run(intent_model_v2_deployment.run(json_data))  # Run the coroutine synchronously
        else:
            response = intent_model_v2_deployment.run(json_data)  # Call directly if it's not a coroutine
        return response
    except Exception:
        log.exception("Error running model")
        raise HTTPException(status_code=500, detail="Error running model")