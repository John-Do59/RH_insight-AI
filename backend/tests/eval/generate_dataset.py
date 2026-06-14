import json
import os
import random

questions_templates = [
    ("Quels sont les candidats ayant de l'expérience en {tech} ?", 
     "Les candidats ayant de l'expérience en {tech} sont généralement ceux avec le rôle de {role}."),
    ("Trouve moi un {role} avec {years} ans d'expérience.", 
     "Je recherche dans la base de données pour un {role} avec {years} ans d'expérience."),
    ("Qui maîtrise {tech} et {tech2} ?", 
     "Plusieurs candidats maîtrisent {tech} et {tech2}, notamment dans l'équipe de développement."),
    ("Quel est le niveau d'études requis pour le poste de {role} ?", 
     "Le niveau d'études requis pour le poste de {role} est généralement {edu}."),
    ("Quelles sont les compétences demandées pour une offre de {role} ?", 
     "Pour une offre de {role}, les compétences demandées incluent {tech}, {tech2} et la gestion de projet."),
    ("Y a-t-il des candidats certifiés en {cert} ?", 
     "Oui, il y a des candidats avec la certification {cert}."),
    ("Combien d'années d'expérience faut-il pour être {role} ?", 
     "Il faut généralement {years} années d'expérience pour ce type de poste."),
    ("Je cherche un développeur backend avec de bonnes connaissances en {tech}.", 
     "Un développeur backend avec de bonnes connaissances en {tech} sera très recherché pour ce projet."),
]

techs = ["Python", "Java", "C++", "React", "Vue.js", "Docker", "Kubernetes", "AWS", "GCP", "FastAPI", "Django", "SQL", "PostgreSQL", "MongoDB", "Redis"]
roles = ["Développeur Backend", "Développeur Frontend", "Data Scientist", "DevOps Engineer", "Chef de Projet", "Product Owner", "Architecte Cloud"]
edus = ["Bac+5", "Master", "Licence", "Doctorat", "Ingénieur"]
certs = ["AWS Solutions Architect", "CKA", "Scrum Master", "ITIL", "Google Cloud Professional"]

dataset = []

for i in range(50):
    template = random.choice(questions_templates)
    q = template[0].format(
        tech=random.choice(techs),
        tech2=random.choice(techs),
        role=random.choice(roles),
        years=random.randint(1, 10),
        edu=random.choice(edus),
        cert=random.choice(certs)
    )
    a = template[1].format(
        tech=random.choice(techs),
        tech2=random.choice(techs),
        role=random.choice(roles),
        years=random.randint(1, 10),
        edu=random.choice(edus),
        cert=random.choice(certs)
    )
    
    dataset.append({
        "question": q,
        "ground_truth": a,
    })

os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
with open("backend/tests/eval/eval_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print(f"Generated {len(dataset)} items in eval_dataset.json")
