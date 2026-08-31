# MAFAND-MT Edge Auditor

A deterministic, lightweight heuristic pipeline for auditing and sanitizing parallel corpora in low-resource African language translation. 

Engineered specifically for the Hausa subset of the MAFAND-MT corpus, this tool identifies web-scraping noise, severe length skews, and entity omissions in sub-second runtimes on standard consumer hardware.

## Overview

Unlike filtering methods that rely on large neural classifiers or n-gram models with historical coverage bias, this pipeline uses a cascading deterministic architecture. It executes locally with minimal memory overhead and zero external API dependencies.

## Pipeline Architecture

Parallel sentence pairs pass through three sequential validation gates:

1. **Gate 1: Language and Script Integrity**
   Uses pycld2 backed by orthographic and lexical overrides. Pairs containing native Hausa hooked characters (ƙ, ɗ, ɓ, ƴ) or high-frequency syntactic markers bypass statistical misclassifications. Identical short entities are retained, while high-confidence foreign text is rejected.

2. **Gate 2: Length and Ratio Validation**
   Computes token length ratios between source and target strings to catch severe truncation, unparsed clauses, or scrap-induced hallucinations.

3. **Gate 3: Entity and Metadata Alignment**
   Extracts numerical entities and hashtags from source and target strings using regular expressions. Verifies retention via set subtraction to ensure factual and contextual consistency.

## Quick Start

### Prerequisites

Python 3.8+ and `pycld2` are required:

```bash
pip install pycld2
```

### Running the Auditor

Run the pipeline against the local dataset:

```bash
python run_pipeline.py
```

The script processes the records, logs audit details into SQLite, and outputs the error taxonomy directly to the terminal.

## Citation

If you use this auditing tool or reference our findings, please cite:

```bibtex
@misc{Yusuf2026mafand,
  title={MAFAND-MT Edge Auditor},
  author={Yusuf, Shuaib Shuaib},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/sysadev/mafand-edge-auditor}}
}
```
