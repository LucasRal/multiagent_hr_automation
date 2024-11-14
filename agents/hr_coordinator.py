from langchain.prompts import ChatPromptTemplate
from typing import Dict

class HRCoordinatorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Vous êtes un coordinateur RH expérimenté.
            Votre rôle est de synthétiser toutes les informations du processus de recrutement
            et de formuler des recommandations finales.
            
            Analyse du profil:
            {profile_analysis}
            
            Plan d'entretien:
            {interview_plan}
            
            Feedback d'entretien (si disponible):
            {interview_feedback}
            
            Instructions spécifiques:
            1. Analyser les résultats de l'évaluation du profil
            2. Évaluer les réponses aux questions d'entretien
            3. Formuler une recommandation claire
            4. Suggérer les prochaines étapes
            
            Format de réponse attendu:
            {{
                "summary": [résumé global du candidat],
                "evaluation": [évaluation détaillée],
                "recommendation": "GO/NO GO",
                "next_steps": [actions recommandées],
                "risk_factors": [points d'attention éventuels]
            }}
            """)
        ])

    def synthesize(self, 
                   profile_analysis: str, 
                   interview_plan: str, 
                   interview_feedback: str = None) -> Dict:
        messages = self.prompt.format_messages(
            profile_analysis=profile_analysis,
            interview_plan=interview_plan,
            interview_feedback=interview_feedback or "Non disponible"
        )
        response = self.llm.invoke(messages)
        return response.content
