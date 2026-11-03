# FHIR R4 Patient & Observation ETL

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A small, dependency-free Python ETL that reads a FHIR R4 `Bundle`, resolves each Observation to its Patient, and exports flat, analytics-ready CSV rows.

> Built on synthetic data only. No real patient information is included.

## Why this exists

FHIR resources are nested and linked by references, which makes them awkward for reporting tools. This project shows the core transformation step: take a Bundle, follow `Observation.subject` references back to `Patient` resources, and produce one flat row per observation that a BI tool or SQL table can consume.

## Features

- Reads `Bundle.entry` resources from FHIR R4 JSON
- Resolves Observation → Patient references
- Exports one flat CSV row per observation
- Rejects malformed bundles
- Rejects observations that reference an unknown Patient
- Unit tests for the validation paths

## Project structure

```
.
├── data/
│   └── sample_bundle.json     # fictional FHIR R4 Patient + Observation resources
├── src/
│   └── main.py                # parsing, reference resolution, CSV export
├── tests/                     # validation tests
├── output/                    # generated CSV
├── LICENSE
└── README.md
```

## Quick start

Requires Python 3.10+ and nothing else (standard library only). Run from the repository root.

```bash
python src/main.py                      # writes the CSV to output/
python -m unittest discover -s tests    # runs the tests
```

## How it works

1. Load the Bundle JSON and confirm it is a valid `Bundle` with entries.
2. Index Patient resources by id.
3. For each Observation, look up the Patient named in `subject.reference`; fail clearly if it doesn't exist.
4. Write the combined patient + observation fields to CSV.

## Limitations and next steps

- Handles a small, fixed subset of fields rather than the full FHIR spec.
- Not validated against FHIR profiles; a production version would use a FHIR validator or a library such as `fhir.resources`.
- Possible extensions: support more resource types (Encounter, Condition), read from a FHIR server API, add schema-based validation, and add logging.

## License

MIT. See [LICENSE](LICENSE).
