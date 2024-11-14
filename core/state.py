from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentState:
    job_description: str
    cv_content: str
    profile_analysis: Optional[str] = None
    interview_plan: Optional[str] = None
    interview_feedback: Optional[str] = None
    final_recommendation: Optional[str] = None
    current_step: str = "start"
    error: Optional[str] = None

    def update(self, **kwargs) -> 'AgentState':
        """Create a new AgentState with updated values."""
        new_data = self.to_dict()
        new_data.update(kwargs)
        return AgentState(**new_data)

    @classmethod
    def create_initial(cls, job_description: str, cv_content: str, interview_feedback: Optional[str] = None) -> 'AgentState':
        return cls(
            job_description=job_description,
            cv_content=cv_content,
            interview_feedback=interview_feedback
        )

    def to_dict(self) -> dict:
        return {
            "job_description": self.job_description,
            "cv_content": self.cv_content,
            "profile_analysis": self.profile_analysis,
            "interview_plan": self.interview_plan,
            "interview_feedback": self.interview_feedback,
            "final_recommendation": self.final_recommendation,
            "current_step": self.current_step,
            "error": self.error
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentState':
        return cls(**data)

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentState':
        # Clean the input data to only include our fields
        valid_fields = cls.__annotations__.keys()
        cleaned_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**cleaned_data)
