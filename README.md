# MAFAND-MT Edge Auditor

A lightweight, serverless heuristic pipeline for auditing and sanitizing low-resource African language corpora. This engine was specifically engineered to audit the Hausa subset of the MAFAND-MT dataset, filtering out web-scraping noise, truncation, and factual entity dropping in sub-second runtimes on standard consumer hardware.

## Overview

Unlike standard filtering paradigms that rely on heavy, memory-intensive deep neural classifiers or pre-trained n-gram models with historical coverage bias, this architecture uses a highly deterministic, cascading heuristic approach. It executes entirely on localized edge-compute environments with minimal memory footprint.

## Pipeline Architecture

The pipeline processes parallel translation records through three strict validation gates.

* **Gate 1: Orthographic Language Identification**
  Utilizes Google's Compact Language Detector 2 (CLD2) via `pycld2` alongside native orthographic immunity rules (such as Hausa hooked characters ƙ, ɗ, ɓ) to prevent false negatives on valid domain-specific terminology.
* **Gate 2: Syntactic Density Physics**
  Enforces a strict source-to-target word count ratio to immediately isolate severe truncation, missing translation clauses, or unparsed HTML scraper bloat.
* **Gate 3: Constant-Time Entity Alignment**
  Extracts all numerical data and hashtags via regular expressions and maps them into memory as hash sets. Verification executes instantly via set subtraction, ensuring absolute factual and clinical alignment between the source and target strings.

## Quick Start

### Prerequisites
The engine requires Python 3.8+ and the official CLD2 Python bindings.

```bash
pip install pycld2
```

### Execution
Run the auditing pipeline directly against your SQLite dataset.

```bash
python run_pipeline.py
```

The script will output the empirical error taxonomy directly to your terminal, detailing overall pass rates and granular gate failure distributions.

## Citation

If you use this auditing pipeline or our empirical findings in your research, please cite our software repository.

```bibtex
@misc{Yusuf2026mafand,
  title={Auditing Data Rot in Low-Resource African Machine Translation},
  author={Yusuf, Shuaib Shuaib},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/sysadev/mafand-edge-auditor}}
}
```
