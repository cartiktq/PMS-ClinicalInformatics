import os
import csv
import uuid
import spacy
from typing import List, Dict
from pathlib import Path

# Dummy UMLS linking logic for illustration
class UMLSLinker:
    def __init__(self, umls_map_file="cui_to_aui.csv"):
        self.cui_to_aui = self.load_cui_to_aui_map(umls_map_file)

    def load_cui_to_aui_map(self, filepath: str) -> Dict[str, List[Dict[str, str]]]:
        mapping = {}
        if not os.path.exists(filepath):
            print(f"Warning: UMLS mapping file {filepath} not found.")
            return mapping
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cui = row['CUI']
                mapping.setdefault(cui, []).append({
                    'AUI': row['AUI'],
                    'SAB': row['SAB'],  # source vocab, e.g., ICD10CM, RXNORM
                    'CODE': row['CODE']
                })
        return mapping

    def map_entity_to_cuis(self, entity: str) -> List[str]:
        # Placeholder logic — replace with QuickUMLS/MetamapLite output
        return [f"C{hash(entity) % 100000:06d}"]

    def map_cui_to_auis(self, cui: str) -> List[Dict[str, str]]:
        return self.cui_to_aui.get(cui, [])


class ClinicalNoteTripleExtractor:
    def __init__(self, input_dir: str, output_csv: str, umls_linker: UMLSLinker):
        self.input_dir = input_dir
        self.output_csv = output_csv
        self.umls_linker = umls_linker
        self.nlp = spacy.load("en_core_sci_md")  # use SciSpacy model
        self.relation_map = {
            "DIAGNOSIS": "diagnosis",
            "SYMPTOM": "symptom",
            "BEHAVIOR": "behavior",
            "TECHNIQUE": "technique",
            "THERAPY": "therapy",
            "PRESCRIPTION": "prescription",
            "LAB": "lab",
            "COMORBIDITY": "comorbidity"
        }

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            label = ent.label_.upper()
            relation = self.relation_map.get(label)
            if relation:
                entities.append({"text": ent.text, "relation": relation})
        return entities

    def generate_triples(self) -> None:
        triples = []
        for filepath in Path(self.input_dir).glob("*.txt"):
            with open(filepath, "r") as f:
                text = f.read()
            patient_id = str(uuid.uuid4())
            entities = self.extract_entities(text)
            for entity in entities:
                cuis = self.umls_linker.map_entity_to_cuis(entity["text"])
                for cui in cuis:
                    auis = self.umls_linker.map_cui_to_auis(cui)
                    for aui in auis:
                        triples.append([
                            patient_id,
                            entity["relation"],
                            f"{aui['SAB']}:{aui['CODE']}"
                        ])
        self.write_triples(triples)

    def write_triples(self, triples: List[List[str]]) -> None:
        with open(self.output_csv, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["patient_id", "relation", "identifier"])
            writer.writerows(triples)
        print(f"Generated {len(triples)} triples at '{self.output_csv}'")

def main():
    input_dir = os.environ.get("INPUT_DIR", "./clinical_notes")
    output_csv = os.environ.get("OUTPUT_CSV", "./output_triples.csv")
    umls_map_file = os.environ.get("UMLS_MAP", "./cui_to_aui.csv")

    linker = UMLSLinker(umls_map_file)
    extractor = ClinicalNoteTripleExtractor(input_dir, output_csv, linker)
    extractor.generate_triples()

if __name__ == "__main__":
    main()
