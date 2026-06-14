from pydantic import BaseModel, Field
from typing import List, Optional

class JobParsedData(BaseModel):
    title: str = Field(description="The job title")
    description: str = Field(description="A brief summary of the job description")
    required_skills: List[str] = Field(description="List of required technical and soft skills")
    preferred_skills: List[str] = Field(description="List of nice-to-have or preferred skills", default_factory=list)
    experience_years: Optional[int] = Field(description="Years of experience required. If a range is given, use the minimum.", default=None)
    education_level: Optional[str] = Field(description="Required education level (e.g. Master, Bachelor)", default=None)
    certifications: List[str] = Field(description="List of required or preferred certifications", default_factory=list)
    languages: List[str] = Field(description="List of required languages", default_factory=list)
    location: Optional[str] = Field(description="Job location", default=None)
    contract_type: Optional[str] = Field(description="Type of contract (e.g. CDI, CDD, Freelance)", default=None)
