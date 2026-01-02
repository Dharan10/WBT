from abc import ABC, abstractmethod
from typing import Dict, Any, List
from core.config import settings

class BaseWAFAdapter(ABC):
    def __init__(self):
        self.config = settings.waf

    @abstractmethod
    async def get_logs(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """
        Retrieve logs from the WAF for the given time window.
        """
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Verify WAF is reachable.
        """
        pass

    @abstractmethod
    def parse_log_entry(self, entry: Any) -> Dict[str, Any]:
        """
        Normalize WAF specific log entry to common WBT format.
        Should return dict with keys: timestamp, request_id, rule_id, action, client_src
        """
        pass
