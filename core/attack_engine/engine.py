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
        evasion_level = settings.target.evasion_level
        logger.info(f"Starting Attack Engine with {len(self.payloads)} base vectors | Evasion Level: {evasion_level}")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for vector in self.payloads:
                # Generate mutations based on configured evasion level
                mutations = self.mutator.mutate(vector["payload"], level=evasion_level)
                logger.info(f"Vector {vector['id']}: Generated {len(mutations)} mutations (Base: {vector['payload'][:20]}...)")
                
                for i, mutant in enumerate(mutations):
                    tasks.append(self._send_attack(session, vector, mutant, i))
            
            # Concurrency control could be added here (Semaphore)
            self.results = await asyncio.gather(*tasks)
            
        logger.info(f"Attack Engine finished. Total requests: {len(self.results)}")
        return self.results

    async def _send_attack(self, session: aiohttp.ClientSession, vector: Dict, payload: str, mutation_id: int) -> Dict[str, Any]:
        """
        Sends a single attack request.
        """
        url = settings.target.url
        method = vector.get("method", "GET")
        location = vector.get("location", "query")
        
        # Prepare params/body
        params = {}
        data = None
        headers = settings.target.headers.copy() # Start with global custom headers
        
        # Dynamically inject payload
        if location == "query":
            params = {"q": payload}
        elif location == "header":
            headers["X-Attack-Payload"] = payload
        elif location == "body":
            data = {"input": payload}
        elif location == "path":
            if url.endswith("/"):
                url += payload
            else:
                url += "/" + payload
                
        try:
            async with session.request(
                method, 
                url, 
                params=params, 
                json=data, 
                headers=headers, 
                timeout=settings.target.timeout
            ) as response:
                status = response.status
                text = await response.text()
                
                result_type = "BLOCKED" if status in [403, 406, 500] else "PASSED"
                log_level = logger.warning if result_type == "PASSED" else logger.info
                
                log_level(f"Attack {vector['id']} [Mut:{mutation_id}] => Status: {status} ({result_type})")
                
                return {
                    "vector_id": vector["id"],
                    "mutation_id": mutation_id,
                    "category": vector["category"],
                    "payload": payload,
                    "status": status,
                    "response_len": len(text)
                }
        except Exception as e:
            logger.error(f"Attack failed {vector['id']}: {e}")
            return {"vector_id": vector["id"], "error": str(e)}
