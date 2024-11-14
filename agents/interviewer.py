from langchain.prompts import ChatPromptTemplate
from typing import Dict


class InterviewerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Vous êtes un expert en conduite d'entretiens professionnels.
            Votre rôle est de préparer un plan d'entretien basé sur l'analyse préalable du profil.
            
            Description du poste:
            {job_description}
            
            Analyse précédente du profil:
            {profile_analysis}
            
            Instructions spécifiques:
            1. Générer des questions techniques adaptées au profil
            2. Préparer des questions comportementales pertinentes
            3. Créer des mises en situation spécifiques au poste
            4. Suggérer des points de discussion pour évaluer les soft skills
            
            Format de réponse attendu:
            {{
                "technical_questions": [liste des questions techniques],
                "behavioral_questions": [questions comportementales],
                "scenarios": [mises en situation],
                "evaluation_criteria": [critères d'évaluation suggérés]
            }}
            """)
        ])

    def prepare_interview(self, profile_analysis: str, job_description: str) -> Dict:
        messages = self.prompt.format_messages(
            profile_analysis=profile_analysis,
            job_description=job_description
        )
        response = self.llm.invoke(messages)
        return response.content