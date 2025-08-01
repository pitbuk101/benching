from fastapi import FastAPI, HTTPException, Request
from src.ada.azml_realtime_deployments import intent_model_v2_deployment
from src.middleware.authentication import JWTAuthenticationMiddleware
from src.ada.utils.logs.logger import get_logger
from starlette.middleware.cors import CORSMiddleware
from src.ada.use_cases.quick_nego import fetch_supplier
from src.ada.use_cases.quick_nego.agent import ProcurementAgent
from src.ada.components.db.sf_connector import SnowflakeClient
from src.ada.use_cases.quick_nego.model import (
    QuickNegoRequest, QuickNegoResponse, SKURequest, 
    ConversationStartResponse, SupplierResponse,SupplierRequest,SKUResponse,AnalysisStartRequest,AnalysisStartResponse,ResponseStatus,
    WELCOME_MESSAGE,ASSISTANT_ID
)
import json
import asyncio
from datetime import datetime
log = get_logger("SPS Unified ML endpoint")

app = FastAPI()
app.add_middleware(JWTAuthenticationMiddleware)


intent_model_v2_deployment.init()  # This will initialize the model

INPUT_TOKEN_COST = 0.0020 # (2.00 / 1,000) = $0.0020
OUTPUT_TOKEN_COST = 0.0080 # (8.00 / 1,000) = $0.0080




# procurement_agent = ProcurementAgent()
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
            log.info("Running coroutine called intent_model_v2_deployment.run")
            response = asyncio.run(intent_model_v2_deployment.run(json_data))  # Run the coroutine synchronously
        else:
            log.info("Running function called intent_model_v2_deployment.run")
            response = intent_model_v2_deployment.run(json_data)  # Call directly if it's not a coroutine
        return response
    except Exception:
        log.exception("Error running model")
        raise HTTPException(status_code=500, detail="Error running model")

@app.get("/chat/api/quick-nego")
def nego_agent():
    return {"status": "ok", "message": "Negotiation agent is running"}

@app.get("/api/quick-nego/assistant")
def quick_nego_assistant():
    try:
        procurement_agent = ProcurementAgent()
        assistant_id = procurement_agent.create_or_get_assistant()
        if not assistant_id:
            return {"error": "Failed to create or retrieve assistant"}
        
        response_data = {
            "assistant_id": assistant_id,
            "status": "success",
            "message": "Assistant created successfully"
        }
        return response_data
    except Exception as e:
        log.error(f"Error creating assistant: {e}")
        return {"error": str(e)}, 500

@app.post('/chat/api/quick-nego/chat',response_model=QuickNegoResponse)
async def quick_nego_chat(request: QuickNegoRequest):
    thread_id = request.thread_id
    message = request.message
    assistant_id = ASSISTANT_ID
    procurement_agent = ProcurementAgent()
    
    procurement_agent.client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    
    run = procurement_agent.client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    
    status = procurement_agent.wait_for_run_completion(thread_id, run.id, timeout=60)
    
    if status != "completed":
        raise HTTPException(status_code=500, detail=f"Assistant failed: {status}")
    
    messages = procurement_agent.client.beta.threads.messages.list(thread_id=thread_id)
    assistant_messages = [m for m in messages.data if m.role == "assistant"]
    if assistant_messages:
        reply = assistant_messages[0].content[0].text.value
        print(reply)
        return QuickNegoResponse(reply=reply,status=ResponseStatus.COMPLETED)


@app.post('/chat/api/suppliers',response_model=SupplierResponse)
async def get_suppliers(request: SupplierRequest):
    try:
        tenant_id = request.tenant_id
        category = request.category
        sf_client = SnowflakeClient(tenant_id=tenant_id)
        suppliers = fetch_supplier.get_all_suppliers(sf_client=sf_client, category=category)
        suppliers = json.loads(suppliers) if isinstance(suppliers, str) else suppliers
        if not suppliers:
            log.warning("No suppliers found")
            return SupplierResponse(supplier_data=[])
        return SupplierResponse(supplier_data=suppliers)
    except Exception as e:
        log.error(f"Error fetching suppliers: {e}")
        raise HTTPException(status_code=500, detail="Error fetching suppliers")

@app.post('/chat/api/skus',response_model=SKUResponse)
async def get_skus(request: SKURequest):
    try:
        supplier_name = request.supplier_name
        tenant_id = request.tenant_id
        category =request.category
        sf_client = SnowflakeClient(tenant_id=tenant_id)
        skus = fetch_supplier.get_all_skus(sf_client=sf_client,supplier_name=supplier_name,category=category)
        skus = json.loads(skus) if isinstance(skus, str) else skus
        if not skus:
            log.warning("No Sku's found")
            return SKUResponse(skus=skus)
        return SKUResponse(skus=skus)
    except Exception as e:
        log.error(f"Error fetching skus: {e}")
        raise HTTPException(status_code=500, detail="Error fetching skus")

@app.get("/chat/api/quick-nego/start-conversation",response_model=ConversationStartResponse)
def start_conversation():
    try:
        
        agent = ProcurementAgent()
        thread_id = agent.create_thread()
        log.info(f"Starting conversation with thread ID: {thread_id}")
        return ConversationStartResponse(thread_id=thread_id,welcome_message=WELCOME_MESSAGE,status="Success")
    
    except Exception as e:
        log.error(f"Error starting conversation: {e}")
        raise HTTPException(status_code=500, detail="Error starting conversation")


@app.post("/chat/api/quick-nego/start-analyse", response_model=AnalysisStartResponse)
async def start_analyse(request: AnalysisStartRequest):
    try:
        supplier_name = request.supplier_name
        tenant_id = request.tenant_id
        sku = request.sku
        category = request.category_name
        agent = ProcurementAgent()
        thread_id = request.thread_id

        log.info(f"Starting conversation with thread ID: {thread_id}")
        
        # Fetch supplier intelligence
        results = agent.get_supplier_information(supplier_name=supplier_name, tenant_id=tenant_id, category=category, skus=sku)
        llm_results = agent.generate_insights_and_objective_parallel(
            supplier_name=supplier_name,information=results
        )

        objective = llm_results["objective"]
        
        # Message formatting
        message = f'''
        ## This is the information for your strategic negotiation planning and for your assistant to use in the chat:
        **Supplier Name:** { supplier_name}
        ** User Selected SKU or Sku's:** { sku }
        ## SUPPLIER INSIGHTS For your strategic negotiation planning:
        {results.get('supplier_insights', 'No insights available')}

        ## BATNA: {results.get('batna')}

        ## ZOPA: {results.get('zopa')}

        ## Objective: {objective}


        Please acknowledge this information and wait for the user to say "start" before beginning the negotiation process.
        '''
        
        # Send supplier intelligence to the thread
        agent.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        return AnalysisStartResponse(
            status=ResponseStatus.COMPLETED,
            thread_id=thread_id,
            message="Supplier analysis completed successfully"
        )
        
    except Exception as e:
        log.error(f"Error starting conversation: {e}")
        return AnalysisStartResponse(
            status=ResponseStatus.FAILED,
            thread_id=None,
            message=f"Failed to complete analysis: {str(e)}"
        )