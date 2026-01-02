import asyncio
import aiohttp
from typing import List, Dict, Any
from core.logger import logger
from core.config import settings

class LegitSimulator:
    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    async def run(self) -> List[Dict[str, Any]]:
        logger.info("Starting Legitimate Traffic Simulation")
        
        target_url = settings.target.url
        # Define some common legitimate paths/actions
        scenarios = [
            {"method": "GET", "path": "/", "name": "Homepage"},
            {"method": "GET", "path": "/login", "name": "Login Page"},
            {"method": "POST", "path": "/api/v1/search", "data": {"q": "products"}, "name": "Search Action"},
            {"method": "GET", "path": "/api/health", "name": "Health Check"},
            {"method": "POST", "path": "/contact", "data": {"message": "Hello support"}, "name": "Contact Form"},
        ]
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for scenario in scenarios:
                # Simulate multiple users
                for i in range(settings.target.concurrency // 2): 
                    tasks.append(self._simulate_user(session, scenario, i))
            
            self.results = await asyncio.gather(*tasks)
            
        logger.info(f"Legit Traffic Simulation finished. Total requests: {len(self.results)}")
        return self.results

    async def _simulate_user(self, session: aiohttp.ClientSession, scenario: Dict, user_id: int) -> Dict[str, Any]:
        url = f"{settings.target.url.rstrip('/')}{scenario['path']}"
        method = scenario["method"]
        data = scenario.get("data")
        
        headers = settings.target.headers.copy() if settings.target.headers else {}
        headers["X-WBT-Legit"] = "true"
        headers["X-WBT-User"] = str(user_id)
        
        try:
            start_time = asyncio.get_event_loop().time()
            async with session.request(method, url, json=data if method == "POST" else None, headers=headers, timeout=settings.target.timeout) as response:
                end_time = asyncio.get_event_loop().time()
                await response.read()
                
                return {
                    "type": "legit",
                    "scenario": scenario["name"],
                    "user_id": user_id,
                    "status": response.status,
                    "latency": (end_time - start_time) * 1000,
                }
        except Exception as e:
            logger.error(f"Legit request failed for {scenario['name']}: {e}")
            return {
                "type": "legit",
                "scenario": scenario["name"],
                "error": str(e)
            }
