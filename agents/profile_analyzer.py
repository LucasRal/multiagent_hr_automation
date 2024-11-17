from langchain.prompts import ChatPromptTemplate
from typing import Dict
import json

class ProfileAnalyzerValidationError(Exception):
    """Custom exception for profile analyzer validation errors"""
    pass

class ProfileAnalyzerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.template = """Vous êtes un expert en analyse de CV et profils professionnels.
        Votre rôle est d'analyser méticuleusement l'adéquation entre un profil et un poste.
        
        Description du poste:
        {job_description}
        
        CV du candidat:
        {cv_content}
        
        Instructions spécifiques:
        1. Extraire et évaluer les compétences techniques et soft skills
        2. Calculer un score de correspondance basé sur les exigences du poste
        3. Identifier les points forts et les lacunes potentielles
        4. Suggérer des points spécifiques à approfondir en entretien
        
        Format de réponse attendu:
        {{
            "matching_score": <score sur 100>,
            "key_skills": [liste des compétences clés identifiées],
            "strengths": [points forts],
            "gaps": [points à approfondir],
            "interview_topics": [sujets suggérés pour l'entretien]
        }}
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.template)
        ])

    def validate_inputs(self, job_description: str, cv_content: str) -> None:
        """Validate inputs before processing"""
        if not job_description or job_description.isspace():
            raise ProfileAnalyzerValidationError("Job description cannot be empty")
        
        if not cv_content or cv_content.isspace():
            raise ProfileAnalyzerValidationError("CV content cannot be empty")
            
        if len(job_description.split()) < 10:
            raise ProfileAnalyzerValidationError("Job description too short - needs at least 10 words")
            
        if len(cv_content.split()) < 10:
            raise ProfileAnalyzerValidationError("CV content too short - needs at least 10 words")
            
        # Check for required sections in job description
        required_job_sections = ["responsabilités", "requis"]
        if not any(section.lower() in job_description.lower() for section in required_job_sections):
            raise ProfileAnalyzerValidationError("Job description missing required sections (Responsabilités, Requis)")
            
        # Check for required sections in CV
        required_cv_sections = ["expérience", "compétences"]
        if not any(section.lower() in cv_content.lower() for section in required_cv_sections):
            raise ProfileAnalyzerValidationError("CV missing required sections (Expérience, Compétences)")

    def analyze(self, job_description: str, cv_content: str) -> Dict:
        """Analyze profile with validation"""
        try:
            # Validate inputs first
            self.validate_inputs(job_description, cv_content)
            
            # Format messages using the template
            messages = self.prompt.format_messages(
                job_description=job_description,
                cv_content=cv_content
            )
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                raise ProfileAnalyzerValidationError("LLM response was not in valid JSON format")
                
        except Exception as e:
            raise ProfileAnalyzerValidationError(f"Analysis failed: {str(e)}")