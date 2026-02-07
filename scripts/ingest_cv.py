import os
from app.pdf.extractor import extract_text_from_pdf
from app.utils.preprocess import clean_spaced_text
from app.rag.chunking import get_text_chunks
from app.rag.vector_store import add_texts_to_vector_store
from app.sql.ingest import extract_structured_data
from app.sql.database import get_engine
from sqlalchemy import text
from app.utils.logger import logger

def ingest_cv(pdf_path: str):
    logger.info(f"Starting ingestion for {pdf_path}")
    
    # 1. Extract Text
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        logger.error("No text extracted from PDF.")
        return

    # 2. Clean Text (important for spaced-out characters)
    text_content = clean_spaced_text(raw_text)
    logger.info("Text cleaned and normalized.")

    # 2. RAG Ingestion (Vector Store)
    chunks = get_text_chunks(text_content)
    metadatas = [{"source": os.path.basename(pdf_path)} for _ in chunks]
    add_texts_to_vector_store(chunks, metadatas)
    logger.info(f"Added {len(chunks)} chunks to vector store.")

    # 3. SQL Ingestion (Structured Data)
    structured_data = extract_structured_data(text_content)
    if structured_data:
        engine = get_engine()
        with engine.connect() as conn:
            # Insert candidate
            ins_cand = text("""
                INSERT INTO candidates (first_name, last_name, email, phone, city, summary, looking_for)
                VALUES (:first_name, :last_name, :email, :phone, :city, :summary, :looking_for)
                RETURNING id
            """)
            result = conn.execute(ins_cand, {
                "first_name": structured_data.get("first_name"),
                "last_name": structured_data.get("last_name"),
                "email": structured_data.get("email"),
                "phone": structured_data.get("phone"),
                "city": structured_data.get("city"),
                "summary": structured_data.get("summary"),
                "looking_for": structured_data.get("looking_for")
            })
            candidate_id = result.fetchone()[0]

            # Insert experiences
            for exp in structured_data.get("experiences", []):
                ins_exp = text("""
                    INSERT INTO experiences (candidate_id, company, job_title, start_date, end_date, description)
                    VALUES (:candidate_id, :company, :job_title, :start_date, :end_date, :description)
                """)
                conn.execute(ins_exp, {
                    "candidate_id": candidate_id,
                    "company": exp.get("company"),
                    "job_title": exp.get("job_title"),
                    "start_date": exp.get("start_date"),
                    "end_date": exp.get("end_date"),
                    "description": exp.get("description")
                })

            # Insert education
            for edu in structured_data.get("education", []):
                ins_edu = text("""
                    INSERT INTO education (candidate_id, school, degree, field, start_year, end_year)
                    VALUES (:candidate_id, :school, :degree, :field, :start_year, :end_year)
                """)
                conn.execute(ins_edu, {
                    "candidate_id": candidate_id,
                    "school": edu.get("school"),
                    "degree": edu.get("degree"),
                    "field": edu.get("field"),
                    "start_year": edu.get("start_year"),
                    "end_year": edu.get("end_year")
                })

            # Insert projects
            for proj in structured_data.get("projects", []):
                ins_proj = text("""
                    INSERT INTO projects (candidate_id, name, description, technologies)
                    VALUES (:candidate_id, :name, :description, :technologies)
                """)
                conn.execute(ins_proj, {
                    "candidate_id": candidate_id,
                    "name": proj.get("name"),
                    "description": proj.get("description"),
                    "technologies": proj.get("technologies")
                })

            # Insert skills
            for skill in structured_data.get("skills", []):
                ins_skill = text("""
                    INSERT INTO skills (candidate_id, skill_name, level)
                    VALUES (:candidate_id, :skill_name, :level)
                """)
                conn.execute(ins_skill, {
                    "candidate_id": candidate_id,
                    "skill_name": skill.get("skill_name"),
                    "level": skill.get("level")
                })

            # Insert languages
            for lang in structured_data.get("languages", []):
                ins_lang = text("""
                    INSERT INTO languages (candidate_id, language, level)
                    VALUES (:candidate_id, :language, :level)
                """)
                conn.execute(ins_lang, {
                    "candidate_id": candidate_id,
                    "language": lang.get("language"),
                    "level": lang.get("level")
                })
            conn.commit()
        logger.info(f"SQL data ingested for candidate ID {candidate_id}")
    else:
        logger.warning("Failed to extract structured data for SQL ingestion.")

if __name__ == "__main__":
    # Test path
    import glob
    pdf_files = glob.glob("app/pdf/*.pdf")
    if pdf_files:
        ingest_cv(pdf_files[0])
