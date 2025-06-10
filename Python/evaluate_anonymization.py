# File 2: evaluate_anonymization.py
from pathlib import Path
from difflib import SequenceMatcher
from presidio_analyzer import AnalyzerEngine
import numpy as np

class AnonymizationEvaluationAgent:
    def __init__(self, original_folder: str, anonymized_folder: str):
        self.original_folder = Path(original_folder)
        self.anonymized_folder = Path(anonymized_folder)
        self.analyzer = AnalyzerEngine()

    def evaluate_pair(self, original_text: str, anonymized_text: str):
        original_entities = self.analyzer.analyze(text=original_text, entities=None, language='en')
        anonymized_entities = self.analyzer.analyze(text=anonymized_text, entities=None, language='en')

        orig_set = {(e.entity_type, e.start, e.end) for e in original_entities}
        anon_set = {(e.entity_type, e.start, e.end) for e in anonymized_entities}

        true_positives = len(orig_set - anon_set)
        false_negatives = len(orig_set & anon_set)
        false_positives = len(anon_set - orig_set)

        precision = true_positives / (true_positives + false_positives + 1e-6)
        recall = true_positives / (true_positives + false_negatives + 1e-6)
        f1 = 2 * precision * recall / (precision + recall + 1e-6)

        return precision, recall, f1

    def evaluate_all(self):
        precisions, recalls, f1s = [], [], []
        for file in self.original_folder.glob("*.txt"):
            counterpart = self.anonymized_folder / (file.stem + "_anonymized.txt")
            if counterpart.exists():
                orig_text = file.read_text()
                anon_text = counterpart.read_text()
                p, r, f = self.evaluate_pair(orig_text, anon_text)
                precisions.append(p)
                recalls.append(r)
                f1s.append(f)

        print("Evaluation Report")
        print("-----------------")
        print(f"Avg Precision: {np.mean(precisions):.4f}")
        print(f"Avg Recall   : {np.mean(recalls):.4f}")
        print(f"Avg F1 Score : {np.mean(f1s):.4f}")

if __name__ == "__main__":
    evaluator = AnonymizationEvaluationAgent(original_folder="./raw_texts", anonymized_folder="./anonymized_texts")
    evaluator.evaluate_all()
