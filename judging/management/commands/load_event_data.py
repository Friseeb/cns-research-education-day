from django.core.management.base import BaseCommand
import json

_DATA = json.loads(r"""
{
  "submissions": [
    {
      "abstract_number": "PLAT-1",
      "title": "Surgical residency attrition in Canada - Trainee Perspectives on leaving surgical training",
      "presenting_author": "Amirti Vivekanandan",
      "presenting_author_email": "",
      "co_authors": "A. Sepulveda, K. Squires, S. Singh, K. MacDougall, A. Harvey, S. Lopushinsky, O. Daodu",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "Surgical residency attrition in Canada - Trainee Perspectives on leaving surgical training",
      "location": "O1 | 9:40 - 9:49 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-10",
      "title": "Decoding Cognitive and Oculomotor Signals from Prefrontal Cortex Neural Ensembles During Naturalistic Behavior",
      "presenting_author": "Mohamad Abbass",
      "presenting_author_email": "",
      "co_authors": "R.G.Couper, P.H. Espino, J.G. Burneo",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "Outcomes of Valproic Acid Withdrawal in Females Before or During Pregnancy: A Systematic Review and Meta-analysis",
      "location": "O3 | 12:09 \u2013 12:18 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-11",
      "title": "Outcomes of Valproic Acid Withdrawal in Females Before or During Pregnancy: A Systematic Review and Meta-analysis",
      "presenting_author": "Maria Claudia Burbano Donoso",
      "presenting_author_email": "",
      "co_authors": "A. Alanazi, A.Svendrovski, B. Ciftci, J. Racosta, P. Riccio, C. Casserly",
      "category": "Fellow",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "Association Between Serum Neurofilament Light Chain Levels and MRI Activity Across Disability Levels and Treatment Contexts in Multiple Sclerosis",
      "location": "O2 | 12:18 \u2013 12:27 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-12",
      "title": "Association Between Serum Neurofilament Light Chain Levels and MRI Activity Across Disability Levels and Treatment Contexts in Multiple Sclerosis",
      "presenting_author": "Zainab Alfares",
      "presenting_author_email": "",
      "co_authors": "R. Eagleson, A. Khan, G. Pellegrino",
      "category": "Fellow",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "Structure-Function Coupling for Epileptogenic Zone Network Identification and Connectivity Analysis in Paediatric Focal Epilepsy",
      "location": "O2 | 12:27 \u2013 12:36 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-13",
      "title": "Clinical Predictors of Freezing of Gait with Reduced Dopaminergic Responsiveness in Parkinson\u2019s Disease",
      "presenting_author": "Mojtaba Sharafkhah",
      "presenting_author_email": "",
      "co_authors": "S. Pandey, P. Malik, J. Megyesi, R. Bartha",
      "category": "Graduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "Clinically Feasible pH-Weighted Imaging at University Hospital: A Proof-of-Concept Study",
      "location": "O2 | 12:36 \u2013 12:45 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-14",
      "title": "Structure-Function Coupling for Epileptogenic Zone Network Identification and Connectivity Analysis in Paediatric Focal Epilepsy",
      "presenting_author": "Adetunji Oremakinde",
      "presenting_author_email": "",
      "co_authors": "A. Diana Ayan, B. Lakni Abeyesekera, C. Fawaz Alotaibi, D. Arturo Gonzalez Lara, E. Jaime Rodriguez Orozco, F. Zahra Mirza Asgari, G. Lorne Gula, H. Alan Skanes, I. Jason Andrade, J. Lauren Mai, K. Sebastian Fridman, L. Thalia Field, M. Michael Hill, N. Rodrigo Bagur, O. Luciano A. Sposato",
      "category": "Graduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "First Canadian Experience of Stroke Fellows Implanting Loop Recorders in Stroke Patients: Preliminary Results of the B2AD-Risk AFDAS Study",
      "location": "O2 | 12:45 \u2013 12:54 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-15",
      "title": "Clinically Feasible pH-Weighted Imaging at University Hospital: A Proof-of-Concept Study",
      "presenting_author": "Dickson Wong",
      "presenting_author_email": "",
      "co_authors": "David Hudson, Anita Florendo-Cumbermack",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "Reducing the Rate of Urinary Tract Infections (UTIs) on the Neurology Ward",
      "location": "O3 | 1:45 \u2013 1:54 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-16",
      "title": "First Canadian Experience of Stroke Fellows Implanting Loop Recorders in Stroke Patients: Preliminary Results of the B2AD-Risk AFDAS Study",
      "presenting_author": "Eduardo Soriano Navarro",
      "presenting_author_email": "",
      "co_authors": "G. Pellegrino",
      "category": "Fellow",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "Examining Cortical Excitability Using Magnetoencephalography",
      "location": "O3 | 1:54 \u2013 2:03 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-17",
      "title": "Reducing the Rate of Urinary Tract Infections (UTIs) on the Neurology Ward",
      "presenting_author": "Trevor Jairam",
      "presenting_author_email": "",
      "co_authors": "K. Dwyer, P. Riccio, J. Racosta, P. Malik, C. S. Casserly, A. Budhram, B. Ciftci",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "An Exploratory Analysis of the Prognostic Significance of Serum Neurofilament Light Chain for Disability Progression and Treatment Outcomes in Multiple Sclerosis: A Retrospective Cohort Study",
      "location": "O3 | 2:03 \u2013 2:12 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-18",
      "title": "Examining Cortical Excitability Using Magnetoencephalography",
      "presenting_author": "Kevin Kim",
      "presenting_author_email": "",
      "co_authors": "K.K.L. Coleman, K. Borron, R.G. Tirona, C.A. Rupar, G. Zou, R.A. Hegele, E.C. Finger, R. Bartha, S.A. Morrow, J. Wells, M. Borrie, P.A. MacDonald, M.E. Jenkins, M.S. Jog, G. Dresser, S. Fox, R. Camicioli, B. Feagan, D.A. Mendon\u00e7a, S.H. Pasternak",
      "category": "Undergraduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "THE EFFECTS OF 78-WEEK TREATMENT WITH AMBROXOL ON COGNITIVE, MOTOR, AND NEUROPSYCHIATRIC SYMPTOMS IN PARKINSON\u2019S DISEASE DEMENTIA",
      "location": "O3 | 2:12 \u2013 2:21 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-19",
      "title": "An Exploratory Analysis of the Prognostic Significance of Serum Neurofilament Light Chain for Disability Progression and Treatment Outcomes in Multiple Sclerosis: A Retrospective Cohort Study",
      "presenting_author": "Bhuvna Dalal",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Undergraduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "",
      "location": "O3 | 2:21 \u2013 2:30 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-2",
      "title": "Evaluating the Dear MD to Be Podcast as an Equity, Diversity, and Inclusion Resource: A Cross-Sectional Survey Analysis",
      "presenting_author": "Happy Inibhunu",
      "presenting_author_email": "",
      "co_authors": "I. Kherani, C. Osei-Yeboah, M. Bushra, M. Mahendiran, M. Mylopoulos, and M. Law",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "Evaluating the Dear MD to Be Podcast as an Equity, Diversity, and Inclusion Resource: A Cross-Sectional Survey Analysis",
      "location": "O1 | 9:49 - 9:58 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-20",
      "title": "THE EFFECTS OF 78-WEEK TREATMENT WITH AMBROXOL ON COGNITIVE, MOTOR, AND NEUROPSYCHIATRIC SYMPTOMS IN PARKINSON\u2019S DISEASE DEMENTIA",
      "presenting_author": "Carolina Silveira",
      "presenting_author_email": "",
      "co_authors": "A. Thurairajah, D. Bansal, D. Steven, K. MacDougall, J. Burneo, A. Suller-Marti, Western Epilepsy Research Group, A. Khan, J. Lau",
      "category": "Faculty/Staff",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "Thalamic microstructural changes in focal epilepsy identified using 7T MRI",
      "location": "O3 | 2:30 \u2013 2:39 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-21",
      "title": "A Containerized, Tissue-Resolved Pipeline for Reproducible Biomarker Extraction in Resting-State fMRI for Epilepsy",
      "presenting_author": "Dilanjan Diyabalanage",
      "presenting_author_email": "",
      "co_authors": "A. Soni, J. Burneo",
      "category": "Graduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "Status Epilepticus Management in Resource-limited Settings: An International Expert Survey",
      "location": "O3 | 2:39 \u2013 2:48 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-22",
      "title": "Thalamic microstructural changes in focal epilepsy identified using 7T MRI",
      "presenting_author": "Derek George",
      "presenting_author_email": "",
      "co_authors": "MC Burbano, A Ahmadi, H Kreinter, G Pellegrino, JG Burneo, ML Jones, KW MacDougall, JC Lau, DA Steven, D Diosy, A Suller Marti",
      "category": "Fellow",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "Electrophysiological Signatures of SEEG After Radiofrequency Ablation: Clinical Interpretation",
      "location": "O3 | 2:48 \u2013 2:57 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-23",
      "title": "Status Epilepticus Management in Resource-limited Settings: An International Expert Survey",
      "presenting_author": "Grace Couper",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Faculty/Staff",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "",
      "location": "O3 | 2:57 \u2013 3:06 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-24",
      "title": "Electrophysiological Signatures of SEEG After Radiofrequency Ablation: Clinical Interpretation",
      "presenting_author": "Iv\u00e1n Castro",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Fellow",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "",
      "location": "O3 | 3:06 \u2013 3:15 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-3",
      "title": "A National Quality Assessment of Headache Medicine Fellowship Training Programs in Canada",
      "presenting_author": "Jihad Al Kharbooshi",
      "presenting_author_email": "",
      "co_authors": "N/A",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "A National Quality Assessment of Headache Medicine Fellowship Training Programs in Canada",
      "location": "O1 | 9:58 - 10:07 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-4",
      "title": "DBS-Induced Blood\u2013Brain Barrier Dysfunction: A Dynamic Contrast-Enhanced MRI Pilot Study",
      "presenting_author": "Brendan Santyr",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Resident",
      "presentation_format": "Oral presentation",
      "training_level": "resident",
      "abstract_text": "",
      "location": "O2 | 11:15 - 11:24 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-5",
      "title": "Quantifying Neural Excitability in Epilepsy Using Resting-State EEG: A Quantum-Inspired Approach",
      "presenting_author": "Steven Li",
      "presenting_author_email": "",
      "co_authors": "A. Taha, A. Thurairajah, D. Bansal, V. Liu, A. R. Khan, K. W. MacDougall, A. G. Parrent",
      "category": "Graduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "Comparative evaluation of machine learning models for automatic detection of the caudal zona incerta for surgical planning",
      "location": "O2 | 11:24 - 11:33 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-6",
      "title": "Comparative evaluation of machine learning models for automatic detection of the caudal zona incerta for surgical planning",
      "presenting_author": "Jaime Thrower",
      "presenting_author_email": "",
      "co_authors": "J. Lombardi, A. Staffaroni, J. Rohrer, B. Boeve, A. Boxer, H. Rosen, S. Lee, E. Finger, on behalf of Frontotemporal Dementia Prevention Initiative Investigators",
      "category": "Undergraduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "Longitudinal trajectories of neurodevelopmental and neurodegenerative outcomes in genetic frontotemporal degeneration",
      "location": "O2 | 11:33 \u2013 11:42 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-7",
      "title": "Longitudinal trajectories of neurodevelopmental and neurodegenerative outcomes in genetic frontotemporal degeneration",
      "presenting_author": "Isis So",
      "presenting_author_email": "",
      "co_authors": "D. Johnston, R. Kanji, S. Leighton, J. Kelly, J. Ronald, M. Hebb, S. Penuela",
      "category": "Graduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "Disrupting Pannexin 1 Signalling Suppresses Glioblastoma Growth",
      "location": "O2 | 11:42 \u2013 11:51 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-8",
      "title": "Disrupting Pannexin 1 Signalling Suppresses Glioblastoma Growth",
      "presenting_author": "Matthew Huver",
      "presenting_author_email": "",
      "co_authors": "Diana Ayan, Lakni Abeyesekera, Eduardo Soriano Navarro, Arturo Gonzalez Lara, Jaime Rodriguez Orozco, Zahra Mirza Asgari, Lauren Mai, Sebastian Fridman, Antonio Arauz, Rodrigo Bagur, Luciano A. Sposato",
      "category": "Graduate Student",
      "presentation_format": "Oral presentation",
      "training_level": "student",
      "abstract_text": "International, Multicentre, Real-World Data on PFO and Recurrent Ischemic Stroke in Young Adults: Results From the IMPROVE Registry",
      "location": "O2 | 11:51 \u2013 12:00 | Kenny Theatre"
    },
    {
      "abstract_number": "PLAT-9",
      "title": "International, Multicentre, Real-World Data on PFO and Recurrent Ischemic Stroke in Young Adults: Results From the IMPROVE Registry",
      "presenting_author": "Fawaz Alotaibi",
      "presenting_author_email": "",
      "co_authors": "B. Corrigan, R. Johnston, R. Gulli, A. Sachs, J. Lau, J. Martinez-Trujillo",
      "category": "Fellow",
      "presentation_format": "Oral presentation",
      "training_level": "fellow",
      "abstract_text": "Decoding Cognitive and Oculomotor Signals from Prefrontal Cortex Neural Ensembles During Naturalistic Behavior",
      "location": "O2 | 12:00 \u2013 12:09 | Kenny Theatre"
    },
    {
      "abstract_number": "POST-1",
      "title": "Left Atrial Volume Index Changes After Patent Foramen Ovale Closure for Secondary Stroke Prevention: A Potential Explanation for Increased Risk of Atrial Fibrillation",
      "presenting_author": "Robin Sawaya",
      "presenting_author_email": "",
      "co_authors": "Liberman F., Vargas Gonzalez J., Diamantopoulos P., Blissett S., Bagur R, Sposato L.",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Left Atrial Volume Index Changes After Patent Foramen Ovale Closure for Secondary Stroke Prevention: A Potential Explanation for Increased Risk of Atrial Fibrillation",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-10",
      "title": "A Personalized Summary Sheet Improves Patient Understanding and Reduces Anxiety in Multiple Sclerosis: Preliminary Results of the MANGOES Quality Improvement Initiative",
      "presenting_author": "Sydney Cao",
      "presenting_author_email": "",
      "co_authors": "D. Ayan, F. Alotaibi, E. Soriano Navarro, F. Liberman, A. Gonzalez Lara, J. Rodriguez Orozco, Z. Mirza Asgari, L. Mai, S. Fridman, R. Bagur, M. Ahmed, N. Paul, L. A. Sposato",
      "category": "Undergraduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Segmental Left Atrial Appendage Opacification: A Novel CT Imaging Biomarker for Individualized Stroke Phenotyping in Patients with and without Atrial Fibrillation",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-11",
      "title": "Real-World Performance of Automated MRI Lesion Detection Programs in Focal Epilepsy",
      "presenting_author": "Michelle Li",
      "presenting_author_email": "",
      "co_authors": "R. Rios-Carrillo, K. Coleman, E. Finger, C. Baron",
      "category": "Undergraduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Microscopic fractional anisotropy differences in genetic frontotemporal degeneration",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-12",
      "title": "Segmental Left Atrial Appendage Opacification: A Novel CT Imaging Biomarker for Individualized Stroke Phenotyping in Patients with and without Atrial Fibrillation",
      "presenting_author": "Lakni Abeyesekera",
      "presenting_author_email": "",
      "co_authors": "C. Burbano,\u00a0 I. Castro, H. Kreinter, G. Pellegrino, J. Burneo, M. Jones, K. MacDougall, J. Lau, D. Steven, D. Diosy",
      "category": "Undergraduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Changes in Local and Network Brain Activity Across Repeated SEEG-Guided Thermocoagulation in Drug-Resistant Epilepsy",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-13",
      "title": "Microscopic fractional anisotropy differences in genetic frontotemporal degeneration",
      "presenting_author": "Isis So",
      "presenting_author_email": "",
      "co_authors": "-",
      "category": "Graduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Ondine\u2019s Curse (Central Hypoventilation Syndrome) as the Presenting Manifestation of Diffuse Midline Glioma",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-14",
      "title": "Changes in Local and Network Brain Activity Across Repeated SEEG-Guided Thermocoagulation in Drug-Resistant Epilepsy",
      "presenting_author": "Ahdyie Ahmadi",
      "presenting_author_email": "",
      "co_authors": "J. Clarke, M. Strong",
      "category": "Faculty/Staff",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Extraneuronal TAR DNA-Binding Protein 43/SARS-CoV-2 N Protein Condensates in Amyotrophic Lateral Sclerosis",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-15",
      "title": "Ondine\u2019s Curse (Central Hypoventilation Syndrome) as the Presenting Manifestation of Diffuse Midline Glioma",
      "presenting_author": "Bhuvna Dalal",
      "presenting_author_email": "",
      "co_authors": "H. Minhas, J. Tran, V. Zeynalli, Z. Raza, P. Parikh, J. Atton, J. Mohamad, Y. Lin, K. Dwyer, C.S. Casserly",
      "category": "Undergraduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Improving the Identification and Documentation of Non-Motor Symptoms in Patients with Multiple Sclerosis: A Quality Improvement Study",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-16",
      "title": "Extraneuronal TAR DNA-Binding Protein 43/SARS-CoV-2 N Protein Condensates in Amyotrophic Lateral Sclerosis",
      "presenting_author": "Alexandra Keating",
      "presenting_author_email": "",
      "co_authors": "B. Brower, H. Lee, L. Ang, E. Finger, Q. Zhang",
      "category": "Undergraduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Correlating Post-mortem Gross Macroscopy with Histopathological Findings in the Caudate Nucleus in Frontotemporal Lobar Degeneration",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-17",
      "title": "Improving the Identification and Documentation of Non-Motor Symptoms in Patients with Multiple Sclerosis: A Quality Improvement Study",
      "presenting_author": "Ariela Jamshidi-Shahvar",
      "presenting_author_email": "",
      "co_authors": "Z. Alfares, A. Svendrovski, B. Ciftci, J. Racosta, P. Riccio, C. Casserly",
      "category": "Medical Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Real-World Association Between Serum Neurofilament Light Chain and MRI-Defined Disease Activity in Multiple Sclerosis",
      "location": "P1B | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-18",
      "title": "Correlating Post-mortem Gross Macroscopy with Histopathological Findings in the Caudate Nucleus in Frontotemporal Lobar Degeneration",
      "presenting_author": "Shervin Pejhan",
      "presenting_author_email": "",
      "co_authors": "S. Vuyyuru, P. Riccio, J. Racosta, C. Casserly, V. Jairath, B. Ciftci",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Treatment Outcomes of Advanced Combination Therapy in Multiple Sclerosis-Inflammatory Bowel Disease Overlap: A retrospective Single-Centre case series",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-19",
      "title": "Real-World Association Between Serum Neurofilament Light Chain and MRI-Defined Disease Activity in Multiple Sclerosis",
      "presenting_author": "Azhar Alanazi",
      "presenting_author_email": "",
      "co_authors": "A. Akbarpour, D. Adil, A. Thurairajah, A. Skovronska, M. Kregel, R. Eagleson, M.N. Nouri, A. Andrade, and S. de Ribaupierre",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Pediatric epilepsy surgery following stereoelectroencephalography: multi-level data on clinical factors and electrode contact-brain tissue sampling representation",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-2",
      "title": "Optimizing Response to Status Epilepticus in the Epilepsy Monitoring Unit: A Quality Improvement Initiative",
      "presenting_author": "Sarah Alotaibi",
      "presenting_author_email": "",
      "co_authors": "A. Florence-Cumbermack, D. Hudson",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Optimizing Response to Status Epilepticus in the Epilepsy Monitoring Unit: A Quality Improvement Initiative",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-20",
      "title": "Treatment Outcomes of Advanced Combination Therapy in Multiple Sclerosis-Inflammatory Bowel Disease Overlap: A retrospective Single-Centre case series",
      "presenting_author": "Azhar Alanazi",
      "presenting_author_email": "",
      "co_authors": "C. Burbano, I. Castro, J. Burneo, G. Pellegrino, M. Lee-Jones, JC. Lau, DA. Steven, KW. MacDougall, D. Diosy, A. Suller-Marti",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Use of Responsive Neurostimulation Beyond the U.S.: International Experience and Outcomes",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-21",
      "title": "Pediatric epilepsy surgery following stereoelectroencephalography: multi-level data on clinical factors and electrode contact-brain tissue sampling representation",
      "presenting_author": "Kevin Paul Ferraris",
      "presenting_author_email": "",
      "co_authors": "A.J. Appleton, W.A. Fisher, S.N. Whitehead, J.K. Shoemaker, V Hachinski.",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "The CanDo Brain Health Implementation Initiative",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-22",
      "title": "Use of Responsive Neurostimulation Beyond the U.S.: International Experience and Outcomes",
      "presenting_author": "Natalia Valencia-Enciso",
      "presenting_author_email": "",
      "co_authors": "J. Houpy, Y. Li, C. Howlett, L. Ang, J. Megyesi",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Erdheim-Chester Disease Presenting as a Subdural Hematoma",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-23",
      "title": "The CanDo Brain Health Implementation Initiative",
      "presenting_author": "Abolfazl Avan",
      "presenting_author_email": "",
      "co_authors": "Diana Ayan, Lakni Abeyesekera, Eduardo Soriano Navarro, Arturo Gonzalez Lara, Jaime Rodriguez Orozco, Zahra Mirza Asgari, Lauren Mai, Sebastian Fridman, Antonio Arauz, Rodrigo Bagur, Luciano A. Sposato",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Low Risk of Ischemic Stroke Recurrence in Young Adults with TIA and PFO: Results From the IMPROVE International Registry",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-24",
      "title": "Erdheim-Chester Disease Presenting as a Subdural Hematoma",
      "presenting_author": "Waseem Yaghmoor",
      "presenting_author_email": "",
      "co_authors": "N. Fulcher, S. Schmid, T. Peters, E. Wong, M.O. Hebb",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Preclinical Safety and Efficacy of Intracranial Electrotherapy for Glioma Treatment",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-25",
      "title": "Low Risk of Ischemic Stroke Recurrence in Young Adults with TIA and PFO: Results From the IMPROVE International Registry",
      "presenting_author": "Fawaz Alotaibi",
      "presenting_author_email": "",
      "co_authors": "M. Elnazali",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "Effectiveness and stimulation parameters of transcutaneous vagus nerve stimulation in patients with epilepsy: a systematic review",
      "location": "P2C | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-26",
      "title": "Preclinical Safety and Efficacy of Intracranial Electrotherapy for Glioma Treatment",
      "presenting_author": "Erin Iredale",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Fellow",
      "presentation_format": "Poster presentation",
      "training_level": "fellow",
      "abstract_text": "",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-27",
      "title": "Effectiveness and stimulation parameters of transcutaneous vagus nerve stimulation in patients with epilepsy: a systematic review",
      "presenting_author": "Sydney Papadopoulos",
      "presenting_author_email": "",
      "co_authors": "M. Poon, A. Mastrolonardo, S. De Ribaupierre, C. Cacciotti",
      "category": "Medical Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Medulloblastoma in Two Infants with Gorlin Syndrome",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-28",
      "title": "Quasi-Instantaneous Neural Excitability (QINe): A Multiscale fMRI Framework for Characterizing Normative Cortical Dynamics in Healthy Cohorts",
      "presenting_author": "Dilanjan Diyabalanage",
      "presenting_author_email": "",
      "co_authors": "K. Volkening, C. McLellan, T. Balci, C. Shoesmith, M. Strong",
      "category": "Graduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Resolving Variants of Uncertain Significance in ALS through Integrated In Silico and Functional Approaches",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-29",
      "title": "Medulloblastoma in Two Infants with Gorlin Syndrome",
      "presenting_author": "Oviya Ananthakrishnan",
      "presenting_author_email": "",
      "co_authors": "Dr. A. Mastrolonardo, Dr. A. Mascarenhas",
      "category": "Medical Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Management of GSA: Case Report and Systematic Review of Treatment Strategies",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-3",
      "title": "Clinical and Molecular Features of Biomarker Shifting in Breast Cancer Brain Metastases",
      "presenting_author": "Ryan Wang",
      "presenting_author_email": "",
      "co_authors": "R. Abdo, Q. Zhang, J. Megyesi",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Clinical and Molecular Features of Biomarker Shifting in Breast Cancer Brain Metastases",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-30",
      "title": "Resolving Variants of Uncertain Significance in ALS through Integrated In Silico and Functional Approaches",
      "presenting_author": "Minhal Ahmed",
      "presenting_author_email": "",
      "co_authors": "V. Smye, W. Koopman",
      "category": "Medical Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "Navigating The Unknown: Exploring the Lived Experiences of Persons Newly Diagnosed with Multiple Sclerosis in Canada",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-31",
      "title": "Impact of Alzheimer\u2019s Disease Co-Pathology on Shunt Outcomes in Idiopathic Normal Pressure Hydrocephalus: A Systematic Review and Meta-Analysis",
      "presenting_author": "Mojtaba Sharafkhah",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Graduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-32",
      "title": "Management of GSA: Case Report and Systematic Review of Treatment Strategies",
      "presenting_author": "Khushali Parikh",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Medical Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-33",
      "title": "Navigating The Unknown: Exploring the Lived Experiences of Persons Newly Diagnosed with Multiple Sclerosis in Canada",
      "presenting_author": "Saba Hyarat",
      "presenting_author_email": "",
      "co_authors": "",
      "category": "Graduate Student",
      "presentation_format": "Poster presentation",
      "training_level": "student",
      "abstract_text": "",
      "location": "P2D | 3:20 - 4:08 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-4",
      "title": "Advancements in Robotic-Assisted Cervical Spine Fixation",
      "presenting_author": "Happy Inibhunu",
      "presenting_author_email": "",
      "co_authors": "S. Detombe, R. Bartha, N. Duggal",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Longitudinal Assessment of Motor Cortical Activity and Hand Dexterity in Degenerative Cervical Myelopathy Patients Using Functional MRI",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-5",
      "title": "Endovascular considerations in managing neurovascular manifestations of connective tissue disorders",
      "presenting_author": "Priscilla Chan",
      "presenting_author_email": "",
      "co_authors": "B. Santyr, D. Lee, B. Rotenberg, L. Sowerby, N. Duggal",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Portable intraoperative MRI during endoscopic endonasal pituitary adenoma resection: an early institutional experience",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-6",
      "title": "Longitudinal Assessment of Motor Cortical Activity and Hand Dexterity in Degenerative Cervical Myelopathy Patients Using Functional MRI",
      "presenting_author": "Dickson Wong",
      "presenting_author_email": "",
      "co_authors": "R. Ragguett, B. Santyr, W. Ng",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Minimally Invasive Approach for Subdural Hematoma",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-7",
      "title": "Portable intraoperative MRI during endoscopic endonasal pituitary adenoma resection: an early institutional experience",
      "presenting_author": "Mohammad Alostad",
      "presenting_author_email": "",
      "co_authors": "SP. Lownie",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Comparison of Outcomes Between Retrosigmoid and Translabyrinthine Approaches for Vestibular Schwannoma Resection",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-8",
      "title": "Minimally Invasive Approach for Subdural Hematoma",
      "presenting_author": "Rana Moshref",
      "presenting_author_email": "",
      "co_authors": "A. Alanazi, J. Arocha Perez, Z. Alfares",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "A Personalized Summary Sheet Improves Patient Understanding and Reduces Anxiety in Multiple Sclerosis: Preliminary Results of the MANGOES Quality Improvement Initiative",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    },
    {
      "abstract_number": "POST-9",
      "title": "Comparison of Outcomes Between Retrosigmoid and Translabyrinthine Approaches for Vestibular Schwannoma Resection",
      "presenting_author": "Alexander Mastrolonardo",
      "presenting_author_email": "",
      "co_authors": "G. Pellegrino",
      "category": "Resident",
      "presentation_format": "Poster presentation",
      "training_level": "resident",
      "abstract_text": "Real-World Performance of Automated MRI Lesion Detection Programs in Focal Epilepsy",
      "location": "P1A | 10:15 - 11:10 | Garron/Spriet Lounge"
    }
  ],
  "judges": [
    {
      "email": "Alexander.Khaw@lhsc.on.ca",
      "name": "Alexander Khaw",
      "affiliation": ""
    },
    {
      "email": "Beyza.Ciftci@lhsc.on.ca",
      "name": "Beyza Ciftci",
      "affiliation": ""
    },
    {
      "email": "cwatling@royalcollege.ca",
      "name": "Chris Watling",
      "affiliation": ""
    },
    {
      "email": "Deepa.Dash@lhsc.on.ca",
      "name": "Deepa Dash",
      "affiliation": ""
    },
    {
      "email": "Joseph.Megyesi@lhsc.on.ca",
      "name": "Joseph Megyesi",
      "affiliation": ""
    },
    {
      "email": "judge1@example.com",
      "name": "Judge 1",
      "affiliation": "CNS Faculty"
    },
    {
      "email": "judge2@example.com",
      "name": "Judge 2",
      "affiliation": "CNS Faculty"
    },
    {
      "email": "judge3@example.com",
      "name": "Judge 3",
      "affiliation": "CNS Faculty"
    },
    {
      "email": "judge4@example.com",
      "name": "Judge 4",
      "affiliation": "CNS Faculty"
    },
    {
      "email": "Robert.Hammond@lhsc.on.ca",
      "name": "Robert Hammond",
      "affiliation": ""
    },
    {
      "email": "Yiu-Chia.Chang@lhsc.on.ca",
      "name": "Yiu-Chia Chang",
      "affiliation": ""
    }
  ],
  "assignments": [
    {
      "judge_email": "judge1@example.com",
      "abstract_number": "PLAT-1"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-1"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-1"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-1"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-10"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-10"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-10"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-11"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-11"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-11"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-12"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-12"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-12"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-13"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-13"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-13"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-14"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-14"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-14"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-15"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-15"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-15"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-16"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-16"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-16"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-17"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-17"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-17"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-18"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-18"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-18"
    },
    {
      "judge_email": "judge1@example.com",
      "abstract_number": "PLAT-2"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-2"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-2"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-2"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-20"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-20"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-20"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-21"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-21"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-21"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-22"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-22"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-22"
    },
    {
      "judge_email": "judge1@example.com",
      "abstract_number": "PLAT-3"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-3"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-3"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-3"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-5"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-5"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-5"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-6"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-6"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-6"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-7"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-7"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-7"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-8"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-8"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-8"
    },
    {
      "judge_email": "cwatling@royalcollege.ca",
      "abstract_number": "PLAT-9"
    },
    {
      "judge_email": "Robert.Hammond@lhsc.on.ca",
      "abstract_number": "PLAT-9"
    },
    {
      "judge_email": "Alexander.Khaw@lhsc.on.ca",
      "abstract_number": "PLAT-9"
    },
    {
      "judge_email": "judge1@example.com",
      "abstract_number": "POST-1"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-1"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-1"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-10"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-10"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-11"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-11"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-12"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-12"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-13"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-13"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-14"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-14"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-15"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-15"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-16"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-16"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-17"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-17"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-18"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-18"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-19"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-19"
    },
    {
      "judge_email": "judge1@example.com",
      "abstract_number": "POST-2"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-2"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-2"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-20"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-20"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-21"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-21"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-22"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-22"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-23"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-23"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-24"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-24"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-25"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-25"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-27"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-27"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-28"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-28"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-29"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-29"
    },
    {
      "judge_email": "judge1@example.com",
      "abstract_number": "POST-3"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-3"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-3"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-30"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-30"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-4"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-4"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-5"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-5"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-6"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-6"
    },
    {
      "judge_email": "Yiu-Chia.Chang@lhsc.on.ca",
      "abstract_number": "POST-7"
    },
    {
      "judge_email": "Beyza.Ciftci@lhsc.on.ca",
      "abstract_number": "POST-7"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-8"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-8"
    },
    {
      "judge_email": "Deepa.Dash@lhsc.on.ca",
      "abstract_number": "POST-9"
    },
    {
      "judge_email": "Joseph.Megyesi@lhsc.on.ca",
      "abstract_number": "POST-9"
    }
  ],
  "events": [
    {
      "name": "CNS Research Day 2026",
      "date": "2026-05-14",
      "is_active": true
    }
  ],
  "rubrics": [
    {
      "presentation_format": "Oral presentation",
      "is_active": true,
      "items": [
        {
          "label": "Scientific question",
          "description": "Is the research question clear, relevant, and important?",
          "max_score": 5,
          "sort_order": 1
        },
        {
          "label": "Methods",
          "description": "Are design and analyses appropriate?",
          "max_score": 5,
          "sort_order": 2
        },
        {
          "label": "Results",
          "description": "Are results clear and complete?",
          "max_score": 5,
          "sort_order": 3
        },
        {
          "label": "Interpretation",
          "description": "Are conclusions supported by data?",
          "max_score": 5,
          "sort_order": 4
        },
        {
          "label": "Slide quality",
          "description": "Are slides readable and organized?",
          "max_score": 5,
          "sort_order": 5
        },
        {
          "label": "Delivery",
          "description": "Was delivery clear and confident?",
          "max_score": 5,
          "sort_order": 6
        },
        {
          "label": "Timing",
          "description": "Was time used appropriately?",
          "max_score": 5,
          "sort_order": 7
        },
        {
          "label": "Response to questions",
          "description": "Did presenter answer thoughtfully?",
          "max_score": 5,
          "sort_order": 8
        },
        {
          "label": "Overall impression",
          "description": "Overall quality of research and presentation.",
          "max_score": 5,
          "sort_order": 9
        }
      ]
    },
    {
      "presentation_format": "Poster presentation",
      "is_active": true,
      "items": [
        {
          "label": "Scientific question",
          "description": "Is the research question clear, relevant, and important?",
          "max_score": 5,
          "sort_order": 1
        },
        {
          "label": "Methods",
          "description": "Are design and analyses appropriate?",
          "max_score": 5,
          "sort_order": 2
        },
        {
          "label": "Results",
          "description": "Are results clear and complete?",
          "max_score": 5,
          "sort_order": 3
        },
        {
          "label": "Interpretation",
          "description": "Are conclusions supported by data?",
          "max_score": 5,
          "sort_order": 4
        },
        {
          "label": "Poster design",
          "description": "Is the poster readable and well organized?",
          "max_score": 5,
          "sort_order": 5
        },
        {
          "label": "Verbal explanation",
          "description": "Did presenter explain clearly?",
          "max_score": 5,
          "sort_order": 6
        },
        {
          "label": "Response to questions",
          "description": "Did presenter answer thoughtfully?",
          "max_score": 5,
          "sort_order": 7
        },
        {
          "label": "Overall impression",
          "description": "Overall quality of research and presentation.",
          "max_score": 5,
          "sort_order": 8
        }
      ]
    }
  ]
}
""")


