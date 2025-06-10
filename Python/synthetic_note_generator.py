import os
import random
from faker import Faker

class SyntheticClinicalNoteGenerator:
    def __init__(self, output_dir="pms_clinical_notes", num_notes=100):
        self.fake = Faker()
        self.output_dir = output_dir
        self.num_notes = num_notes

        self.physical_symptoms = [
            "Developmental Delay", "Speech and Language Impairment", "Hypotonia", "Seizures",
            "Gastrointestinal Issues", "Sleep Disturbances", "Dysmorphia", "Lymphedema",
            "Renal Abnormalities", "Thermoregulation Issues", "Abnormalities of Nails"
        ]
        self.behavioral_symptoms = [
            "Autism Spectrum Disorder (ASD) Features", "Intellectual Disability", "Anxiety",
            "Aggression/Self-Injurious Behaviors", "Hyperactivity/Impulsivity",
            "Sensory Processing Differences", "Compulsive Behaviors", "Mood Dysregulation"
        ]
        self.prescriptions = [
            "Levetiracetam", "Valproic Acid", "Lamotrigine", "Fluoxetine", "Sertraline",
            "Risperidone", "Aripiprazole", "Melatonin", "Polyethylene glycol", "Omeprazole",
            "Ranitidine", "Methylphenidate"
        ]
        self.lab_tests = [
            "Chromosomal Microarray Analysis (CMA)", "FISH", "Karyotype", "EEG",
            "Metabolic Screens", "Renal Ultrasound", "GI Motility Studies"
        ]
        self.therapies = [
            "Early Intervention Programs", "Speech and Language Therapy (SLT)",
            "Occupational Therapy (OT)", "Physical Therapy (PT)", "Applied Behavior Analysis (ABA) Therapy",
            "Feeding Therapy", "Behavioral Therapy/Parent Training", "Surgical Interventions"
        ]
        self.comorbidities = [
            "Autism Spectrum Disorder (ASD)", "Epilepsy/Seizure Disorder", "Gastrointestinal Disorders",
            "Sleep Disorders", "Anxiety Disorders", "ADHD", "Obesity", "Lymphedema",
            "Renal Anomalies", "Immunodeficiency"
        ]

    def generate_clinical_note(self, patient_id):
        name = self.fake.name()
        dob = self.fake.date_of_birth(minimum_age=2, maximum_age=25).strftime('%Y-%m-%d')
        address = self.fake.address().replace('\n', ', ')
        note = f"""
Patient ID: {patient_id}
Name: {name}
DOB: {dob}
Address: {address}

Diagnosis: Phelan-McDermid Syndrome (22q13.3 deletion)

Reported Physical Symptoms:
- {chr(10).join(random.sample(self.physical_symptoms, k=random.randint(3, 6)))}

Reported Behavioral Symptoms:
- {chr(10).join(random.sample(self.behavioral_symptoms, k=random.randint(2, 5)))}

Lab Results:
- {chr(10).join(random.sample(self.lab_tests, k=random.randint(2, 4)))}

Comorbidities:
- {chr(10).join(random.sample(self.comorbidities, k=random.randint(2, 4)))}

Prescriptions:
- {chr(10).join(random.sample(self.prescriptions, k=random.randint(2, 4)))}

Therapeutic Interventions:
- {chr(10).join(random.sample(self.therapies, k=random.randint(2, 4)))}

Additional Notes:
The patient exhibits characteristic features of PMS, including global developmental delay and ASD features. Multidisciplinary management is recommended, with focus on supportive therapies and symptom management.
"""
        return note

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)
        for pid in range(1, self.num_notes + 1):
            note = self.generate_clinical_note(f"PMS-{pid:03d}")
            with open(os.path.join(self.output_dir, f"PMS_{pid:03d}_clinical_note.txt"), "w") as f:
                f.write(note)
        print(f"Generated {self.num_notes} synthetic clinical notes in '{self.output_dir}/'")

def main():
    generator = SyntheticClinicalNoteGenerator()
    generator.run()

if __name__ == "__main__":
    main()
