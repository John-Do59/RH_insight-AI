import sqlite3
import os
from app.config.settings import SQL_DB_PATH

def seed_database():
    # Ensure directory exists
    os.makedirs(os.path.dirname(SQL_DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(SQL_DB_PATH)
    cursor = conn.cursor()
    
    # Suppression des anciennes tables pour repartir sur du propre
    cursor.execute("DROP TABLE IF EXISTS skills")
    cursor.execute("DROP TABLE IF EXISTS education")
    cursor.execute("DROP TABLE IF EXISTS experiences")
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute("DROP TABLE IF EXISTS languages")
    cursor.execute("DROP TABLE IF EXISTS candidates")
    
    # Table candidat
    cursor.execute("""
    CREATE TABLE candidates (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        summary TEXT,
        looking_for TEXT,
        extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Table compétences
    cursor.execute("""
    CREATE TABLE skills (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER,
        skill_name TEXT,
        level TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)
    
    # Table expériences
    cursor.execute("""
    CREATE TABLE experiences (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER,
        company TEXT,
        job_title TEXT,
        start_date TEXT,
        end_date TEXT,
        description TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)
    
    # Table formations
    cursor.execute("""
    CREATE TABLE education (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER,
        school TEXT,
        degree TEXT,
        field TEXT,
        start_year INTEGER,
        end_year INTEGER,
        description TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)
    
    # Table projets
    cursor.execute("""
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER,
        name TEXT,
        description TEXT,
        technologies TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)
    
    # Table langues
    cursor.execute("""
    CREATE TABLE languages (
        id INTEGER PRIMARY KEY,
        candidate_id INTEGER,
        language TEXT,
        level TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id)
    )
    """)
    
    # =============================
    # INSERTION DE VOS DONNÉES
    # =============================
    
    # Candidat
    cursor.execute("""
    INSERT INTO candidates (id, first_name, last_name, email, phone, city, summary, looking_for) 
    VALUES (
        1, 'Amaury', 'Rammanat', 
        'rammanatamaury@gmail.com', '0601022320', 'Lille',
        'Développeur IA en formation chez Simplon, recherche alternance sept. 2026. Bases solides en Python et SQL, intérêt pour ML, IA générative et IA agentique. Profil en reconversion avec 15 ans d''expérience professionnelle.',
        'Alternance Développeur IA pour Sept 2026'
    )
    """)
    
    # Compétences
    skills = [
        (1, 1, 'Python', 'Avancé'),
        (2, 1, 'SQL', 'Avancé'),
        (3, 1, 'PostgreSQL', 'Intermédiaire'),
        (4, 1, 'Supabase', 'Intermédiaire'),
        (5, 1, 'Docker', 'Intermédiaire'),
        (6, 1, 'Git', 'Avancé'),
        (7, 1, 'GitHub', 'Avancé'),
        (8, 1, 'Linux Ubuntu', 'Intermédiaire'),
        (9, 1, 'Bash', 'Intermédiaire'),
        (10, 1, 'Pandas', 'Avancé'),
        (11, 1, 'NumPy', 'Avancé'),
        (12, 1, 'Matplotlib', 'Intermédiaire'),
        (13, 1, 'Seaborn', 'Intermédiaire'),
        (14, 1, 'Scikit-learn', 'Intermédiaire'),
        (15, 1, 'PyTorch', 'Débutant'),
        (16, 1, 'TensorFlow', 'Débutant'),
        (17, 1, 'Machine Learning', 'Intermédiaire'),
        (18, 1, 'Langchain', 'Intermédiaire'),
        (19, 1, 'RAG', 'Intermédiaire'),
        (20, 1, 'LLM', 'Intermédiaire'),
        (21, 1, 'Agents IA', 'Intermédiaire'),
        (22, 1, 'MCP', 'Débutant'),
        (23, 1, 'N8N', 'Intermédiaire'),
        (24, 1, 'Streamlit', 'Avancé'),
        (25, 1, 'MLflow', 'Débutant'),
        (26, 1, 'FastAPI', 'Intermédiaire'),
        (27, 1, 'Django', 'Débutant'),
        (28, 1, 'HTML/CSS', 'Intermédiaire'),
        (29, 1, 'JavaScript', 'Débutant'),
        (30, 1, 'SwiftUI', 'Intermédiaire'),
        (31, 1, 'Xcode', 'Intermédiaire'),
        (32, 1, 'Figma', 'Débutant'),
        (33, 1, 'GPT/Claude/Gemini', 'Avancé'),
        (34, 1, 'Agile', 'Intermédiaire'),
        (35, 1, 'TypeScript', 'Débutant'),
        (36, 1, 'Node.js', 'Débutant'),
    ]
    cursor.executemany("INSERT INTO skills (id, candidate_id, skill_name, level) VALUES (?, ?, ?, ?)", skills)
    
    # Formations
    education = [
        (1, 1, 'Simplon', 'Développeur en Intelligence Artificielle', 'IA, ML, Data', 2025, 2026, 
         'RNCP niveau 6. Collecte et stockage données, intégration modèles IA, développement apps web IA, MLOps, feature engineering.'),
        (2, 1, 'Simplon', 'Apple Foundation Programme Extended', 'Développement iOS', 2025, 2025,
         'Swift, SwiftUI, SwiftData, Xcode, Figma'),
        (3, 1, 'Simplon', 'Développeur Intégrateur Web', 'Développement Web', 2024, 2025,
         'HTML, CSS, SCSS, JavaScript, Linux Ubuntu, Bash, Git, GitHub'),
        (4, 1, 'Simplon', 'Apple Foundation Programme', 'Développement iOS', 2024, 2024,
         'Swift, SwiftUI, Xcode, Figma'),
        (5, 1, 'ULCO Dunkerque', 'Licence Sciences Économiques et Sociales', 'Économie', 2009, 2010, ''),
        (6, 1, 'ULCO Dunkerque', 'DEUST Gestionnaire Entrepôts et Logistique', 'Logistique', 2008, 2009, ''),
        (7, 1, 'Lycée Jean Bart Dunkerque', 'Baccalauréat', 'Économie', 2007, 2008, ''),
    ]
    cursor.executemany("INSERT INTO education (id, candidate_id, school, degree, field, start_year, end_year, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", education)
    
    # Expériences
    experiences = [
        (1, 1, 'Indépendant', 'Paysagiste', '2020', '2025', 
         'Création et entretien des espaces verts. Travail en autonomie, gestion de projets, relation client.'),
        (2, 1, 'Diverses entreprises', 'Gestionnaire de milieux naturels', '2010', '2020',
         'Gestion et entretien de milieux naturels.'),
        (3, 1, 'Entreprise logistique', 'Gestionnaire entrepôt et logistique', '2008', '2010',
         'Gestion informatique des stocks avec SAP et Excel.'),
        (4, 1, 'Diverses entreprises', 'Magasinier polyvalent', '2005', '2008',
         'Grande distribution, industrie, logistique, BTP.'),
    ]
    cursor.executemany("INSERT INTO experiences (id, candidate_id, company, job_title, start_date, end_date, description) VALUES (?, ?, ?, ?, ?, ?, ?)", experiences)
    
    # Projets
    projects = [
        (1, 1, 'Sport-Unity IA', 'Application iOS avec coach fitness et nutrition via chatbot IA', 
         'Swift, SwiftUI, IA, Chatbot'),
        (2, 1, 'CV Chatbot', 'Chatbot vocal pour interroger mon CV avec RAG et SQL', 
         'Python, Langchain, Streamlit, RAG, LangGraph'),
    ]
    cursor.executemany("INSERT INTO projects (id, candidate_id, name, description, technologies) VALUES (?, ?, ?, ?, ?)", projects)
    
    # Langues
    languages = [
        (1, 1, 'Français', 'Natif'),
        (2, 1, 'Anglais', 'B1'),
        (3, 1, 'Espagnol', 'A2'),
    ]
    cursor.executemany("INSERT INTO languages (id, candidate_id, language, level) VALUES (?, ?, ?, ?)", languages)
    
    conn.commit()
    conn.close()
    print(f"✅ Base de données initialisée manuellement avec succès dans : {SQL_DB_PATH}")


if __name__ == "__main__":
    seed_database()
