from langchain.prompts import ChatPromptTemplate
from typing import Dict


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

    def analyze(self, job_description: str, cv_content: str) -> Dict:
        messages = self.prompt.format_messages(
            job_description=job_description,
            cv_content=cv_content
        )
        response = self.llm.invoke(messages)
        return response.content


