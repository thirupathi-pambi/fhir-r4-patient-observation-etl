# FHIR R4 Patient & Observation ETL

This is a small Python ETL that takes a FHIR R4 Bundle and flattens it into a CSV. FHIR is great for exchanging data between systems, but it's awkward for reporting, because everything is nested JSON and resources point at each other by reference. I wanted to write that transform step myself and see what it takes to turn linked FHIR resources into one plain row per observation that Excel or a SQL table can use.

The sample data is made up and there are no real patients in it. The script only uses Python's standard library.

## What goes in, what comes out

**In:** `data/sample_bundle.json` is a FHIR Bundle with 2 Patients and 2 Observations. Each Observation points to its patient like this:

```json
"subject": { "reference": "Patient/p001" }
```

**Out:** `output/observations.csv`, with one row per observation and the patient's details joined in:

| patient_id | patient_name | observation_id | loinc_code | observation      | date                 | value | unit      |
|------------|--------------|----------------|------------|------------------|----------------------|-------|-----------|
| p001       | Alex Taylor  | o001           | 8867-4     | Heart rate       | 2026-01-10T10:00:00Z | 72    | beats/min |
| p002       | Casey Morgan | o002           | 8310-5     | Body temperature | 2026-01-11T11:00:00Z | 36.8  | Cel       |

## How it works

1. Load the JSON and check that it's actually a `Bundle` with an `entry` list.
2. Go through the entries once and build a lookup of Patients by `id`.
3. For each Observation, strip `Patient/` from `subject.reference` and look up that patient.
4. Pull out the name, LOINC code, date, value and unit, and write one CSV row.

## Running it

You need Python 3.10 or newer. There's nothing to install.

```bash
python src/main.py
python -m unittest discover -s tests
```

Run both commands from the repo root.

## Some decisions I made

- **A bad reference stops the run.** If an Observation points to a patient that isn't in the Bundle, the script raises an error instead of writing a row with a blank patient. An orphaned lab value with no patient attached is worse than no data, because someone could end up reporting on it.
- **Patients are indexed first, then observations are processed.** In a Bundle, an Observation can appear before its Patient. Building the patient lookup up front means the order inside the Bundle doesn't matter.
- **Other resource types are skipped, not rejected.** If the Bundle also has an Encounter or a Condition, the script ignores it. A real Bundle almost always has more in it than you need.
- **No FHIR library.** Libraries like `fhir.resources` exist and would be the right choice in production. For this project I wanted to work with the raw JSON so I'd understand the structure myself.

## Tests

`tests/test_main.py` covers three cases:

- the sample Bundle produces exactly 2 rows
- an input that isn't a Bundle is rejected
- an Observation pointing to `Patient/missing` is rejected

## Files

```
data/sample_bundle.json   fictional FHIR R4 Bundle (2 Patients, 2 Observations)
src/main.py               extract, reference resolution, CSV export
tests/test_main.py        unit tests
output/observations.csv   generated CSV
```

## What I'd add next

- Check that the coding system is actually `http://loinc.org`. Right now the script takes the first code it finds and puts it in the `loinc_code` column.
- Handle values that aren't quantities, like `valueString` and `valueCodeableConcept`, since plenty of observations aren't numbers
- Add Encounter and Condition support
- Pull the Bundle from a FHIR server's API (a test server such as HAPI) instead of a local file
