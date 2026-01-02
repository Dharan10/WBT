import asyncio
from typing import List, Optional, Dict
from core.config import settings
from core.logger import logger
from core.attack_engine.engine import AttackEngine
from core.legit_traffic.simulator import LegitSimulator
from core.analyzer.detector import DetectionEngine
from core.scoring.calculator import ScoringEngine
from core.reporting.generator import ReportGenerator

class TrafficOrchestrator:
    def __init__(self):
        self.running = False
        self.lock = asyncio.Lock()
        self.attack_engine = AttackEngine()
        self.legit_simulator = LegitSimulator()
        self.detector = DetectionEngine()
        self.scorer = ScoringEngine()
        self.reporter = ReportGenerator()
        
    async def start_benchmark(self, mode: str = "concurrent"):
        """
        Starts the benchmark process.
        :param mode: 'concurrent' (mixed traffic) or 'sequential' (legit then attack)
        """
        async with self.lock:
            if self.running:
                logger.warning("Benchmark already running")
                return {"status": "error", "message": "Benchmark already running"}
            
            self.running = True
            
        logger.info(f"🚀 INITIALIZING BENCHMARK SEQUENCE")
        logger.info(f"Target: {settings.target.url} | Mode: {mode.upper()}")
        
        try:
            attack_results = []
            legit_results = []

            if mode == "sequential":
                legit_results, attack_results = await self._run_sequential()
            else:
                legit_results, attack_results = await self._run_concurrent()
            
            # Combine results
            all_results = attack_results + legit_results
            
            # TODO: Fetch WAF logs via Adapter here if needed for correlation
            waf_logs = [] 
            
            # Analyze
            logger.info("🔍 PHASE: Analysis & Correlation")
            stats = self.detector.analyze(all_results, waf_logs)
            
            # Score
            score_data = self.scorer.calculate_score(stats)
            stats.update(score_data)
            logger.info(f"📊 SCORED: {score_data['total_score']}/100")
            
            # Report
            logger.info("📝 PHASE: Report Generation")
            json_report = self.reporter.generate_json(stats)
            pdf_report = self.reporter.generate_pdf(stats)
            
            logger.info("✅ BENCHMARK COMPLETE successfully.")
            
            return {
                "status": "success", 
                "message": "Benchmark completed", 
                "results": stats,
                "reports": {
                    "json": json_report,
                    "pdf": pdf_report
                }
            }
        except Exception as e:
            logger.error(f"❌ BENCHMARK FAILED: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}
        finally:
            self.running = False

    async def _run_sequential(self):
        logger.info("--- Phase 1: Legitimate Traffic Baseline ---")
        legit_results = await self.legit_simulator.run()
        
        logger.info("--- Phase 2: Attack Traffic Injection ---")
        attack_results = await self.attack_engine.run()
        
        return legit_results, attack_results

    async def _run_concurrent(self):
        logger.info("--- Starting Concurrent Traffic Simulation ---")
        results = await asyncio.gather(
            self.legit_simulator.run(),
            self.attack_engine.run()
        )
        logger.info("--- Traffic Simulation Complete ---")
        return results[0], results[1]

orchestrator = TrafficOrchestrator()
