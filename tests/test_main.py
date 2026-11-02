import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from main import extract

class FHIRTests(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(len(extract(json.loads((ROOT/'data/sample_bundle.json').read_text()))), 2)
    def test_invalid_bundle(self):
        with self.assertRaises(ValueError): extract({})
    def test_unknown_patient(self):
        with self.assertRaises(ValueError): extract({'resourceType':'Bundle','entry':[{'resource':{'resourceType':'Observation','subject':{'reference':'Patient/missing'}}}]})
