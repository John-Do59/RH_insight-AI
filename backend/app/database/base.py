# Import all the models, so that Base has them before being imported by Alembic
from backend.app.database.session import Base
from backend.app.models.user import User
from backend.app.models.candidat import Candidate, Education, Experience, Skill, Project, Language
