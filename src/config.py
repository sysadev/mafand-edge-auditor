from pathlib import Path

# --- PROJECT DIRECTORY MAPPING ---
# Dynamically resolves root folder regardless of where the script runs from
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_FILE = BASE_DIR / "data" / "raw" / "mafand.json"
DB_PATH = BASE_DIR / "data" / "artifacts" / "audit_results.sqlite"

# --- GATE 1: ISO LANGUAGE MAPPING ---
TARGET_LANG = "hau"

# --- GATE 2: LENGTH SKEW HEURISTICS ---
# Acceptable ratio = len(hausa_words) / len(english_words)
MIN_TOKEN_RATIO = 0.25      # Hausa string is suspiciously truncated
MAX_TOKEN_RATIO = 3.50      # Hausa string is suspiciously bloated

# --- GATE 3: ENTITY REGEX ---
NUMERIC_REGEX = r"\b\d+(?:\.\d+)?\b"
HASHTAG_REGEX = r"#(\w+)"

# --- GATE 1: DIPLOMATIC IMMUNITY DNA ---
# If CLD2 gets confused by foreign proper nouns, these markers override it
HAUSA_IMMUNITY_WORDS = {
    "da", "ne", "ce", "ya", "na", "ta", "ka", "ba", "kuma",
    "cewa", "wanda", "wani", "wata", "sai", "suka", "yake",
    "daga", "wannan", "cikin", "lokacin", "akan", "yadda",
    "zuwa", "saboda", "jinsi"
}

# Unique Hausa orthographic hooked characters
HAUSA_HOOKS = set("ƙɗɓƴƘƊƁƳ")
