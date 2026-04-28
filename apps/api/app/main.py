import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("residency-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Data Residency Blueprints API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/regions")
def get_regions():
    return [
        {"id": "eu-boundary", "name": "EU Data Boundary", "compliance_score": 0.984, "status": "COMPLIANT"},
        {"id": "uk-sovereign", "name": "UK Sovereign Zone", "compliance_score": 0.92, "status": "WARNING"},
        {"id": "us-regulated", "name": "US Regulated Hub", "compliance_score": 1.0, "status": "COMPLIANT"}
    ]

@app.get("/policies")
def get_policies():
    return [
        {"id": "pol-loc-001", "name": "EU Citizen Localization", "category": "Residency", "severity": "CRITICAL"},
        {"id": "pol-enc-042", "name": "Local Key Management", "category": "Encryption", "severity": "HIGH"},
        {"id": "pol-tra-101", "name": "Cross-Border Approval", "category": "Transfer", "severity": "MEDIUM"}
    ]

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "global_sovereignty_index": 0.962,
        "policy_violations": 2,
        "pending_transfers": 14,
        "last_audit": "2026-04-20"
    }

@app.get("/risks")
def get_risks():
    return [
        {"id": "risk-456", "title": "SaaS Data Exfiltration", "level": "HIGH", "owner": "Privacy Office"},
        {"id": "risk-789", "title": "Legacy Backup Locality", "level": "MED", "owner": "Infrastructure Team"}
    ]

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_regional_pods": 24,
        "managed_countries": 12,
        "compliance_uptime": "99.994%",
        "active_exceptions": 3
    }

@app.post("/blueprints/validate")
def validate_blueprint(blueprint_id: str, region: str):
    logger.info(f"Validating sovereignty blueprint: {blueprint_id} for region: {region}")
    return {"status": "Validation Job Enqueued", "job_id": "job_res_789"}
