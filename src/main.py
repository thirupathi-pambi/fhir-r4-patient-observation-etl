"""Transform a synthetic FHIR R4 Bundle into an observation CSV."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['patient_id', 'patient_name', 'observation_id', 'loinc_code', 'observation', 'date', 'value', 'unit']

def extract(bundle):
    if bundle.get('resourceType') != 'Bundle' or not isinstance(bundle.get('entry'), list):
        raise ValueError('Expected a FHIR Bundle with an entry list')
    resources = [entry['resource'] for entry in bundle['entry'] if 'resource' in entry]
    patients = {p['id']: p for p in resources if p.get('resourceType') == 'Patient'}
    output = []
    for observation in resources:
        if observation.get('resourceType') != 'Observation':
            continue
        reference = observation.get('subject', {}).get('reference', '')
        patient_id = reference.removeprefix('Patient/')
        if not reference.startswith('Patient/') or patient_id not in patients:
            raise ValueError(f'Unknown patient reference: {reference}')
        p = patients[patient_id]
        name = p.get('name', [{}])[0]
        first = ' '.join(name.get('given', []))
        coding = observation.get('code', {}).get('coding', [{}])[0]
        quantity = observation.get('valueQuantity', {})
        output.append(dict(zip(FIELDS, [patient_id, f"{first} {name.get('family', '')}".strip(),
            observation.get('id', ''), coding.get('code', ''), coding.get('display', ''),
            observation.get('effectiveDateTime', ''), quantity.get('value', ''), quantity.get('unit', '')])))
    return output

def main():
    bundle = json.loads((ROOT / 'data/sample_bundle.json').read_text())
    rows = extract(bundle)
    destination = ROOT / 'output/observations.csv'
    destination.parent.mkdir(exist_ok=True)
    with destination.open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f'Exported {len(rows)} observations to {destination}')

if __name__ == '__main__':
    main()