class Command(BaseCommand):
    help = "One-time load of CNS Research Day 2026 event data (submissions, judges, assignments, rubrics)"

    def handle(self, *args, **options):
        from judging.models import Category, Event, Judge, JudgeAssignment, PresentationFormat, Rubric, RubricItem, Submission

        data = _DATA

        # Event
        event_data = data["events"][0]
        event, _ = Event.objects.get_or_create(
            name=event_data["name"],
            defaults={"date": event_data["date"], "is_active": event_data["is_active"]},
        )
        self.stdout.write(f"Event: {event.name}")

        # Rubrics
        for r_data in data["rubrics"]:
            fmt, _ = PresentationFormat.objects.get_or_create(name=r_data["presentation_format"])
            rubric, created = Rubric.objects.get_or_create(
                event=event,
                presentation_format=fmt,
                defaults={"is_active": r_data["is_active"]},
            )
            if created:
                for item in r_data["items"]:
                    RubricItem.objects.create(
                        rubric=rubric,
                        label=item["label"],
                        description=item["description"],
                        max_score=item["max_score"],
                        sort_order=item["sort_order"],
                    )
                self.stdout.write(f"Rubric created: {fmt.name} ({len(r_data['items'])} items)")
            else:
                self.stdout.write(f"Rubric exists: {fmt.name}")

        # Submissions
        sub_created = sub_updated = 0
        for row in data["submissions"]:
            cat, _ = Category.objects.get_or_create(event=event, name=row["category"])
            fmt, _ = PresentationFormat.objects.get_or_create(name=row["presentation_format"])
            _, created = Submission.objects.update_or_create(
                event=event,
                abstract_number=row["abstract_number"],
                defaults={
                    "title": row["title"],
                    "presenting_author": row["presenting_author"],
                    "presenting_author_email": row.get("presenting_author_email", ""),
                    "co_authors": row["co_authors"],
                    "category": cat,
                    "presentation_format": fmt,
                    "training_level": row["training_level"],
                    "abstract_text": row["abstract_text"],
                    "location": row["location"],
                },
            )
            if created:
                sub_created += 1
            else:
                sub_updated += 1
        self.stdout.write(f"Submissions: {sub_created} created, {sub_updated} updated")

        # Judges
        j_created = j_updated = 0
        for row in data["judges"]:
            _, created = Judge.objects.update_or_create(
                event=event,
                email=row["email"],
                defaults={"name": row["name"], "affiliation": row["affiliation"]},
            )
            if created:
                j_created += 1
            else:
                j_updated += 1
        self.stdout.write(f"Judges: {j_created} created, {j_updated} updated")

        # Assignments
        a_created = a_skipped = 0
        for row in data["assignments"]:
            judge = Judge.objects.filter(event=event, email=row["judge_email"]).first()
            submission = Submission.objects.filter(event=event, abstract_number=row["abstract_number"]).first()
            if not judge or not submission:
                a_skipped += 1
                continue
            _, created = JudgeAssignment.objects.get_or_create(
                event=event, judge=judge, submission=submission,
            )
            if created:
                a_created += 1
        self.stdout.write(f"Assignments: {a_created} created, {a_skipped} skipped")

        # Substitute presenters — not eligible for awards
        non_competing = ["PLAT-5", "POST-1", "POST-15"]
        updated = Submission.objects.filter(event=event, abstract_number__in=non_competing).update(award_eligible=False)
        self.stdout.write(f"Marked {updated} submission(s) as not award-eligible: {', '.join(non_competing)}")

        self.stdout.write(self.style.SUCCESS("Done."))
