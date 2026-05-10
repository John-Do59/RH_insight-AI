CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    city TEXT,
    summary TEXT,
    looking_for TEXT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    school TEXT,
    degree TEXT,
    field TEXT,
    start_year TEXT,
    end_year TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    company TEXT,
    job_title TEXT,
    start_date TEXT,
    end_date TEXT,
    description TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    skill_name TEXT,
    level TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    name TEXT,
    description TEXT,
    technologies TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);

CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    language TEXT,
    level TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
);
