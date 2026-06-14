from pydantic import BaseModel, Field
from typing import List, Optional

class ExperienceSchema(BaseModel):
    company: str = Field(description="Name of the company")
    title: str = Field(description="Job title")
    duration: Optional[str] = Field(description="Duration or dates of employment", default=None)
    description: Optional[str] = Field(description="Description of responsibilities and achievements", default=None)

class CandidateParsedData(BaseModel):
    first_name: Optional[str] = Field(description="First name of the candidate", default=None)
    last_name: Optional[str] = Field(description="Last name of the candidate", default=None)
    email: Optional[str] = Field(description="Email address", default=None)
    title: Optional[str] = Field(description="Current or most recent job title", default=None)
    location: Optional[str] = Field(description="Candidate location", default=None)
    experience_years: Optional[int] = Field(description="Total years of professional experience", default=None)
    summary: Optional[str] = Field(description="A brief professional summary", default=None)
    skills: List[str] = Field(description="List of all technical and soft skills", default_factory=list)
    education: List[str] = Field(description="List of degrees and schools", default_factory=list)
    experiences: List[ExperienceSchema] = Field(description="List of professional experiences", default_factory=list)
    certifications: List[str] = Field(description="List of certifications", default_factory=list)
    languages: List[str] = Field(description="List of spoken languages", default_factory=list)
