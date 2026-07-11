import json
from pathlib import Path
from typing import Generator, Dict, Any
from src.config import RAW_DATA_FILE


def stream_mafand_data(file_path: Path = RAW_DATA_FILE) -> Generator[Dict[str, Any], None, None]:
    """
    True Stream Reader: Iterates over Newline-Delimited JSON (NDJSON/JSONL).
    Memory footprint is strictly limited to 1 single string in RAM at any given millisecond.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"\n[!] CRITICAL: Raw data not found at {file_path}.\n"
            f"Please drop your mafand.json file into data/raw/"
        )

    with open(file_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            clean_line = line.strip()
            if not clean_line:
                continue  # Skip trailing blank newlines

            try:
                entry = json.loads(clean_line)
            except json.JSONDecodeError:
                continue  # Defensive: if a scraper dropped half a broken JSON string, skip it safely

            payload = entry.get("translation", entry)

            source = payload.get("en", "")
            target = payload.get("hau", "")

            source_clean = str(source).strip() if source is not None else ""
            target_clean = str(target).strip() if target is not None else ""

            yield {
                "raw_row_id": idx,
                "source_text": source_clean,
                "target_text": target_clean
            }
