from pathlib import Path
from typing import Any, Dict
import yaml
from pydantic import BaseModel, HttpUrl

class TargetConfig(BaseModel):
    url: str
    timeout: int = 10
    concurrency: int = 5
    headers: Dict[str, str] = {}

class WAFConfig(BaseModel):
    type: str = "modsecurity"
    log_path: str = "/var/log/modsec_audit.log"

class AppConfig:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.target: TargetConfig = self._load_target()
        self.waf: WAFConfig = self._load_waf()

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        path = self.base_dir / "configs" / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

    def _load_target(self) -> TargetConfig:
        data = self._load_yaml("target.yaml")
        # Ensure we are passing the 'target' key content if it exists, otherwise the root dict
        config_data = data.get("target", data)
        return TargetConfig(**config_data)

    def _load_waf(self) -> WAFConfig:
        data = self._load_yaml("waf.yaml")
        config_data = data.get("waf", data)
        return WAFConfig(**config_data)

settings = AppConfig()
