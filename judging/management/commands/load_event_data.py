from django.core.management.base import BaseCommand
import json

_DATA = json.loads(r"""
{
  "submissions": [
    {"abstract_number":"PLAT-1","title":"Surgical residency attrition in Canada - Trainee Perspectives on leaving surgical training","presenting_author":"Amirti Vivekanandan","co_authors":"A. Sepulveda, K. Squires, S. Singh, K. MacDougall, A. Harvey, S. Lopushinsky, O. Daodu","category":"Resident","presentation_format":"Oral presentation","training_level":"resident","location":"O1 | 9:40 - 9:49 | Kenny Theatre"},
    {"abstract_number":"PLAT-2","title":"Evaluating the Dear MD to Be Podcast as an Equity, Diversity, and Inclusion Resource: A Cross-Sectional Survey Analysis","presenting_author":"Happy Inibhunu","co_authors":"I. Kherani, C. Osei-Yeboah, M. Bushra, M. Mahendiran, M. Mylopoulos, and M. Law","category":"Resident","presentation_format":"Oral presentation","training_level":"resident","location":"O1 | 9:49 - 9:58 | Kenny Theatre"},
    {"abstract_number":"PLAT-3","title":"A National Quality Assessment of Headache Medicine Fellowship Training Programs in Canada","presenting_author":"Jihad Al Kharbooshi","co_authors":"N/A","category":"Resident","presentation_format":"Oral presentation","training_level":"resident","location":"O1 | 9:58 - 10:07 | Kenny Theatre"},
    {"abstract_number":"PLAT-5","title":"Comparative evaluation of machine learning models for automatic detection of the caudal zona incerta for surgical planning","presenting_author":"Jaime Thrower","co_authors":"A. Taha, A. Thurairajah, D. Bansal, V. Liu, A. R. Khan, K. W. MacDougall, A. G. Parrent","category":"Undergraduate Student","presentation_format":"Oral presentation","training_level":"student","location":"O2 | 11:24 – 11:33 | Kenny Theatre"},
    {"abstract_number":"PLAT-6","title":"Longitudinal trajectories of neurodevelopmental and neurodegenerative outcomes in genetic frontotemporal degeneration","presenting_author":"Isis So","co_authors":"J. Lombardi, A. Staffaroni, J. Rohrer, B. Boeve, A. Boxer, H. Rosen, S. Lee, E. Finger, on behalf of Frontotemporal Dementia Prevention Initiative Investigators","category":"Graduate Student","presentation_format":"Oral presentation","training_level":"student","location":"O2 | 11:42 – 11:51 | Kenny Theatre"},
    {"abstract_number":"PLAT-7","title":"Disrupting Pannexin 1 Signalling Suppresses Glioblastoma Growth","presenting_author":"Matthew Huver","co_authors":"D. Johnston, R. Kanji, S. Leighton, J. Kelly, J. Ronald, M. Hebb, S. Penuela","category":"Graduate Student","presentation_format":"Oral presentation","training_level":"student","location":"O2 | 11:51 – 12:00 | Kenny Theatre"},
    {"abstract_number":"PLAT-8","title":"International, Multicentre, Real-World Data on PFO and Recurrent Ischemic Stroke in Young Adults: Results From the IMPROVE Registry","presenting_author":"Fawaz Alotaibi","co_authors":"Diana Ayan, Lakni Abeyesekera, Eduardo Soriano Navarro, Arturo Gonzalez Lara, Jaime Rodriguez Orozco, Zahra Mirza Asgari, Lauren Mai, Sebastian Fridman, Antonio Arauz, Rodrigo Bagur, Luciano A. Sposato","category":"Clinical Fellow","presentation_format":"Oral presentation","training_level":"fellow","location":"O2 | 12:00 – 12:09 | Kenny Theatre"},
    {"abstract_number":"PLAT-9","title":"Decoding Cognitive and Oculomotor Signals from Prefrontal Cortex Neural Ensembles During Naturalistic Behavior","presenting_author":"Mohamad Abbass","co_authors":"B. Corrigan, R. Johnston, R. Gulli, A. Sachs, J. Lau, J. Martinez-Trujillo","category":"Resident","presentation_format":"Oral presentation","training_level":"resident","location":"O3 | 11:15 – 11:24 | Kenny Theatre"},
    {"abstract_number":"PLAT-10","title":"Outcomes of Valproic Acid Withdrawal in Females Before or During Pregnancy: A Systematic Review and Meta-analysis","presenting_author":"Maria Claudia Burbano Donoso","co_authors":"R.G. Couper, P.H. Espino, J.G. Burneo","category":"Research Fellow","presentation_format":"Oral presentation","training_level":"fellow","location":"O2 | 12:09 – 12:18 | Kenny Theatre"},
    {"abstract_number":"PLAT-11","title":"Association Between Serum Neurofilament Light Chain Levels and MRI Activity Across Disability Levels and Treatment Contexts in Multiple Sclerosis","presenting_author":"Zainab Alfares","co_authors":"A. Alanazi, A. Svendrovski, B. Ciftci, J. Racosta, P. Riccio, C. Casserly","category":"Clinical Fellow","presentation_format":"Oral presentation","training_level":"fellow","location":"O2 | 12:18 – 12:27 | Kenny Theatre"},
    {"abstract_number":"PLAT-12","title":"Structure-Function Coupling for Epileptogenic Zone Network Identification and Connectivity Analysis in Paediatric Focal Epilepsy","presenting_author":"Adetunji Oremakinde","co_authors":"R. Eagleson, A. Khan, G. Pellegrino","category":"Graduate Student","presentation_format":"Oral presentation","training_level":"student","location":"O2 | 12:27 – 12:36 | Kenny Theatre"},
    {"abstract_number":"PLAT-13","title":"Clinically Feasible pH-Weighted Imaging at University Hospital: A Proof-of-Concept Study","presenting_author":"Dickson Wong","co_authors":"S. Pandey, P. Malik, J. Megyesi, R. Bartha","category":"Resident","presentation_format":"Oral presentation","training_level":"resident","location":"O3 | 1:35 – 1:44 | Kenny Theatre"},
    {"abstract_number":"PLAT-14","title":"First Canadian Experience of Stroke Fellows Implanting Loop Recorders in Stroke Patients: Preliminary Results of the B2AD-Risk AFDAS Study","presenting_author":"Eduardo Soriano Navarro","co_authors":"A. Diana Ayan, B. Lakni Abeyesekera, C. Fawaz Alotaibi, D. Arturo Gonzalez Lara, E. Jaime Rodriguez Orozco, F. Zahra Mirza Asgari, G. Lorne Gula, H. Alan Skanes, I. Jason Andrade, J. Lauren Mai, K. Sebastian Fridman, L. Thalia Field, M. Michael Hill, N. Rodrigo Bagur, O. Luciano A. Sposato","category":"Clinical Fellow","presentation_format":"Oral presentation","training_level":"fellow","location":"O3 | 1:44 – 1:53 | Kenny Theatre"},
    {"abstract_number":"PLAT-15","title":"Reducing the Rate of Urinary Tract Infections (UTIs) on the Neurology Ward","presenting_author":"Trevor Jairam","co_authors":"David Hudson, Anita Florendo-Cumbermack","category":"Resident","presentation_format":"Oral presentation","training_level":"resident","location":"O3 | 1:53 – 2:02 | Kenny Theatre"},
    {"abstract_number":"PLAT-16","title":"Examining Cortical Excitability Using Magnetoencephalography","presenting_author":"Kevin Kim","co_authors":"G. Pellegrino","category":"Undergraduate Student","presentation_format":"Oral presentation","training_level":"student","location":"O3 | 11:33 – 11:42 | Kenny Theatre"},
    {"abstract_number":"PLAT-17","title":"An Exploratory Analysis of the Prognostic Significance of Serum Neurofilament Light Chain for Disability Progression and Treatment Outcomes in Multiple Sclerosis: A Retrospective Cohort Study","presenting_author":"Bhuvna Dalal","co_authors":"K. Dwyer, P. Riccio, J. Racosta, P. Malik, C. S. Casserly, A. Budhram, B. Ciftci","category":"Undergraduate Student","presentation_format":"Oral presentation","training_level":"student","location":"O3 | 2:02 – 2:11 | Kenny Theatre"},
    {"abstract_number":"PLAT-18","title":"THE EFFECTS OF 78-WEEK TREATMENT WITH AMBROXOL ON COGNITIVE, MOTOR, AND NEUROPSYCHIATRIC SYMPTOMS IN PARKINSON’S DISEASE DEMENTIA","presenting_author":"Carolina Silveira","co_authors":"K.K.L. Coleman, K. Borron, R.G. Tirona, C.A. Rupar, G. Zou, R.A. Hegele, E.C. Finger, R. Bartha, S.A. Morrow, J. Wells, M. Borrie, P.A. MacDonald, M.E. Jenkins, M.S. Jog, G. Dresser, S. Fox, R. Camicioli, B. Feagan, D.A. Mendonça, S.H. Pasternak","category":"Research Associate","presentation_format":"Oral presentation","training_level":"fellow","location":"O3 | 2:11 – 2:20 | Kenny Theatre"},
    {"abstract_number":"PLAT-20","title":"Thalamic microstructural changes in focal epilepsy identified using 7T MRI","presenting_author":"Derek George","co_authors":"A. Thurairajah, D. Bansal, D. Steven, K. MacDougall, J. Burneo, A. Suller-Marti, Western Epilepsy Research Group, A. Khan, J. Lau","category":"Research Fellow","presentation_format":"Oral presentation","training_level":"fellow","location":"O3 | 2:20 – 2:29 | Kenny Theatre"},
    {"abstract_number":"PLAT-21","title":"Status Epilepticus Management in Resource-limited Settings: An International Expert Survey","presenting_author":"Grace Couper","co_authors":"A. Soni, J. Burneo","category":"Research Associate","presentation_format":"Oral presentation","training_level":"fellow","location":"O3 | 2:29 – 2:38 | Kenny Theatre"},
    {"abstract_number":"PLAT-22","title":"Electrophysiological Signatures of SEEG After Radiofrequency Ablation: Clinical Interpretation","presenting_author":"Iván Castro","co_authors":"MC Burbano, A Ahmadi, H Kreinter, G Pellegrino, JG Burneo, ML Jones, KW MacDougall, JC Lau, DA Steven, D Diosy, A Suller Marti","category":"Clinical Fellow","presentation_format":"Oral presentation","training_level":"fellow","location":"O3 | 2:38 – 2:47 | Kenny Theatre"},
    {"abstract_number":"POST-1","title":"Left Atrial Volume Index Changes After Patent Foramen Ovale Closure for Secondary Stroke Prevention: A Potential Explanation for Increased Risk of Atrial Fibrillation","presenting_author":"Robin Sawaya","co_authors":"Liberman F., Vargas Gonzalez J., Diamantopoulos P., Blissett S., Bagur R, Sposato L.","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-2","title":"Optimizing Response to Status Epilepticus in the Epilepsy Monitoring Unit: A Quality Improvement Initiative","presenting_author":"Sarah Alotaibi","co_authors":"A. Khan, R. Zhou, A. Florence-Cumbermack, D. Hudson","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-3","title":"Clinical and Molecular Features of Biomarker Shifting in Breast Cancer Brain Metastases","presenting_author":"Ryan Wang","co_authors":"R. Abdo, Q. Zhang, J. Megyesi","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-4","title":"Longitudinal Assessment of Motor Cortical Activity and Hand Dexterity in Degenerative Cervical Myelopathy Patients Using Functional MRI","presenting_author":"Dickson Wong","co_authors":"S. Detombe, R. Bartha, N. Duggal","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-5","title":"Portable intraoperative MRI during endoscopic endonasal pituitary adenoma resection: an early institutional experience","presenting_author":"Mohammad Alostad","co_authors":"B. Santyr, D. Lee, B. Rotenberg, L. Sowerby, N. Duggal","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-6","title":"Minimally Invasive Approach for Subdural Hematoma","presenting_author":"Rana Moshref","co_authors":"R. Ragguett, B. Santyr, W. Ng","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-7","title":"Comparison of Outcomes Between Retrosigmoid and Translabyrinthine Approaches for Vestibular Schwannoma Resection","presenting_author":"Alexander Mastrolonardo","co_authors":"SP. Lownie","category":"Resident","presentation_format":"Poster presentation","training_level":"resident","location":"P1A | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-8","title":"A Personalized Summary Sheet Improves Patient Understanding and Reduces Anxiety in Multiple Sclerosis: Preliminary Results of the MANGOES Quality Improvement Initiative","presenting_author":"Sydney Cao","co_authors":"A. Alanazi, J. Arocha Perez, Z. Alfares","category":"Undergraduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-9","title":"Real-World Performance of Automated MRI Lesion Detection Programs in Focal Epilepsy","presenting_author":"Michelle Li","co_authors":"G. Pellegrino","category":"Undergraduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-10","title":"Segmental Left Atrial Appendage Opacification: A Novel CT Imaging Biomarker for Individualized Stroke Phenotyping in Patients with and without Atrial Fibrillation","presenting_author":"Lakni Abeyesekera","co_authors":"D. Ayan, F. Alotaibi, E. Soriano Navarro, F. Liberman, A. Gonzalez Lara, J. Rodriguez Orozco, Z. Mirza Asgari, L. Mai, S. Fridman, R. Bagur, M. Ahmed, N. Paul, L. A. Sposato","category":"Undergraduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-11","title":"Microscopic fractional anisotropy differences in genetic frontotemporal degeneration","presenting_author":"Isis So","co_authors":"R. Rios-Carrillo, K. Coleman, E. Finger, C. Baron","category":"Graduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-12","title":"Changes in Local and Network Brain Activity Across Repeated SEEG-Guided Thermocoagulation in Drug-Resistant Epilepsy","presenting_author":"Ahdyie Ahmadi","co_authors":"C. Burbano, I. Castro, H. Kreinter, G. Pellegrino, J. Burneo, M. Jones, K. MacDougall, J. Lau, D. Steven, D. Diosy","category":"Graduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-13","title":"Ondine’s Curse (Central Hypoventilation Syndrome) as the Presenting Manifestation of Diffuse Midline Glioma","presenting_author":"Bhuvna Dalal","co_authors":"M. Langford","category":"Undergraduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-14","title":"Extraneuronal TAR DNA-Binding Protein 43/SARS-CoV-2 N Protein Condensates in Amyotrophic Lateral Sclerosis","presenting_author":"Alexandra Keating","co_authors":"J. Clarke, M. Strong","category":"Undergraduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-15","title":"Improving the Identification and Documentation of Non-Motor Symptoms in Patients with Multiple Sclerosis: A Quality Improvement Study","presenting_author":"Ariela Jamshidi-Shahvar","co_authors":"H. Minhas, J. Tran, V. Zeynalli, Z. Raza, P. Parikh, J. Atton, J. Mohamad, Y. Lin, K. Dwyer, C.S. Casserly","category":"Medical Student","presentation_format":"Poster presentation","training_level":"student","location":"P1B | 10:15 - 11:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-16","title":"Correlating Post-mortem Gross Macroscopy with Histopathological Findings in the Caudate Nucleus in Frontotemporal Lobar Degeneration","presenting_author":"Shervin Pejhan","co_authors":"B. Brower, H. Lee, L. Ang, E. Finger, Q. Zhang","category":"Research Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-17","title":"Real-World Association Between Serum Neurofilament Light Chain and MRI-Defined Disease Activity in Multiple Sclerosis","presenting_author":"Azhar Alanazi","co_authors":"Z. Alfares, A. Svendrovski, B. Ciftci, J. Racosta, P. Riccio, C. Casserly","category":"Clinical Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-18","title":"Treatment Outcomes of Advanced Combination Therapy in Multiple Sclerosis-Inflammatory Bowel Disease Overlap: A retrospective Single-Centre case series","presenting_author":"Azhar Alanazi","co_authors":"S. Vuyyuru, P. Riccio, J. Racosta, C. Casserly, V. Jairath, B. Ciftci","category":"Clinical Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-19","title":"Pediatric epilepsy surgery following stereoelectroencephalography: multi-level data on clinical factors and electrode contact-brain tissue sampling representation","presenting_author":"Kevin Paul Ferraris","co_authors":"A. Akbarpour, D. Adil, A. Thurairajah, A. Skovronska, M. Kregel, R. Eagleson, M.N. Nouri, A. Andrade, and S. de Ribaupierre","category":"Clinical Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-20","title":"Use of Responsive Neurostimulation Beyond the U.S.: International Experience and Outcomes","presenting_author":"Natalia Valencia-Enciso","co_authors":"C. Burbano, I. Castro, J. Burneo, G. Pellegrino, M. Lee-Jones, JC. Lau, DA. Steven, KW. MacDougall, D. Diosy, A. Suller-Marti","category":"Clinical Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-21","title":"The CanDo Brain Health Implementation Initiative","presenting_author":"Abolfazl Avan","co_authors":"A.J. Appleton, W.A. Fisher, S.N. Whitehead, J.K. Shoemaker, V Hachinski","category":"Research Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-22","title":"Erdheim-Chester Disease Presenting as a Subdural Hematoma","presenting_author":"Waseem Yaghmoor","co_authors":"J. Houpy, Y. Li, C. Howlett, L. Ang, J. Megyesi","category":"Clinical Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-23","title":"Low Risk of Ischemic Stroke Recurrence in Young Adults with TIA and PFO: Results From the IMPROVE International Registry","presenting_author":"Fawaz Alotaibi","co_authors":"Diana Ayan, Lakni Abeyesekera, Eduardo Soriano Navarro, Arturo Gonzalez Lara, Jaime Rodriguez Orozco, Zahra Mirza Asgari, Lauren Mai, Sebastian Fridman, Antonio Arauz, Rodrigo Bagur, Luciano A. Sposato","category":"Clinical Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2A | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-24","title":"Preclinical Safety and Efficacy of Intracranial Electrotherapy for Glioma Treatment","presenting_author":"Erin Iredale","co_authors":"N. Fulcher, S. Schmid, T. Peters, E. Wong, M.O. Hebb","category":"Post-Doctoral Fellow","presentation_format":"Poster presentation","training_level":"fellow","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-25","title":"Effectiveness and stimulation parameters of transcutaneous vagus nerve stimulation in patients with epilepsy: a systematic review","presenting_author":"Sydney Papadopoulos","co_authors":"M. Elnazali","category":"Medical Student","presentation_format":"Poster presentation","training_level":"student","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-27","title":"Medulloblastoma in Two Infants with Gorlin Syndrome","presenting_author":"Oviya Ananthakrishnan","co_authors":"M. Poon, A. Mastrolonardo, S. De Ribaupierre, C. Cacciotti","category":"Medical Student","presentation_format":"Poster presentation","training_level":"student","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-28","title":"Resolving Variants of Uncertain Significance in ALS through Integrated In Silico and Functional Approaches","presenting_author":"Minhal Ahmed","co_authors":"K. Volkening, C. McLellan, T. Balci, C. Shoesmith, M. Strong","category":"Medical Student","presentation_format":"Poster presentation","training_level":"student","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-29","title":"Management of GSA: Case Report and Systematic Review of Treatment Strategies","presenting_author":"Khushali Parikh","co_authors":"Dr. A. Mastrolonardo, Dr. A. Mascarenhas","category":"Medical Student","presentation_format":"Poster presentation","training_level":"student","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"},
    {"abstract_number":"POST-30","title":"Navigating The Unknown: Exploring the Lived Experiences of Persons Newly Diagnosed with Multiple Sclerosis in Canada","presenting_author":"Saba Hyarat","co_authors":"V. Smye, W. Koopman","category":"Graduate Student","presentation_format":"Poster presentation","training_level":"student","location":"P2B | 3:15 - 4:10 | Garron/Spriet Lounge"}
  ],
  "judges": [
    {"email":"Alexander.Khaw@lhsc.on.ca","name":"Alexander Khaw","affiliation":""},
    {"email":"Beyza.Ciftci@lhsc.on.ca","name":"Beyza Ciftci","affiliation":""},
    {"email":"cwatling@royalcollege.ca","name":"Chris Watling","affiliation":""},
    {"email":"Deepa.Dash@lhsc.on.ca","name":"Deepa Dash","affiliation":""},
    {"email":"Joseph.Megyesi@lhsc.on.ca","name":"Joseph Megyesi","affiliation":""},
    {"email":"Stephen.Pasternak@sjhc.london.on.ca","name":"Stephen Pasternak","affiliation":""},
    {"email":"Yiu-Chia.Chang@lhsc.on.ca","name":"Yiu-Chia Chang","affiliation":""}
  ],
  "assignments": [
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-1"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-1"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-1"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-2"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-2"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-2"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-3"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-3"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-3"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-5"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-5"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-5"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-6"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-6"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-6"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-7"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-7"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-7"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-8"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-8"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-8"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-9"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-9"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-9"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-10"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-10"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-10"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-11"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-11"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-11"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-12"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-12"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-12"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-13"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-13"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-13"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-14"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-14"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-14"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-15"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-15"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-15"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-16"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-16"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-16"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-17"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-17"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-17"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-18"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-18"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-18"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-20"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-20"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-20"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-21"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-21"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-21"},
    {"judge_email":"cwatling@royalcollege.ca","abstract_number":"PLAT-22"},
    {"judge_email":"Stephen.Pasternak@sjhc.london.on.ca","abstract_number":"PLAT-22"},
    {"judge_email":"Alexander.Khaw@lhsc.on.ca","abstract_number":"PLAT-22"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-1"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-1"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-2"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-2"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-3"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-3"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-4"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-4"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-5"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-5"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-6"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-6"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-7"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-7"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-8"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-8"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-9"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-9"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-10"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-10"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-11"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-11"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-12"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-12"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-13"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-13"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-14"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-14"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-15"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-15"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-16"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-16"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-17"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-17"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-18"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-18"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-19"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-19"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-20"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-20"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-21"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-21"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-22"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-22"},
    {"judge_email":"Yiu-Chia.Chang@lhsc.on.ca","abstract_number":"POST-23"},
    {"judge_email":"Deepa.Dash@lhsc.on.ca","abstract_number":"POST-23"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-24"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-24"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-25"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-25"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-27"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-27"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-28"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-28"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-29"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-29"},
    {"judge_email":"Beyza.Ciftci@lhsc.on.ca","abstract_number":"POST-30"},
    {"judge_email":"Joseph.Megyesi@lhsc.on.ca","abstract_number":"POST-30"}
  ],
  "events": [
    {"name":"CNS Research Day 2026","date":"2026-06-09","is_active":true}
  ],
  "rubrics": [
    {
      "presentation_format": "Oral presentation",
      "is_active": true,
      "items": [
        {"label":"Scientific question","description":"Is the research question clear, relevant, and important?","max_score":5,"sort_order":1},
        {"label":"Methods","description":"Are design and analyses appropriate?","max_score":5,"sort_order":2},
        {"label":"Results","description":"Are results clear and complete?","max_score":5,"sort_order":3},
        {"label":"Interpretation","description":"Are conclusions supported by data?","max_score":5,"sort_order":4},
        {"label":"Slide quality","description":"Are slides readable and organized?","max_score":5,"sort_order":5},
        {"label":"Delivery","description":"Was delivery clear and confident?","max_score":5,"sort_order":6},
        {"label":"Timing","description":"Was time used appropriately?","max_score":5,"sort_order":7},
        {"label":"Response to questions","description":"Did presenter answer thoughtfully?","max_score":5,"sort_order":8},
        {"label":"Overall impression","description":"Overall quality of research and presentation.","max_score":5,"sort_order":9}
      ]
    },
    {
      "presentation_format": "Poster presentation",
      "is_active": true,
      "items": [
        {"label":"Scientific question","description":"Is the research question clear, relevant, and important?","max_score":5,"sort_order":1},
        {"label":"Methods","description":"Are design and analyses appropriate?","max_score":5,"sort_order":2},
        {"label":"Results","description":"Are results clear and complete?","max_score":5,"sort_order":3},
        {"label":"Interpretation","description":"Are conclusions supported by data?","max_score":5,"sort_order":4},
        {"label":"Poster design","description":"Is the poster readable and well organized?","max_score":5,"sort_order":5},
        {"label":"Verbal explanation","description":"Did presenter explain clearly?","max_score":5,"sort_order":6},
        {"label":"Response to questions","description":"Did presenter answer thoughtfully?","max_score":5,"sort_order":7},
        {"label":"Overall impression","description":"Overall quality of research and presentation.","max_score":5,"sort_order":8}
      ]
    }
  ]
}
""")


