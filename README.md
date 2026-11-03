# FHIR R4 Patient & Observation Integration

> **Portfolio demonstration | Synthetic / fictional data only**

A small local extract-and-transform workflow that reads sample FHIR R4 Bundle JSON, resolves Patient references, and exports observations to CSV.

## What this demonstrates
- Read FHIR `Bundle.entry` resources
- Map Observation subject references to Patient resources
- Produce flat clinical analytics rows
- Reject malformed bundles and unknown references

## Quick start
```bash
python src/main.py
python -m unittest discover -s tests
```

Python 3.10+ is recommended. Core functionality uses the Python standard library; no API keys or patient records are required. Run commands from the repository root.

## Repository contents
- `data/sample_bundle.json`: fictional FHIR R4 patient and observations
- `src/main.py`: processing and CSV export
- `tests/`: validation tests
- `output/`: generated CSV

## Relevant skills
FHIR R4, JSON, interoperability, ETL, Python, clinical data mapping

## Data and privacy
All records, facilities, identifiers, events and organizations in this repository are fabricated for demonstrations. This is **not** a production clinical system and does not contain real protected health information (PHI). Do not upload real patient data or confidential employer files. Outputs do not substitute for clinical, privacy, security, or regulatory review.

## How to discuss in an interview
Explain the input, validations or transformations, measurable outputs, tests, and what you would change for a real deployment (authentication, audit logs, monitoring, regulatory review, and secure storage). Describe this as a **personal portfolio project**, not as an implementation at an employer.

## License
MIT — see [LICENSE](LICENSE).
