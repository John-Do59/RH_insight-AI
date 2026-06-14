"""
Utilitaires pour extraire le texte de fichiers PDF, DOCX et TXT.
"""
import io
from typing import Optional


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extrait le texte d'un fichier PDF via pdfplumber."""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            return "\n".join(pages).strip()
    except Exception as e:
        # Fallback pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        except Exception:
            raise ValueError(f"Impossible de lire le PDF: {e}")


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extrait le texte d'un fichier DOCX."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(para.text for para in doc.paragraphs).strip()
    except Exception as e:
        raise ValueError(f"Impossible de lire le DOCX: {e}")


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Détecte automatiquement le format et extrait le texte.
    Supporte : PDF, DOCX, DOC, TXT, MD
    """
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ("docx",):
        return extract_text_from_docx(file_bytes)
    elif ext in ("txt", "md", "text"):
        return file_bytes.decode("utf-8", errors="replace").strip()
    else:
        # Tentative PDF en premier, puis texte brut
        try:
            return extract_text_from_pdf(file_bytes)
        except Exception:
            return file_bytes.decode("utf-8", errors="replace").strip()
