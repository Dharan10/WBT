from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from core.orchestrator.manager import orchestrator
from core.logger import logger
from core.config import settings, TargetConfig, WAFConfig
from pathlib import Path
import uvicorn
import json
import yaml

app = FastAPI(
    title="WBT - WAF Benchmark Toolkit",
    description="Industry-grade WAF benchmarking platform",
    version="1.0.0"
)

# Allow CORS for dev (though NGINX handles it in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE = Path("logs/wbt.json")
REPORT_DIR = Path("reports")
CONFIG_DIR = Path("configs")

# In-memory storage of last run stats for dashboard
last_run_stats = {
    "total_requests": 0,
    "blocked_requests": 0,
    "passed_requests": 0, # Bypasses
    "false_positives": 0
}

@app.get("/")
async def root():
    return {"message": "WAF Benchmark Toolkit is running. Access /docs for API."}

@app.get("/api/v1/logs")
async def get_logs(limit: int = 50):
    """Get recent application logs"""
    if not LOG_FILE.exists():
        return []
        
    logs = []
    try:
        with open(LOG_FILE, "r") as f:
            # Simple tail implementation
            lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    logs.append(json.loads(line))
                except:
                    continue
    except Exception as e:
        logger.error(f"Failed to read logs: {e}")
        
    return logs

@app.get("/api/v1/reports")
async def list_reports():
    """List generated reports"""
    if not REPORT_DIR.exists():
        return []
    
    files = []
    for f in REPORT_DIR.glob("*.*"):
        files.append({
            "name": f.name,
            "size": f.stat().st_size,
            "modified": f.stat().st_mtime
        })
    # Sort by new
    files.sort(key=lambda x: x["modified"], reverse=True)
    return files

@app.get("/api/v1/reports/{filename}")
async def download_report(filename: str):
    """Download a specific report"""
    path = REPORT_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path)

@app.post("/api/v1/benchmark/start")
async def start_benchmark(mode: str = "concurrent", background_tasks: BackgroundTasks = None):
    """
    Start a new benchmark scan.
    """
    global last_run_stats
    if orchestrator.running:
        return JSONResponse(status_code=409, content={"error": "Benchmark is already running"})
    
    result = await orchestrator.start_benchmark(mode)
    
    # Cache stats for UI
    if result.get("status") == "success":
        results = result["results"]
        last_run_stats = {
            "total_requests": results.get("total_requests", 0),
            "blocked_requests": results.get("blocked_requests", 0),
            "passed_requests": results.get("passed_requests", 0), # Bypasses (False Negatives)
            "false_positives": results.get("false_positives", 0)
        }
    
    return result

@app.get("/api/v1/status")
async def get_status():
    return {"running": orchestrator.running}

@app.get("/api/v1/stats/latest")
async def get_latest_stats():
    """Get statistics from the last run"""
    return last_run_stats

@app.get("/api/v1/config/target")
async def get_target_config():
    """Get current target configuration"""
    return settings.target.dict()

@app.post("/api/v1/config/target")
async def update_target_config(config: TargetConfig):
    """Update target configuration"""
    # Update in-memory
    settings.target = config
    
    # Persist to disk
    try:
        path = CONFIG_DIR / "target.yaml"
        with open(path, "w") as f:
            yaml.dump({"target": config.dict()}, f)
    except Exception as e:
        logger.error(f"Failed to save target config: {e}")
        raise HTTPException(status_code=500, detail="Failed to save configuration")
        
    return config

@app.get("/api/v1/config/waf")
async def get_waf_config():
    """Get current WAF configuration"""
    return settings.waf.dict()

@app.post("/api/v1/config/waf")
async def update_waf_config(config: WAFConfig):
    """Update WAF configuration"""
    # Update in-memory
    settings.waf = config
    
    # Persist to disk
    try:
        path = CONFIG_DIR / "waf.yaml"
        with open(path, "w") as f:
            yaml.dump({"waf": config.dict()}, f)
    except Exception as e:
        logger.error(f"Failed to save waf config: {e}")
        raise HTTPException(status_code=500, detail="Failed to save configuration")
        
    return config

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
