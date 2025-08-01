import contextlib
import asyncio
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.providers.cache_store.redis_cache import RedisCacheProvider
from src.utils.logs import get_custom_logger
from src.pipelines.deploy.force_deploy import force_deploy_semantics
logger = get_custom_logger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the CloudWatch client once
cloudwatch_client = boto3.client("cloudwatch", region_name="us-east-1")

# Create RedisCacheProvider instances for each DB once
queue_dbs = [1, 2, 3]
redis_cache_providers = {db: RedisCacheProvider(REDIS_DB=db) for db in queue_dbs}

async def emit_queue_metric():
    queue_name = "celery"
    try:
        metric_data = []
        for db in queue_dbs:
            try:
                logger.debug(f"Checking DB: {db}")
                cache = redis_cache_providers[db]
                queue_size = cache.check_queue_size(queue_name)
                queue_size += cache.check_queue_size("unacked")
                metric_data.append({
                    'MetricName': f'PendingTasks_{queue_name}_{db}',
                    'Dimensions': [{'Name': 'Queue', 'Value': f"{queue_name}_{db}"}],
                    'Value': queue_size,
                    'Unit': 'Count'
                })
            except Exception as qe:
                logger.info(f"[✗] Failed to get size for queue '{queue_name}':", qe)
        if metric_data:
            cloudwatch_client.put_metric_data(Namespace="Celery", MetricData=metric_data)
            logger.info(f"✅ Successfully Emitted Metrics.")
    except Exception as e:
        logger.exception(f"❌ Failed to emit metrics: {e}")
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def periodic_task():
        while True:
            await emit_queue_metric()
            await asyncio.sleep(5)
    task = asyncio.create_task(periodic_task())
    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

app.router.lifespan_context = lifespan

@app.post("/force-deploy")
async def deploy():
    await force_deploy_semantics()
    return {"status": "Accepted"}

@app.get("/health")
def health():
    return {"status": "ok"}


