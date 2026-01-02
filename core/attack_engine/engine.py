import yaml
import aiohttp
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from core.logger import logger
from core.config import settings
from core.attack_engine.mutator import PayloadMutator

PAYLOAD_DIR = Path(__file__).parent.parent.parent / "payloads"

class AttackEngine:
    def __init__(self):
        self.payloads = self._load_payloads()
        self.mutator = PayloadMutator()
        self.results: List[Dict[str, Any]] = []

    def _load_payloads(self) -> List[Dict[str, Any]]:
        loaded = []
        if not PAYLOAD_DIR.exists():
            logger.warning(f"Payload directory not found: {PAYLOAD_DIR}")
            return loaded
            
        for f in PAYLOAD_DIR.glob("*.yaml"):
            try:
                with open(f, "r") as file:
                    data = yaml.safe_load(file)
                    category = data.get("category", "Unknown")
                    for vector in data.get("vectors", []):
                        vector["category"] = category
                        loaded.append(vector)
            except Exception as e:
                logger.error(f"Failed to load payload file {f}: {e}")
        return loaded

    async def run(self) -> List[Dict[str, Any]]:
        logger.info(f"Starting Attack Engine with {len(self.payloads)} base vectors")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for vector in self.payloads:
                # Generate mutations
                mutations = self.mutator.mutate(vector["payload"])
                logger.info(f"Vector {vector['id']}: Generated {len(mutations)} mutations (Base: {vector['payload'][:20]}...)")
                
                for i, mutant in enumerate(mutations):
                    tasks.append(self._send_attack(session, vector, mutant, i))
            
            # Concurrency control could be added here (Semaphore)
            self.results = await asyncio.gather(*tasks)
            
        logger.info(f"Attack Engine finished. Total requests: {len(self.results)}")
        return self.results

    async def _send_attack(self, session: aiohttp.ClientSession, vector: Dict, payload: str, mutation_id: int) -> Dict[str, Any]:
        target_url = settings.target.url
        method = vector.get("method", "GET")
        location = vector.get("location", "query")
        
        params = {}
        data = {}
        
        # Inject payload based on location
        if location == "query":
            params = {"q": payload} # Generic parameter
        elif location == "body":
            data = {"input": payload}
        
        headers = settings.target.headers.copy() if settings.target.headers else {}
        headers["X-WBT-Vector"] = vector["id"]
        
        # Log attempt start
        # logger.debug(f"Sending {vector['id']} [Mut:{mutation_id}] to {target_url}")
        
        try:
            start_time = asyncio.get_event_loop().time()
            async with session.request(method, target_url, params=params, data=data, headers=headers, timeout=settings.target.timeout) as response:
                end_time = asyncio.get_event_loop().time()
                content = await response.text()
                
                status = response.status
                result_type = "BLOCKED" if status in [403, 406, 500] else "PASSED"
                log_level = logger.warning if result_type == "PASSED" else logger.info
                
                log_level(f"Attack {vector['id']} [Mut:{mutation_id}] => Status: {status} ({result_type})")
                
                return {
                    "vector_id": vector["id"],
                    "category": vector["category"],
                    "payload": payload,
                    "mutation_id": mutation_id,
                    "status": status,
                    "headers": dict(response.headers),
                    "latency": (end_time - start_time) * 1000,
                    "timestamp": start_time
                }
        except Exception as e:
            logger.error(f"Attack request failed for {vector['id']}: {e}")
            return {
                "vector_id": vector["id"],
                "error": str(e)
            }