class Command(BaseCommand):
    help = "Load CNS Research Day 2026 event data (idempotent; clears and reloads submissions/judges/assignments)"

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

        # Rubrics (only created once; not cleared)
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

        # Clear stale data so re-runs are clean
        JudgeAssignment.objects.filter(event=event).delete()
        Submission.objects.filter(event=event).delete()
        Judge.objects.filter(event=event).delete()
        self.stdout.write("Cleared previous submissions, judges, assignments.")

        _PRESENTER_EMAILS = {
            'PLAT-1': 'amirti.vivekanandan@lhsc.on.ca',
            'PLAT-2': 'happy.inibhunu@lhsc.on.ca',
            'PLAT-3': 'jalkharb@uwo.ca',
            'PLAT-5': 'jthrowe3@uwo.ca',
            'PLAT-6': 'cso53@uwo.ca',
            'PLAT-7': 'mhuver@uwo.ca',
            'PLAT-8': 'Fawaz.Alotaibi@lhsc.on.ca',
            'PLAT-9': 'mohamad.abbass@lhsc.on.ca',
            'PLAT-10': 'claudia.burbanodonoso@lhsc.on.ca',
            'PLAT-11': 'Zainab.Alfares@lhsc.on.ca',
            'PLAT-12': 'aoremaki@uwo.ca',
            'PLAT-13': 'dwong2022@meds.uwo.ca',
            'PLAT-14': 'eduardo.sorianonavarro@lhsc.on.ca',
            'PLAT-15': 'trevor.jairam@lhsc.on.ca',
            'PLAT-16': 'kkim492@uwo.ca',
            'PLAT-17': 'bdalal2027@meds.uwo.ca',
            'PLAT-18': 'Carolina.Silveira@sjhc.london.on.ca',
            'PLAT-20': 'derek_george@urmc.rochester.edu',
            'PLAT-21': 'rcouper2@uwo.ca',
            'PLAT-22': 'ivan.castro@lhsc.on.ca',
            'POST-1': 'robin.sawaya@lhsc.on.ca',
            'POST-2': 'salotai5@uwo.ca',
            'POST-3': 'Ryan.wang@lhsc.on.ca',
            'POST-4': 'dwong2022@meds.uwo.ca',
            'POST-5': 'mohammad.alostad@lhsc.on.ca',
            'POST-6': 'ranamoshref@gmail.com',
            'POST-7': 'alexander.mastrolonardo@lhsc.on.ca',
            'POST-8': 'scao262@uwo.ca',
            'POST-9': 'mli2534@uwo.ca',
            'POST-10': 'Lakni.Abeyesekera@lhsc.on.ca',
            'POST-11': 'cso53@uwo.ca',
            'POST-12': 'aahma229@uwo.ca',
            'POST-13': 'bdalal2027@meds.uwo.ca',
            'POST-14': 'akeatin3@uwo.ca',
            'POST-15': 'ajamshi3@uwo.ca',
            'POST-16': 'shervin.pejhan@lhsc.on.ca',
            'POST-17': 'Azhar.Alanazi@lhsc.on.ca',
            'POST-18': 'Azhar.Alanazi@lhsc.on.ca',
            'POST-19': 'kferrar3@uwo.ca',
            'POST-20': 'nvalenc4@uwo.ca',
            'POST-21': 'aavan2@uwo.ca',
            'POST-22': 'waseem.yaghmoor@lhsc.on.ca',
            'POST-23': 'Fawaz.Alotaibi@lhsc.on.ca',
            'POST-24': 'eiredale@uwo.ca',
            'POST-25': 'papadopoulos.syd@gmail.com',
            'POST-27': 'oananthakrishnan2028@meds.uwo.ca',
            'POST-28': 'mahmed12028@meds.uwo.ca',
            'POST-29': 'kparikh2027@meds.uwo.ca',
            'POST-30': 'shyarat@uwo.ca',
        }

        # Submissions
        for row in data["submissions"]:
            cat, _ = Category.objects.get_or_create(event=event, name=row["category"])
            fmt, _ = PresentationFormat.objects.get_or_create(name=row["presentation_format"])
            Submission.objects.create(
                event=event,
                abstract_number=row["abstract_number"],
                title=row["title"],
                presenting_author=row["presenting_author"],
                presenting_author_email=_PRESENTER_EMAILS.get(row["abstract_number"], ""),
                co_authors=row["co_authors"],
                category=cat,
                presentation_format=fmt,
                training_level=row["training_level"],
                abstract_text="",
                location=row["location"],
            )
        self.stdout.write(f"Submissions: {len(data['submissions'])} created")

        # Judges
        for row in data["judges"]:
            Judge.objects.create(
                event=event,
                email=row["email"],
                name=row["name"],
                affiliation=row["affiliation"],
            )
        self.stdout.write(f"Judges: {len(data['judges'])} created")

        # Assignments
        a_created = a_skipped = 0
        for row in data["assignments"]:
            judge = Judge.objects.filter(event=event, email=row["judge_email"]).first()
            submission = Submission.objects.filter(event=event, abstract_number=row["abstract_number"]).first()
            if not judge or not submission:
                a_skipped += 1
                continue
            JudgeAssignment.objects.create(event=event, judge=judge, submission=submission)
            a_created += 1
        self.stdout.write(f"Assignments: {a_created} created, {a_skipped} skipped")

        # Substitute presenters (not original submitter)
        non_competing = ["PLAT-5", "POST-1", "POST-15"]
        # Prior travel/publication award winners (Jairam, D. Wong x2, Al Kharbooshi)
        prior_award_winners = ["PLAT-15", "PLAT-13", "POST-4", "PLAT-3"]
        ineligible = list(set(non_competing + prior_award_winners))
        updated = Submission.objects.filter(event=event, abstract_number__in=ineligible).update(award_eligible=False)
        self.stdout.write(f"Marked {updated} submission(s) as not award-eligible: {', '.join(sorted(ineligible))}")

        self.stdout.write(self.style.SUCCESS("Done."))
