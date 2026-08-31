import re
import pycld2 as cld2
from typing import Tuple, Set

from src.config import (
    TARGET_LANG,
    MIN_TOKEN_RATIO,
    MAX_TOKEN_RATIO,
    NUMERIC_REGEX,
    HASHTAG_REGEX,
    HAUSA_IMMUNITY_WORDS,
    HAUSA_HOOKS,
)


def _gate_1_language_check(source_text: str, target_text: str) -> Tuple[bool, str]:
    """Gate 1: Language and Script Validation."""
    if not target_text:
        return False, "Target string is totally empty."

    # 1. Native Hausa orthographic markers
    if any(char in HAUSA_HOOKS for char in target_text):
        return True, ""

    # 2. High frequency Hausa syntactic markers
    words = set(re.findall(r"\b[a-z']+\b", target_text.lower()))
    if words.intersection(HAUSA_IMMUNITY_WORDS):
        return True, ""

    # 3. CLD2 Language Detection
    try:
        is_reliable, _, details = cld2.detect(target_text)
    except Exception as e:
        return False, f"CLD2 engine parsing crash: {str(e)}"

    top_lang_name, top_lang_code, confidence, _ = details[0]
    expected_code = "ha" if TARGET_LANG == "hau" else TARGET_LANG

    # 4. Confident Foreign Language Rejection
    if top_lang_code not in (expected_code, "un") and confidence >= 80:
        return False, f"Language mismatch. Detected '{top_lang_name}' ({top_lang_code}) at {confidence}% confidence."

    # 5. Invariant Entity Bypass versus Untranslated Sentences
    if source_text.strip() == target_text.strip():
        if len(words) <= 3:
            return True, ""
        return False, "Untranslated source text repeated as target."

    # 6. Forgiving the Unknown Classification
    if top_lang_code == "un":
        return True, ""

    # 7. Final mismatch catch
    if top_lang_code != expected_code:
        return False, f"Language mismatch. Detected '{top_lang_name}' ({top_lang_code}) at {confidence}% confidence."

    return True, ""


def _gate_2_length_skew(source_text: str, target_text: str) -> Tuple[bool, str]:
    """Gate 2: The Scale. Checks word count physics between source and target."""
    src_words = source_text.split()
    tgt_words = target_text.split()

    src_len = len(src_words)
    tgt_len = len(tgt_words)

    if src_len == 0:
        return False, "Source English text contains 0 tokens."
    if tgt_len == 0:
        return False, "Target Hausa text contains 0 tokens."

    ratio = tgt_len / src_len

    if ratio < MIN_TOKEN_RATIO:
        return False, f"Severe truncation. Ratio {ratio:.2f} < min {MIN_TOKEN_RATIO} (Eng: {src_len}w, Hausa: {tgt_len}w)"

    if ratio > MAX_TOKEN_RATIO:
        return False, f"Severe hallucination. Ratio {ratio:.2f} > max {MAX_TOKEN_RATIO} (Eng: {src_len}w, Hausa: {tgt_len}w)"

    return True, ""


def _extract_entities(text: str) -> Tuple[Set[str], Set[str]]:
    """Helper: Pulls raw numbers and normalized hashtags out of a string."""
    numbers = set(re.findall(NUMERIC_REGEX, text))

    raw_hashtags = re.findall(HASHTAG_REGEX, text)
    hashtags = {tag.lower() for tag in raw_hashtags}

    return numbers, hashtags


def _gate_3_entity_alignment(source_text: str, target_text: str) -> Tuple[bool, str]:
    """Gate 3: The Auditor. Verifies numbers and hashtags survived the trip."""
    src_nums, src_tags = _extract_entities(source_text)
    tgt_nums, _ = _extract_entities(target_text)

    # 1. Number Audit
    missing_nums = src_nums - tgt_nums
    if missing_nums:
        return False, f"Dropped numeric entities: {sorted(list(missing_nums))}"

    # 2. Hashtag Audit
    tgt_lower = target_text.lower()
    missing_tags = [tag for tag in src_tags if tag not in tgt_lower]

    if missing_tags:
        return False, f"Dropped hashtag entities: {sorted(missing_tags)}"

    return True, ""


def audit_sentence_pair(source: str, target: str) -> Tuple[bool, str, str]:
    """
    The Master Gateway. Passes data through Bouncers 1, 2, and 3 sequentially.
    Returns: (is_valid, gate_failed_enum, error_reason_text)
    """
    passed, reason = _gate_1_language_check(source, target)
    if not passed:
        return False, "GATE_1_LANG_ID", reason

    passed, reason = _gate_2_length_skew(source, target)
    if not passed:
        return False, "GATE_2_LENGTH_SKEW", reason

    passed, reason = _gate_3_entity_alignment(source, target)
    if not passed:
        return False, "GATE_3_ENTITY_ALIGNMENT", reason

    return True, "PASSED", "Pristine record."
