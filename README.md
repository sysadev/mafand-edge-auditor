# MAFAND-MT Edge Auditor

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23003213.svg)](https://doi.org/10.5281/zenodo.23003213)

A deterministic, lightweight heuristic pipeline for auditing and sanitizing parallel corpora in low-resource African language translation.

Engineered specifically for the Hausa subset of the MAFAND-MT corpus, this tool identifies web-scraping noise, severe length skews, and entity omissions in sub-second runtimes on standard consumer hardware.

## Overview

Unlike filtering methods that rely on large neural classifiers or n-gram models with historical coverage bias, this pipeline uses a cascading deterministic architecture. It executes locally with minimal memory overhead and zero external API dependencies.

## Pipeline Architecture

Parallel sentence pairs pass through three sequential validation gates:

1. **Gate 1: Language and Script Integrity**
   Uses pycld2 backed by orthographic and lexical overrides. Pairs containing native Hausa hooked characters (ƙ, ɗ, ɓ, ƴ) or high-frequency syntactic markers bypass statistical misclassifications. Identical short entities are retained, while high-confidence foreign text is rejected.

2. **Gate 2: Length and Ratio Validation**
   Computes token length ratios between source and target strings to catch severe truncation, unparsed clauses, or scrape-induced hallucinations.

3. **Gate 3: Entity and Metadata Alignment**
   Extracts numerical entities and hashtags from source and target strings using regular expressions. Verifies retention via set subtraction to ensure factual and contextual consistency.

## Quick Start

### Prerequisites

Python 3.8+ and `pycld2` are required:

```bash
pip install pycld2==0.42
```

### Data

- `data/raw/mafand.json`: the Hausa subset of MAFAND-MT (input to the pipeline)
- `data/artifacts/filtered.json`: bundled reference file, the passed pairs only
- `data/artifacts/fixed.json`: bundled reference file, passed pairs plus manually corrected versions of the non-passed pairs. Corrections were made by the author, a native Hausa speaker.

### Running the Auditor

```bash
python run_pipeline.py
```

The script audits `data/raw/mafand.json` and writes results to `data/artifacts/audit_results.sqlite`.

### Example Output

```
[+] Booting MAFAND-MT Edge Auditor...
[+] Conveyor belt running. Auditing pairs...
[✓] Audit Complete: 5,865 pairs processed in 0.89s.

====================================================
             EMPIRICAL AUDIT TAXONOMY
====================================================
 PASSED                     |   5,515 rows  ( 94.0%)
 GATE_3_ENTITY_ALIGNMENT    |     276 rows  (  4.7%)
 GATE_2_LENGTH_SKEW         |      72 rows  (  1.2%)
 GATE_1_LANG_ID             |       2 rows  (  0.0%)
====================================================
```

## Data and License

This tool operates on the Hausa subset of MAFAND-MT (Adelani et al., NAACL 2022), bundled in `data/raw/mafand.json` for reproducibility. The dataset is licensed under CC-BY-NC-4.0, separate from this repository's MIT code license. Please respect the non-commercial restriction if reusing the data.

Note: per the original MAFAND-MT documentation, the Hausa training set is of mixed provenance. An initial portion was created by the MAFAND-MT authors, with the remainder sourced from the WMT21 News Translation Task. Downstream news-source licensing may apply to that portion.

If you use this dataset, please cite the original paper:

```bibtex
@inproceedings{adelani-etal-2022-thousand,
    title = "A Few Thousand Translations Go a Long Way! Leveraging Pre-trained Models for African News Translation",
    author = "Adelani, David and Alabi, Jesujoba and Fan, Angela and Kreutzer, Julia and Shen, Xiaoyu and Reid, Machel and Ruiter, Dana and Klakow, Dietrich and Nabende, Peter and Chang, Ernie and Gwadabe, Tajuddeen and Sackey, Freshia and Dossou, Bonaventure F. P. and Emezue, Chris and Leong, Colin and Beukman, Michael and Muhammad, Shamsuddeen and Jarso, Guyo and Yousuf, Oreen and Niyongabo Rubungo, Andre and Hacheme, Gilles and Wairagala, Eric Peter and Nasir, Muhammad Umair and Ajibade, Benjamin and Ajayi, Tunde and Gitau, Yvonne and Abbott, Jade and Ahmed, Mohamed and Ochieng, Millicent and Aremu, Anuoluwapo and Ogayo, Perez and Mukiibi, Jonathan and Ouoba Kabore, Fatoumata and Kalipe, Godson and Mbaye, Derguene and Tapo, Allahsera Auguste and Memdjokam Koagne, Victoire and Munkoh-Buabeng, Edwin and Wagner, Valencia and Abdulmumin, Idris and Awokoya, Ayodele and Buzaaba, Happy and Sibanda, Blessing and Bukula, Andiswa and Manthalu, Sam",
    booktitle = "Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    year = "2022",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.naacl-main.223",
    doi = "10.18653/v1/2022.naacl-main.223",
    pages = "3053--3070",
}
```

## Citation

If you use this auditing tool or reference our findings, please cite:

```bibtex
@software{yusuf_2026_23003214,
  author       = {Yusuf, Shuaib Shuaib},
  title        = {MAFAND-MT Edge Auditor},
  month        = sep,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.23003213},
  url          = {https://doi.org/10.5281/zenodo.23003213},
}
```
