thonimport json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List

logger = logging.getLogger("dealroom-utils")

def load_settings(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Settings file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        settings = json.load(f)

    # Basic validation with sensible defaults
    settings.setdefault("http", {})
    settings["http"].setdefault("timeout", 10)
    settings["http"].setdefault("max_retries", 2)
    settings["http"].setdefault("user_agent", "dealroom-scraper/1.0")

    settings.setdefault("crawler", {})
    settings["crawler"].setdefault("dealroom_base_url", "https://app.dealroom.co/companies")
    settings["crawler"].setdefault("concurrency", 4)
    settings["crawler"].setdefault("sleep_between_requests", 0.5)

    settings.setdefault("paths", {})
    settings["paths"].setdefault("input_domains", "data/input_domains.txt")
    settings["paths"].setdefault("output_file", "data/output_sample.json")

    logger.debug("Loaded settings from %s", path)
    return settings

def read_input_domains(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Input domains file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    identifiers = [line for line in lines if line and not line.startswith("#")]
    logger.info("Loaded %d identifiers from %s", len(identifiers), path)
    return identifiers

def write_json_list(records: Iterable[Dict[str, Any]], path: Path) -> None:
    data_list = list(records)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)
    logger.info("Wrote JSON output to %s (%d records)", path, len(data_list))