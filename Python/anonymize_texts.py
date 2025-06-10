# File 1: anonymize_texts.py
from pathlib import Path
import shutil
from transformers import pipeline
import presidio_analyzer
import presidio_anonymizer
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Agentic-style class for anonymization
class TextAnonymizationAgent:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def anonymize_file(self, filepath: Path):
        text = filepath.read_text()
        results = self.analyzer.analyze(text=text, entities=None, language='en')
        anonymized_result = self.anonymizer.anonymize(text=text, analyzer_results=results)
        return anonymized_result.text

    def process_all(self):
        files = list(self.input_folder.glob("*.txt"))[:100]
        for file in files:
            anonymized_text = self.anonymize_file(file)
            output_filename = file.stem + "_anonymized.txt"
            output_path = self.output_folder / output_filename
            output_path.write_text(anonymized_text)
            print(f"Anonymized: {file.name} -> {output_filename}")

if __name__ == "__main__":
    agent = TextAnonymizationAgent(input_folder="./raw_texts", output_folder="./anonymized_texts")
    agent.process_all()
